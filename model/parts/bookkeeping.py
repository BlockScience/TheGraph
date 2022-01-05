def set_block_number(params, step, sL, s, inputs):
    key = 'block_number'
    
    timestep = s['timestep']
    print(f'{timestep=}')
    
    all_events = params['all_events']
    # print(f'{all_events=}')

    event = all_events.get(timestep)[0]
    print(f'{event["blockNumber"]=}')
    value = event['blockNumber']
    return key, value


def increment_timestep_due_to_agent_event(params, step, sL, s, inputs):
    # TODO: perhaps only do this when we have an agent event.
    key = 'injected_event_shift'
    injected_event_shift = s['injected_event_shift']
    agent = s['agents'][0]
    return injected_event_shift + 1

