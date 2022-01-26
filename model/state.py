from model.parts.delegate_front_runner import DelegateFrontRunner
from model.parts.delegate_front_runner_rules import DelegateFrontRunnerRules
from .sys_params import params

initial_account_balance = params['delegator_initial_holdings'][0]

rules = DelegateFrontRunnerRules(initial_account_balance)
""" System state/state of the delegation pool for multiple indexers. """
genesis_state = {
    'indexers': {},
    # 'agents': [DelegateFrontRunner(1, rules, initial_account_balance)],
    'delegator_portfolios': {},
    'block_number': 0,
    'epoch': 0,
    'injected_event_shift': 0
}
