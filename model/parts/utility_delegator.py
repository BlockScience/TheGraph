from .utility_agent import UtilityAgent, UtilityComponents
from .delegate_front_runner_rules import DelegateFrontRunnerRules


class UtilityComponentsDelegator(UtilityComponents):
    def __init__(self, G, opportunity_cost):
        super().__init__()

        self._attributes = {
            'delegationAmount': G,
            'opportunityCost': opportunity_cost
        }

        self._actions = {
            'delegate': {
                'event': "delegate",
                'target': None,
                'amount': self._attributes['delegationAmount'],
                'status': "have delegated"
            },
            'undelegate': {
                'event': "undelegate",
                'targt': None,
                'status': "have sent undelegate()"
            },
        }

        # NOTE: global allows this function to pickle, somehow (https://www.pythonpool.com/cant-pickle-local-object/)
        global utility
        def utility(delegator, indexer, ownDelegation=None,
                    opportunityCost=0, rewardCycles=1):
            # if indexer in delegator.states()[-1]['delegated']:
            if delegator.is_delegated():
                # ownDelegation = delegator.states()[-1]['delegated'][indexer]['amount']
                ownDelegation = delegator.shares

            # TODO: Check if these three have correct values.
            reward = delegator.beliefs[-1][indexer.id]['reward']
            cut = indexer.indexer_revenue_cut
            delegation = indexer.pool_delegated_stake

            r = opportunityCost
            # ell = delegator._inputs[-1]['epochsPerAllocation']
            ell = delegator._inputs[-1]['allocation_days']
            # allocation_days
            d = delegator._inputs[-1]['delegation_unbonding_period_epochs']
            tau = delegator._inputs[-1]['delegation_tax_rate']
            n = rewardCycles

            # TODO: Check this change
            # revenue = n * reward * (1 - cut) * (ownDelegation / delegation)
            revenue = 0 if delegation == 0 else n * reward * (1 - cut) * (ownDelegation / delegation)

            cost = ownDelegation * (r * ((n - 1) * ell + d) + tau / (1 - tau))
            return revenue - cost

        self._utility = utility

        # NOTE: if _beliefs is set to a function, we can't use it to hold the beliefs set later.
        # def beliefs():
        #     return []
        #
        # self._beliefs = beliefs


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

        # i
        # TODO: What is this supposed to do? You can't update a list... -Josh
        for indexer_id, indexer in available_indexers.items():
            # TODO: is indexer_revenue the right thing to put here? - Josh
            belief.update(
                {
                    indexer_id: {'reward': indexer.indexer_revenue}
                }
            )
            # belief.update(
            #     {
            #         indexer: {'reward': indexer['indexer_revenue']}
            #     }
            # )

        self._beliefs.append(belief)
        return

    # this only works for one indexer currently because delegator is an attribute of an indexer.
    def generate_strategies(self):
        available_indexers = self._inputs[-1]['available_indexers']
        payoff = {}
        strategy = []
        for indexer_id, indexer in available_indexers.items():
            # 1. Evaluate marginal utility of each indexer for fixed delegation amount
            # Note that ._utility will use an existing delegation amount (if it
            # exists) instead of using self._delegationAmount, if the two are different

            payoff[indexer_id] = self.utility(self, indexer,
                                              ownDelegation=self._attributes['delegationAmount'],
                                              opportunityCost=1)

        for indexer in available_indexers:
            # 2. If already delegated to this indexer, see if worth extending
            if self.is_delegated():
                if payoff[indexer] < 0:
                    # Not worth extending, so undelegate from this indexer
                    strategy.append(
                        dict(self._actions['undelegate'], **{'target': indexer})
                    )

        # 3. Get indexer with highest marginal utility gain
        best_indexer = max(payoff, key=payoff.get)

        # 4. If not delegating to best currently, delegate to best if profitable and affordable
        if payoff[best_indexer] >= 0 and best_indexer not in self.is_delegated():
            if self._delegationAmount <= self.holdings:
                strategy.append(
                    dict(self._actions['delegate'], **{'target': best_indexer})
                )
        if strategy:
            self.plan = strategy

    def generate_output(self):
        self.output = []
        if self.plan:
            # output must be a list of events.
            self.output.append(self.plan)


