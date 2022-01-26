from .delegator_behaviors import *
from .indexer_behaviors import *
from .portfolio_behaviors import *
from .subgraph_behaviors import *
from .utils import *


def determine_event(params, step, sL, s):
    # timestep = s['timestep']
    # effective_timestep = s['timestep'] - s['injected_event_shift']
    # event = params['all_events'].get(effective_timestep)

    event = get_shifted_event(s, sL, params['all_events'])

    event_type = {'event_type': str(),
                  'event': dict()}
    if event[0]['type'] == 'stakeDelegateds':
        event_type['event_type'] = 'stakeDelegateds'
        event_type['event'] = event
    elif event[0]['type'] == 'stakeDelegatedLockeds':
        event_type['event_type'] = 'stakeDelegatedLockeds'
        event_type['event'] = event
    elif event[0]['type'] == 'stakeDepositeds':
        event_type['event_type'] = 'stakeDepositeds'
        event_type['event'] = event
    elif event[0]['type'] == 'delegationParametersUpdateds':
        event_type['event_type'] = 'delegationParametersUpdateds'
        event_type['event'] = event[0]
    elif event[0]['type'] == 'stakeDelegatedWithdrawns':
        event_type['event_type'] = 'stakeDelegatedWithdrawns'
        event_type['event'] = event
    elif event[0]['type'] == 'allocationCreateds':
        event_type['event_type'] = 'allocationCreateds'
        event_type['event'] = event
    elif event[0]['type'] == 'allocationCloseds':
        event_type['event_type'] = 'allocationCloseds'
        event_type['event'] = event

    return event_type


def indexer_process(params, step, sL, s, inputs):
    event = inputs['event_type']
    if event == 'stakeDelegateds':
        return delegate(params, step, sL, s, inputs)
    elif event == 'stakeDelegatedLockeds':
        return undelegate(params, step, sL, s, inputs)
    elif event == 'stakeDepositeds':
        return cumulative_deposited_stake(params, step, sL, s, inputs)
    elif event == 'delegationParametersUpdateds':
        return store_delegation_parameters(params, step, sL, s, inputs)
    elif event == 'stakeDelegatedWithdrawns':
        return withdraw(params, step, sL, s, inputs)
    elif event == 'allocationCreateds':
        return create_allocations(params, step, sL, s, inputs)
    elif event == 'allocationCloseds':
        return close_allocations(params, step, sL, s, inputs)

    return 'indexers', s['indexers']


def portfolio_process(params, step, sL, s, inputs):
    event = inputs['event_type']
    if event == 'stakeDelegateds':
        return delegate_portfolio(params, step, sL, s, inputs)
    elif event == 'stakeDelegatedLockeds':
        return undelegate_portfolio(params, step, sL, s, inputs)
    elif event == 'stakeDelegatedWithdrawns':
        return withdraw_portfolio(params, step, sL, s, inputs)

    return 'delegator_portfolios', s['delegator_portfolios']