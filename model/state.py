from model.model import delegator

# NOTE: shares and supply are used somewhat interchangeably.
# shares are supply owned by an individual
# and supply is the aggregate total.
genesis_state = {
    # NOTE: make these a parameter
    # NOTE: cannot import config because of circular import.
    "reserve": 10,  # money--this is only added to when a delegator buys shares
    "supply": 10,  # shares--this is only added to when a delegator buys shares
    # id=0 is the original provider of 10 reserve and owns 10 supply
    
    # TODO: use minimum_shares=params['initial_supply']
    "delegators": {0: delegator.Delegator(shares=10, minimum_shares=10)},
    "period_revenue": 0,  # this is passed directly to the delegators
    "spot_price": 2,
}
