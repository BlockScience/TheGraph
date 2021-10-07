from .parts.indexer_behaviors import (cumulative_deposited_stake, indexer_actions,
                                      store_query_fee_cut,
                                      store_indexer_fee_cut)
                                      
# , deposit_stake, add_shares_to_indexer, add_shares_to_pool)

from .parts.delegator_behaviors import (delegate, undelegate, withdraw,
                                        delegate_actions,
                                        undelegate_actions,
                                        withdraw_actions)

from .parts.revenue import (revenue_amt, distribute_revenue_to_indexer, 
                            mint_GRT, distribute_revenue_to_pool,
                            store_indexing_revenue, store_query_revenue,
                            cumulative_non_indexer_revenue)

# from .parts.private_price import compute_and_store_private_prices

from .parts.delegator_behaviors_bookkeeping import (store_shares, 
                                                    subtract_undelegated_stake_from_pool)


psubs = [
    {
        'label': 'Stake Deposit',
        'policies': {
            'indexer_actions': indexer_actions
        },
        'variables': {
            'indexers': cumulative_deposited_stake
        },
    },
    {
        'label': 'Delegation Parameters - Query Fee',
        'policies': {
            'indexer_actions': indexer_actions
        },
        'variables': {
            'indexers': store_query_fee_cut,
        },
    },    
    {
        'label': 'Delegation Parameters - Indexer Revenue',
        'policies': {
            'indexer_actions': indexer_actions
        },
        'variables': {
            'indexers': store_indexer_fee_cut
        },
    },        
    {
        'label': 'Revenue Process - Mint',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': mint_GRT,
        },
    },
    {
        'label': 'Revenue Process - Revenue to Pool',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': distribute_revenue_to_pool,   
        },
    },
    {
        'label': 'Revenue Process - Indexing Revenue',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': store_indexing_revenue,
        },
    },
    {
        'label': 'Revenue Process - Query Revenue',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': store_query_revenue, 
        },
    },
    {
        'label': 'Revenue Process - Non-Indexer Revenue',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': cumulative_non_indexer_revenue,
        },
    },
    {
        'label': 'Revenue Process - Indexer Revenue',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'indexers': distribute_revenue_to_indexer,
        },
    },                    
    {
        'label': 'Delegate',
        'policies': {
            'delegate_actions': delegate_actions,
        },
        'variables': {
            'indexers': delegate,
        },
    },
    {
        'label': 'Undelegate',
        'policies': {
            'undelegate_actions': undelegate_actions
        },
        'variables': {
            # 'pool_delegated_stake': subtract_undelegated_stake_from_pool,            
            'indexers': undelegate,
        },
    },    
    {
        'label': 'Withdraw',
        'policies': {
            'withdraw_actions': withdraw_actions
        },
        'variables': {
            'indexers': withdraw,
        },
    },        
    # {
    #     'label': 'Delegator Behaviors Bookkeeping',
    #     'policies': {
    #         'indexer_actions': indexer_actions
    #     },
    #     'variables': {
    #         # 'pool_delegated_stake': store_pool_delegated_stake,
    #         'shares': store_shares,
    #     },
    # },
]

