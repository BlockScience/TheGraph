from .utility_agent import UtilityComponents


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
            'withdraw': {
                'event': "withdraw",
                'type': 'stakeDelegatedWithdrawns',
                'indexer': None,
                'status': "have withdrawn"
            },
        }

        self._utility = self.utility

    # NOTE: global allows this function to pickle, somehow (https://www.pythonpool.com/cant-pickle-local-object/)
    # global utility
    @staticmethod
    def utility(delegator, indexer, own_delegation=None,
                p_opportunity_cost=0, reward_cycles=1):
        # if indexer in delegator.states()[-1]['delegated']:
        if indexer.id in delegator.delegations and delegator.delegations[indexer.id].is_delegated():
            # own_delegation = delegator.states()[-1]['delegated'][indexer]['amount']
            # own_delegation = delegator.shares  # This should really be the amount of delegated tokens not shares
            own_delegation = own_delegation / indexer.shares * indexer.pool_delegated_stake  # this is in tokens

        reward = delegator.beliefs[-1][indexer.id]['most_recent_indexing_reward']
        cut = indexer.indexer_revenue_cut
        delegation = indexer.shares
        # delegation = indexer.pool_delegated_stake

        r = p_opportunity_cost
        ell = delegator._inputs[-1]['allocation_days']
        d = delegator._inputs[-1]['delegation_unbonding_period_epochs']
        tau = delegator._inputs[-1]['delegation_tax_rate']
        n = reward_cycles

        revenue = n * reward * (1 - cut) if delegation == 0 else n * reward * (1 - cut) * (
                    own_delegation / (delegation + own_delegation))

        cost = own_delegation * (r * ((n - 1) * ell + d) + tau / (1 - tau))

        if delegation != 0:
            tax_threshold = (n * reward * (1 - cut) / delegation) / (1 + (n * reward * (1 - cut) / delegation))
            print(f'{tax_threshold=}')
        if reward > 0:
            print(f'{reward=}')

        if revenue > 0:
            print(f'{revenue=}')

        return revenue - cost
