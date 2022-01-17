def set_block_number(params, step, sL, s, inputs):
    key = 'block_number'
    timestep = s['timestep']
    all_events = params['all_events']
    event = all_events.get(timestep)[0]
    value = event['blockNumber']
    return key, value

def set_epoch(params, step, sL, s, inputs):
    key = 'epoch'
    timestep = s['timestep']
    all_events = params['all_events']
    event = all_events.get(timestep)[0]
    value = int((event['blockNumber'] - params['shift']) / params['blocks_per_epoch'])
    return key, value

def increment_timestep_due_to_agent_event(params, step, sL, s, inputs):
    key = 'injected_event_shift'
    
    injected_event_shift = s['injected_event_shift']
    if s['agents'][0].output:
        injected_event_shift += 1

    # agent = s['agents'][0]
    return key, injected_event_shift

