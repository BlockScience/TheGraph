from .utils import is_agent_event_this_timestep


def set_block_number(params, step, sL, s, inputs):
    key = 'block_number'
    effective_timestep = s['timestep'] - s['injected_event_shift']
    all_events = params['all_events']
    if is_agent_event_this_timestep(s, sL):
        print('---INJECTING AGENT EVENT HERE')
        value = s['block_number']
    else:
        event = all_events.get(effective_timestep)[0]
        value = event['blockNumber']
    return key, value


def set_epoch(params, step, sL, s, inputs):
    key = 'epoch'
    effective_timestep = s['timestep'] - s['injected_event_shift']
    all_events = params['all_events']
    
    if is_agent_event_this_timestep(s, sL):        
        value = s['epoch']
    else:
        event = all_events.get(effective_timestep)[0]
        value = int((event['blockNumber'] - params['shift']) / params['blocks_per_epoch'])
    return key, value

def increment_timestep_due_to_agent_event(params, step, sL, s, inputs):
    key = 'injected_event_shift'
    
    injected_event_shift = s['injected_event_shift']
    for indexer in s['indexers'].values():
        if indexer.delegators[1].output:
            injected_event_shift += 1
            # TODO: if multiple front runners inject events at the same time, this won't work.
            break
        
    return key, injected_event_shift

