# from .config import .
from model import Delegator

genesis_state = {
    # NOTE: make these a parameter
    "reserve": 10,
    "supply": 10,
    # 0 is the original provider of 10 reserve and owns 10 supply
    "delegates": {0: Delegator()},
    "period_revenue": 0,
    "spot_price": 0,    
}
