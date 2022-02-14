# from model.parts import delegator
from .parts.delegator import Delegator
from .parts.indexer import Indexer
from decimal import Decimal

initial_shares = 0
initial_stake = Decimal(0)
# id_indexer = "indexer"

""" System state/state of the delegation pool for multiple indexers. """
genesis_state = {
    'indexers': {},
    'delegator_portfolios': {},
    'block_number': 0    
}
