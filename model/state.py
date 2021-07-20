# from model.parts import delegator
from .parts.delegator import Delegator

""" System state/state of the delegation pool for one indexer. """
genesis_state = {
    # NOTE: make these a parameter
    # NOTE: cannot import config because of circular import.
    'total_delegated_stake': 0,  # money--this is only added to when a delegator delegates
    "shares": 0,  # shares--this is only added to when a delegator delegates
    # id=0 is the original provider of 10 total_delegated_stake and owns 10 shares
    
    # TODO: use minimum_shares=params['s_del']
    "delegators": {0: Delegator(shares=10, minimum_shares=10)},
    "period_revenue": 0,  # this is passed directly to the delegators
    "spot_price": 2,
    'GRT': 10000000,
    'locked_delegatedstake': 0,
    'withdrawn_delegatedstake': 0,
    'indexing_revenue': 0,
    'query_revenue': 0,
    'indexer_revenue': 0,
    
}
