from .utility_agent import UtilityAgent, UtilityComponents
from .delegate_front_runner_rules import DelegateFrontRunnerRules
from decimal import Decimal


class UtilityComponentsDelegator(UtilityComponents):
    def __init__(self, G, opportunity_cost):
        super().__init__()

        self._attributes = {
            'delegation_amount': G,
            'opportunity_cost': opportunity_cost
        }

        self._actions = {
            'delegate': {
                'event': "delegate",
                'type': 'stakeDelegateds',
                'indexer': None,
                'tokens': self._attributes['delegation_amount'],
                'status': "have delegated"
            },
            'undelegate': {
                'event': "undelegate",
                'type': 'stakeDelegatedLockeds',
                'indexer': None,
                'status': "have sent undelegate()"
            },
        }

        # NOTE: global allows this function to pickle, somehow (https://www.pythonpool.com/cant-pickle-local-object/)
        global utility
        def utility(delegator, indexer, own_delegation=None,
                    opportunity_cost=0, reward_cycles=1):
            # if indexer in delegator.states()[-1]['delegated']:
            if delegator.is_delegated():
                # own_delegation = delegator.states()[-1]['delegated'][indexer]['amount']
                # own_delegation = delegator.shares  # This should really be the amount of delegated tokens not shares
                own_delegation = own_delegation / indexer.shares * indexer.pool_delegated_stake  # this is in tokens

            reward = delegator.beliefs[-1][indexer.id]['most_recent_indexing_reward']
            cut = indexer.indexer_revenue_cut
            delegation = indexer.shares
            # delegation = indexer.pool_delegated_stake

            r = opportunity_cost
            ell = delegator._inputs[-1]['allocation_days']
            d = delegator._inputs[-1]['delegation_unbonding_period_epochs']
            tau = delegator._inputs[-1]['delegation_tax_rate']
            n = reward_cycles

            revenue = n * reward * (1 - cut) if delegation == 0 else n * reward * (1 - cut) * (own_delegation / (delegation + own_delegation))

            cost = own_delegation * (r * ((n - 1) * ell + d) + tau / (1 - tau))

            if delegation != 0:
                tax_threshold = (n * reward * (1 - cut) / delegation) / (1+(n * reward * (1 - cut)  / delegation))
                print(f'{tax_threshold=}')
            if reward > 0:
                print(f'{reward=}')

            if revenue > 0:
                print(f'{revenue=}')

            return revenue - cost

        self._utility = utility


class UtilityDelegator(UtilityAgent):

    def __init__(self, delegator_id, initial_account_balance, components):
        super().__init__(delegator_id, initial_account_balance, components)
        self._inputs = []
        self.state = [
            {
                # get this from indexer.delegators
                'delegations': {},
            }
        ]

    def inputs(self, newInput):
        # TODO: remove the ones we don't need, add the ones we do.
        self._inputs.append(
            {
                'available_indexers': newInput['available_indexers'],
                'current_period': newInput['current_period'],
                'dispute_channel_epochs': newInput['dispute_channel_epochs'],
                'allocation_days': newInput['allocation_days'],
                'delegation_unbonding_period_epochs': newInput['delegation_unbonding_period_epochs'],
                'account_balance': newInput['account_balance'],
                'delegation_tax_rate': newInput['delegation_tax_rate'],
                'minimum_delegation_period_epochs': newInput['minimum_delegation_period_epochs'],
            }
        )

    def update_beliefs(self):
        # if there is a belief, start with that.
        if self._beliefs:
            belief = self._beliefs[-1]
        else:
            belief = {}
        available_indexers = self._inputs[-1]['available_indexers']

        for indexer_id, indexer in available_indexers.items():
            # NOTE: is indexer_revenue the right thing to put here? - we are using the most_recent_indexing_reward.
            belief.update(
                {
                    indexer_id: {'most_recent_indexing_reward': indexer.most_recent_indexing_reward}
                }
            )

        self._beliefs.append(belief)
        return

    # this only works for one indexer currently because delegator is an attribute of an indexer.
    def generate_strategies(self):
        if self._inputs[-1]['current_period'] == self.epoch_of_last_action:
            # the delegator already acted this period.
            self.plan = None
            return

        available_indexers = self._inputs[-1]['available_indexers']
        payoff = {}
        strategy = []
        for indexer_id, indexer in available_indexers.items():
            # 1. Evaluate marginal utility of each indexer for fixed delegation amount
            # Note that ._utility will use an existing delegation amount (if it
            # exists) instead of using self._delegation_amount, if the two are different

            payoff[indexer_id] = self.utility(self, indexer,
                                              own_delegation=self._attributes['delegation_amount'],
                                              opportunity_cost=self._attributes['opportunity_cost'])
            print(f'{payoff[indexer_id]=}')

        for indexer in available_indexers:
            # 2. If already delegated to this indexer, see if worth extending
            if self.is_delegated():
                if payoff[indexer] < 0:
                    if self.has_rewards_assigned_since_delegation:
                        # Not worth extending, so undelegate from this indexer
                        inpt = self._inputs[-1]
                        current_period = inpt['current_period']
                        strategy.append(
                            dict(self._actions['undelegate'], **{'indexer': indexer,
                                                                 'delegator': self.id,
                                                                 'shares': self.shares,
                                                                 'until': current_period + inpt['delegation_unbonding_period_epochs']})
                        )

        # 3. Get indexer with highest marginal utility gain
        best_indexer = max(payoff, key=payoff.get)

        # 4. If not delegating to best currently, delegate to best if profitable and affordable
        # if payoff[best_indexer] >= 0 and best_indexer not in self.is_delegated():
        # TODO: make sure we are not delegated to the indexer we chose, not just any indexer. (this works in single indexer scenario)
        if payoff[best_indexer] >= 0 and not self.is_delegated():
            if self._attributes['delegation_amount'] <= self.holdings:
                strategy.append(
                    dict(self._actions['delegate'],
                         **{'indexer': best_indexer,
                            'delegator': self.id})
                )
        if strategy:
            self.plan = strategy[-1]

    def generate_output(self):
        self.output = []
        if self.plan:
            # output must be a list of events.
            self.output.append(self.plan)


