# from .behavior import update_a

from .model.allocate_payments import (allocated_funds, unallocated_funds,
                                      check_brokers,
                                      allocate_funds_to_member_brokers
                                      )

from .model.leaves import (should_leaves, leaves,
                           decrement_allocated_funds_due_to_leaves,
                           increment_unallocated_funds_due_to_forfeit_stake,
                           allowed_to_leave)

from .model.add_delegator import instantiate_delegate, should_instantiate_delegate

from .model.helper_functions import count_brokers

from .model.claims import (should_make_claims, make_claims,
                           decrement_allocated_funds_by_claims)

from .model.bookkeeping import update_time_attached, total_broker_stake

from .model.revenue import revenue_amt, store_revenue, distribute_revenue



psubs = [
    {
        'label': 'Update Time Attached',
        'policies': {
        },
        'variables': {
            'delegators': update_time_attached  # helpful for vesting
        }
    },
    {
        'label': 'Revenue Arrival Process',
        'policies': {
            'revenue_amt': revenue_amt  # how much is paid in.
        },
        'variables': {
            'revenue': store_revenue
        },
    },
    {
        'label': 'Distribute Revenue',
        'policies': {
        },
        'variables': {
            'delegators': distribute_revenue,
        }
    },
    {
        # if there's a vacant spot, flip a coin
        # (heads, they join, tails nobody joins)
        'label': 'Add Delegator',
        'policies': {
            'should_join': should_instantiate_delegate
            },
        'variables': {
            'delegators': instantiate_delegate,
            },
    },
    {
        'label': 'Delegator Behaviors',
        'policies': {
            # outputs ordered list of acting delegatorIds this timestep
            'may_act_this_timestep': may_act_this_timestep  
        },
        'variables': {
            'delegators': act,
        },
    },
    {
        'label': 'Allowed to Leave',
        'policies': {},
        'variables': {
            'brokers': allowed_to_leave
        },
    },
    {
        'label': 'Leaves',
        'policies': {
            'should_leaves': should_leaves
            },
        'variables': {
            'brokers': leaves,
            'allocated_funds': decrement_allocated_funds_due_to_leaves,
            'unallocated_funds': increment_unallocated_funds_due_to_forfeit_stake,
            'num_member_brokers': count_brokers
            }
    },
    {
        'label': 'Bookkeeping',
        'policies': {
        },
        'variables': {
            'total_broker_stake': total_broker_stake,
            'brokers': update_time_attached
        }

    }
]
