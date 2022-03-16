from model.parts.delegate_front_runner import DelegateFrontRunner
from model.parts.delegate_front_runner_rules import DelegateFrontRunnerRules
from model.parts.index_spoofer import IndexSpoofer
from model.parts.index_spoofer_rules import IndexSpoofingRules
from .sys_params import params

initial_account_balance = params['delegator_initial_holdings'][0]
index_account_balance = params['indexer_initial_holdings'][0]
indexer_rules = IndexSpoofingRules(index_account_balance, 1, 5)

rules = DelegateFrontRunnerRules(initial_account_balance)
""" System state/state of the delegation pool for multiple indexers. """
genesis_state = {
    'indexers': {1: IndexSpoofer(1, indexer_rules, index_account_balance)},
    # 'agents': [DelegateFrontRunner(1, rules, initial_account_balance)],
    'delegator_portfolios': {},
    'block_number': 0,
    'epoch': 0,
    'injected_event_shift': 0
}
