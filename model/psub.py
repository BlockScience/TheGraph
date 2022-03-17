from .parts.bookkeeping import *
from .parts.agent_behaviors import *
from .parts.revenue import *
from .parts.event_processor import *
from .parts.agent_slashing import *


psubs = [
    {
        'label': 'Initialization',
        'policies': {
        },
        'variables': {
        },
    },
    {
        'label': 'Bookkeeping',
        'policies': {
        },
        'variables': {
            'block_number': set_block_number,
            'epoch': set_epoch,
            'indexers': check_to_slash
        },
    },    
    {
        'label': 'Revenue Processing',
        'policies': {
            'revenue_amt': revenue_amt
        },
        'variables': {
            'indexers': revenue_process
        },
    },
    {
        'label': 'Event Processing',
        'policies': {
            'event_type': determine_event
        },
        'variables': {
            'indexers': indexer_process,
            'delegator_portfolios': portfolio_process
        }
    },
    {
        'label': 'Agent Actions',
        'policies': {
        },
        'variables': {
            'indexers': get_agent_actions_next_timestep,
        }

    },
    {
        'label': 'Increment agent event counter',
        'policies': {
        },
        'variables': {  # if there is an event in the hopper,
            'injected_event_shift': increment_timestep_due_to_agent_event
        }

    },
]

