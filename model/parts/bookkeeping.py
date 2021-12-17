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

