


from .parts.add_delegator import instantiate_delegate, should_instantiate_delegate

from .parts.delegator_behaviors import (act,delegate_act,
                                        may_act_this_timestep)

from .parts.revenue import (revenue_amt, store_revenue, distribute_revenue, mint_GRT,
                                                    store_indexing_revenue,
                                                    store_query_revenue,
                                                    distribute_indexer_revenue,
                                                    distribute_revenue_to_pool)

from .parts.private_price import compute_and_store_private_prices

from .parts.delegator_behaviors_bookkeeping import (compute_half_life_vested_shares,
                                                    compute_cliff_vested_shares,
                                                    account_global_state_from_delegator_states, 
                                                    store_total_delegated_stake,
                                                    store_shares,
                                                    store_spot_price)


psubs = [
    {
        'label': 'Update Vested Shares',
        'policies': {
        },
        'variables': {
            # 'delegators': compute_half_life_vested_shares  
            'delegators': compute_cliff_vested_shares
        }
    },
    {
        'label': 'Revenue Arrival Process',
        'policies': {
            'revenue_amt': revenue_amt  # how much is paid in.
        },
        'variables': {
            'period_revenue': store_revenue,
            'GRT': mint_GRT,
            'indexing_revenue': store_indexing_revenue, 
            'query_revenue': store_query_revenue,         
        },
    },
    {
        'label': 'Distribute Revenue',
        'policies': {
        },
        'variables': {
            'delegators': distribute_revenue,
            'indexer_revenue': distribute_indexer_revenue,
            'total_delegated_stake': distribute_revenue_to_pool,

        }
    },
    {
        # if there's a vacant spot, flip a coin
        # (heads, they join, tails nobody joins)
        'label': 'Add Delegator',
        'policies': {
            'should_instantiate_delegate': should_instantiate_delegate
            },
        'variables': {
            'delegators': instantiate_delegate,
            },
    },
    {
        'label': 'Compute and Store Private Prices',
        'policies': {            
        },
        'variables': {
            'delegators': compute_and_store_private_prices,
        },
    },
    {
        'label': 'Delegator Behaviors',
        'policies': {
            # outputs ordered list of acting delegatorIds this timestep
            'may_act_this_timestep': may_act_this_timestep
        },
        'variables': {
            'delegators': delegate_act,
        },
    },
    {
        'label': 'Delegator Behaviors Bookkeeping',
        'policies': {
            'account_global_state_from_delegator_states': account_global_state_from_delegator_states
        },
        'variables': {
            'total_delegated_stake': store_total_delegated_stake,
            'shares': store_shares,
            'spot_price': store_spot_price,
        },
    },
]

