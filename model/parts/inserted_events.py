def insert_delegation_event(params, step, sL, s):
    timestep = s['timestep']
    delegation_events = params['delegation_tokens_events'].get(timestep)
    return {'inserted_delegation_events': delegation_events}
