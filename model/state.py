from model.parts.utility_delegator import UtilityDelegator
from model.parts.utility_components_delegator import UtilityComponentsDelegator
from .sys_params import params

initial_account_balance = params['delegator_initial_holdings'][0]
amount_to_delegate = 1000000
opportunity_cost = params['opportunity_cost'][0]
components = UtilityComponentsDelegator(amount_to_delegate, opportunity_cost)

# rules = DelegateFrontRunnerRules(initial_account_balance)
""" System state/state of the delegation pool for multiple indexers. """
genesis_state = {
    'indexers': {},
    'delegator_portfolios': {1: UtilityDelegator(1, initial_account_balance, components)},  # delegator_porfolios is the delegator information that is stored across all indexers
    'block_number': 0,
    'epoch': 0,
    'injected_event_shift': 0
}
