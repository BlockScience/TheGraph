


# from .parts.add_delegator import instantiate_delegate, should_instantiate_delegate

from .parts.delegator_behaviors import (delegate, undelegate, withdraw,
                                        may_act_this_timestep, delegator_action,
                                        account_for_tax)

from .parts.revenue import (revenue_amt, distribute_revenue_to_delegators, 
                            mint_GRT, distribute_revenue_to_pool)

# from .parts.private_price import compute_and_store_private_prices

from .parts.delegator_behaviors_bookkeeping import (store_pool_delegated_stake,
                                                    store_shares, increment_epoch)


psubs = [
    {
        'label': 'Revenue Process',
        'policies': {
            'revenue_amt': revenue_amt, # indexing and query rewards 
        },
        'variables': {
            'GRT': mint_GRT,
            'delegators': distribute_revenue_to_delegators,
            'pool_delegated_stake': distribute_revenue_to_pool,    
        },
    },
    {
        'label': 'Delegate',
        'policies': {
            'delegator_action': delegator_action
        },
        'variables': {
            'delegators': delegate,
            'GRT': account_for_tax,
        },
    },
    {
        'label': 'Undelegate',
        'policies': {
            'delegator_action': delegator_action
        },
        'variables': {
            'delegators': undelegate,
        },
    },    
    {
        'label': 'Withdraw',
        'policies': {
            'delegator_action': delegator_action
        },
        'variables': {
            'delegators': withdraw,
        },
    },        
    {
        'label': 'Delegator Behaviors Bookkeeping',
        'policies': {
        },
        'variables': {
            'pool_delegated_stake': store_pool_delegated_stake,
            'shares': store_shares,
            'epoch': increment_epoch,
        },
    },
]

