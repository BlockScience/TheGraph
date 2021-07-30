# from model.parts import delegator
from .parts.delegator import Delegator
from decimal import Decimal

initial_shares = 1243612
initial_stake = Decimal(1243612)
""" System state/state of the delegation pool for one indexer. """
genesis_state = {
    # NOTE: make these a parameter
    # NOTE: cannot import config because of circular import.
    # D
    'pool_delegated_stake': initial_stake,  # amount of GRT delegated to the indexer
    
    # L
    'pool_locked_stake': 0,  # amount of GRT locked in undelegation process.  these are NO LONGER in the delegated pool and also not owned by delegator yet.
    
    # S
    "shares": initial_shares,  # shares--this is only added to when a delegator delegates
    
    # id=0 is the original provider of 10 pool_delegated_stake and owns 10 shares    
    # TODO: use minimum_shares=params['s_del']
    "delegators": {'indexer': Delegator(id='indexer', shares=initial_shares, delegated_tokens=initial_stake)},
    "period_revenue": 0,  # this is passed directly to the delegators
    'GRT': 10000000,
    'indexing_revenue': 0,
    'query_revenue': 0,
    'indexer_revenue': 0,
    "epoch": 0,
    
}
