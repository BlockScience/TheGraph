# from model.parts import delegator
from model.parts import delegate_front_runner
from .parts.delegator import Delegator
from .parts.indexer import Indexer
from decimal import Decimal

initial_shares = 0
initial_stake = Decimal(0)
# id_indexer = "indexer"

""" System state/state of the delegation pool for multiple indexers. """
genesis_state = {
    'indexers': {},
    # 'agents': [delegate_front_runner.DelegateFrontRunner()],
    'delegator_portfolios': {},
    'block_number': 0,
    'injected_event_shift': 0
}
