from .parts.indexer_behaviors import *                                      
from .parts.delegator_behaviors import *
from .parts.subgraph_behaviors import *
from .parts.revenue import *
from .parts.portfolio_behaviors import *
from .parts.bookkeeping import *
from .parts.agent_behaviors import *
from .parts.revenue_rewrite import *
from .parts.event_processor import *


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
            # 'set_event_list': set_event_list,
            'block_number': set_block_number,
            'epoch': set_epoch
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
    }
]

