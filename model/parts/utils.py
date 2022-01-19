import pandas as pd
from decimal import *
import traceback
import sys
# pip install -U --pre eth-utils --no-deps
# import web3.main as web3
# from eth_utils import currency as web3
from eth_utils.currency import from_wei 
from pandas.core.accessor import delegate_names

"""
These are handled in eth calculations:
    shares
    tokens
    curationFees
    rebateFees
    delegationFees
    amount
"""

def convertFromLongStrToEth(d, field):
    for events in d.values():
        for event in events:                       
            # sometimes it comes in as a number, sometimes as a string
            event[field] = str(event[field])

            # put in a decimal place 18 chars from the right then convert to Decimal to avoid overflow error.
            try:
                if event[field] == 'nan':
                    event[field] = Decimal(0)
                else:                    
                    floatValue = float(event[field])
                    intValue = int(floatValue)                    
                    event[field] = from_wei(intValue, 'ether')
            except:
                print("Unexpected error:", traceback.format_exc())
                sys.exit()
                event[field] = Decimal(0)


def convertFromLongStrToDecimalPercent(d, field):
    # 1000000 is 100%
    # so divide by a million to get percent.
    for events in d.values():
        for event in events:                       
            # sometimes it comes in as a number, sometimes as a string
            event[field] = Decimal(event[field])

            # put in a decimal place 18 chars from the right then convert to Decimal to avoid overflow error.
            event[field] = event[field] / 1000000

def load_all_events(path, agent_event_path = None):
    df = load_all_events_to_pandas_df(path, agent_event_path)
    events_list_of_dicts = convert_pandas_df_to_list_of_dicts(df)
    return events_list_of_dicts

def load_all_events_to_pandas_df(path, agent_event_path = None):
    # make them ordered by blockNumber and logindex
    # squish them because time between doesn't matter
    # **but they have to be interleaved between all event types.
    # reset index
    # break back out to distinct types
    # use block number, resolve conflicts with log index.
    all_events = pd.read_csv(f'{path}')

    if agent_event_path:
        all_events = pd.concat([all_events, pd.read_csv(agent_event_path)])

    all_events.reset_index(inplace=True)
    all_events.sort_values(['blockNumber', 'logIndex'], ascending=[True, True])
    all_events = all_events.rename(columns={'index': 'timestep'})
    
    # start with timestep 1.
    all_events['timestep'] = all_events['timestep'] + 1
    all_events.set_index('timestep', inplace=True, drop=False)
    return all_events

def convert_df_to_dict(df):
    # print(events['timestep'])
    d = df.groupby(level=0).apply(lambda x: x.to_dict('records')).to_dict()
    

    convertFromLongStrToEth(d, 'tokens')
    # print(d)
    try:
        convertFromLongStrToEth(d, 'shares') 
        convertFromLongStrToEth(d, 'amount')            
        convertFromLongStrToEth(d, 'curationFees') 
        convertFromLongStrToEth(d, 'rebateFees') 
        convertFromLongStrToEth(d, 'delegationFees') 
        convertFromLongStrToDecimalPercent(d, 'indexingRewardCut')
        convertFromLongStrToDecimalPercent(d, 'queryFeeCut')
    except KeyError:
        print('KEYERROR!!!')
        pass
    return d

def convert_pandas_df_to_list_of_dicts(all_events):
    # print(all_events.loc[:, ['blockNumber', 'logIndex']])    

    # create a dict from the df where duplicate timesteps appear in a list of dicts under the same timestep index. 
    # NOTE: there should be no duplicates anymore.
    # TODO: Add rebateClaimed
    event_types = ['stakeDelegateds', 'stakeDelegatedLockeds', 'stakeDelegatedWithdrawns', 'allocationCloseds', 
                   'allocationCollecteds', 'stakeDepositeds', 'rewardsAssigneds', 'delegationParametersUpdateds',
                   'allocationCreateds']
    events_list_of_dicts = []
    for event_type in event_types:
        events = all_events[all_events['type'] == event_type]
        print(f'{event_type}: {len(events)} events')

        d = convert_df_to_dict(events)
        events_list_of_dicts.append(d)
    
    d = convert_df_to_dict(all_events)    

    # also append all_events so you can lookup by timestep, so you can set the current blockNumber
    events_list_of_dicts.append(d)
    
    print(f'TOTAL NUMBER OF EVENTS: {len(all_events)}')
    print(f'You should set SIMULATION_TIME_STEPS in config.py to a minimum of {len(all_events)} to capture all events.')
    print()
    return events_list_of_dicts

def is_agent_event_this_timestep(s, sL):
    if len(sL) >= 2:
        previous_injected_event_shift = sL[-2][-1]['injected_event_shift']
    else:
        previous_injected_event_shift = 0
    return s['injected_event_shift'] > previous_injected_event_shift


# get events for this timestep (should only be 1)
def get_shifted_events(s, sL, events_param, event_type=None):
    # increment by injected_event_shift to get real timestep.
    effective_timestep = s['timestep'] - s['injected_event_shift']
    
    if is_agent_event_this_timestep(s, sL):
        for indexer in s['indexers'].values():
            agent = indexer.delegators[1]
            if agent.output:
                output = agent.output[-1]
                if output['event'] == event_type:
                    events = agent.output 
                else:
                    events = None
    else:
        events = events_param.get(effective_timestep)
    
    return events


if __name__ == '__main__':
    event_path = 'another_indexer/single_indexer/singleIndexer_200events_a.csv'
    # event_path = 'multiple_indexer/multipleIndexer.csv'
    # event_path = 'multiple_indexer/allindexer/allEvents.csv'
    
    # agent_event_path = 'multiple_indexer/agent_events/agent_events.csv'
    agent_event_path = None

    delegation_events, undelegation_events, withdraw_events, rewards_assigned_events, \
            allocation_collected_events, stake_deposited_events, rewards_assigned_events, \
            delegation_parameter_events, \
            allocation_created_events, all_events = load_all_events(event_path, agent_event_path)
    # print(allocation_created_events)


