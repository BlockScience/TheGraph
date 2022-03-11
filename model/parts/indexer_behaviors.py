from . import utils
from .indexer import Indexer
# from .utils import get_shifted_events

""" this just gets all of the events at this timestep into policy variables """
# def get_stake_deposited_events(params, step, sL, s):
#     # who delegates,
#     # how many tokens.
#     timestep = s['timestep']
#     effective_timestep = s['timestep'] - s['injected_event_shift']
#     print(f'\n{timestep=} beginning...')
#     print(f'\n{effective_timestep=} beginning...')
#
#     key = 'stake_deposited_events'
#     events = get_shifted_events(s, sL, params[key])
#     return {key: events}




""" this just gets all of the events at this timestep into policy variables """
# def get_delegation_parameter_events(params, step, sL, s):
#     key = 'delegation_parameter_events'
#     events = get_shifted_events(s, sL, params[key])
#     return {key: events}


def cumulative_deposited_stake(params, step, sL, s, inputs):
    key = 'indexers'
    event = inputs['event'][0] if inputs['event'][0] is not None else None
    indexers = s['indexers']

    if event:
        indexer_id = event['indexer']
        if indexer_id not in indexers:
            indexers[indexer_id] = Indexer(indexer_id)
        indexer = indexers[indexer_id]
        indexer.cumulative_deposited_stake += event['tokens']
        indexer.initial_stake_deposited = True
        print(f'''EVENT: STAKE DEPOSITED: 
            {indexer.id=},
            {event["tokens"]=}''')
        indexer.GRT -= event['tokens']

    value = indexers
    return key, value

def store_delegation_parameters(params, step, SL, s, inputs):
    key = 'indexers'
    indexers = s[key]
    print(inputs)

    event = inputs['event'] if inputs['event'] is not None else []
    # print(f'store_query_fee_cut {delegation_parameter_events=}')
    if event:
        indexer_id = event['indexer']
        if indexer_id not in indexers:
            indexers[indexer_id] = Indexer(indexer_id)
        indexer = indexers[indexer_id]

        print(f'''EVENT: DELEGATION PARAMETERS UPDATE (before)--
                {indexer.id=}
                {indexer.query_fee_cut=}
                {indexer.indexer_revenue_cut=}
        ''')
        indexer.query_fee_cut = event['queryFeeCut']
        indexer.indexer_revenue_cut = event['indexingRewardCut']
        print(f'''EVENT: DELEGATION PARAMETERS UPDATE (after)--
                {indexer.id=}
                {indexer.query_fee_cut=}
                {indexer.indexer_revenue_cut=}
        ''')

    value = indexers
    return key, value
    
