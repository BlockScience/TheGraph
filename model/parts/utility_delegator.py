from .utility_agent import UtilityAgent


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
        if self._inputs[-1]['current_period'] == self.epoch_of_last_action and self.plan:
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
                                              p_opportunity_cost=self._attributes['opportunity_cost'])
            print(f'{payoff[indexer_id]=}')

        inpt = self._inputs[-1]

        # TODO: make this work with multiple indexers
        # ---- should we withdraw from each indexer?
        for indexer_id in available_indexers:
            if indexer_id in self.delegations and self.delegations[indexer_id].undelegated_tokens > 0:
                if self.delegations[indexer_id].locked_in_undelegation_until <= inpt['current_period']:
                    strategy.append(
                        dict(self._actions['withdraw'], **{'indexer': indexer_id,
                                                           'delegator': self.id,
                                                           'tokens': self.delegations[indexer_id].undelegated_tokens})
                    )

        # ---- should we undelegate to each indexer?
        for indexer_id in available_indexers:
            # 2. If already delegated to this indexer, see if worth extending
            if indexer_id in self.delegations and self.delegations[indexer_id].is_delegated():
                if payoff[indexer_id] < 0:
                    # Not worth extending, so undelegate from this indexer
                    # must get has_rewards_assigned_since_delegation from indexer, because not available on portfolio
                    if available_indexers[indexer_id].delegators[self.id].has_rewards_assigned_since_delegation:
                        current_period = inpt['current_period']
                        strategy.append(
                            dict(self._actions['undelegate'], **{'indexer': indexer_id,
                                                                 'delegator': self.id,
                                                                 'shares': self.delegations[indexer_id].shares,
                                                                 'until': current_period + inpt['delegation_unbonding_period_epochs']})
                        )

        # ---- should we delegate?
        # 3. Get indexer with highest marginal utility gain
        best_indexer = max(payoff, key=payoff.get)

        # 4. If not delegating to best currently, delegate to best if profitable and affordable
        # if payoff[best_indexer] >= 0 and best_indexer not in self.is_delegated():
        # TODO: make sure we are not delegated to the indexer we chose, not just any indexer. (this works in single indexer scenario)
        delegated_to_best_indexer = best_indexer in self.delegations and self.delegations[best_indexer].is_delegated()
        if payoff[best_indexer] >= 0 and not delegated_to_best_indexer:
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


