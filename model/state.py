# from model.parts import delegator
from .parts.delegator import Delegator

# NOTE: shares and shares are used somewhat interchangeably.
# shares are shares owned by an individual
# and shares is the aggregate total.

GRT = 10000000.0 
DELEGATED = 10000
SHARES = 10000

LOCKED = 0
WITHDRAWN = 0

genesis_state = {
    # NOTE: make these a parameter
    # NOTE: cannot import config because of circular import.
    'total_delegated_stake': DELEGATED,  # money--this is only added to when a delegator buys shares
    "shares": SHARES,  # shares--this is only added to when a delegator buys shares
    # id=0 is the original provider of 10 total_delegated_stake and owns 10 shares
    
    # TODO: use minimum_shares=params['s_del']
    "delegators": {0: Delegator(shares=10, minimum_shares=10)},
    "period_revenue": 0,  # this is passed directly to the delegators
    "spot_price": 2,
    'GRT': GRT,
    'Locked': LOCKED,
    'Withdrawn': WITHDRAWN,

    
}
