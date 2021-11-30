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

def convertFromLongStrToEth(d, field, GRT_conversion_rate):
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
                    # intValue = int(event[field])
                    event[field] = from_wei(intValue, 'ether')
            except:
                print("Unexpected error:", traceback.format_exc())
                sys.exit()
                event[field] = Decimal(0)

# def convertFromLongStrToDecimal(d, field, GRT_conversion_rate):
#     for events in d.values():
#         for event in events:                       
#             # sometimes it comes in as a number, sometimes as a string
#             event[field] = str(event[field])

#             # put in a decimal place 18 chars from the right then convert to Decimal to avoid overflow error.
#             try:
#                 if event[field] == 'nan':
#                     event[field] = Decimal(0)
#                 else:
#                     strValue = event[field][:len(event[field]) - -GRT_conversion_rate] + "." + event[field][GRT_conversion_rate:]
#                     # print(strValue)
#                     event[field] = Decimal(strValue)
#             except:
#                 print(f'{field=}')
#                 print(f'{event=}')

#                 print("Unexpected error:", sys.exc_info()[0])
#                 sys.exit()
#                 event[field] = Decimal(0)


def convertFromLongStrToDecimalPercent(d, field):
    # 1000000 is 100%
    # so divide by a million to get percent.
    for events in d.values():
        for event in events:                       
            # sometimes it comes in as a number, sometimes as a string
            event[field] = Decimal(event[field])

            # put in a decimal place 18 chars from the right then convert to Decimal to avoid overflow error.
            event[field] = event[field] / 1000000

def load_all_events(path, agent_event_path = None, GRT_conversion_rate = -18):
    df = load_all_events_to_pandas_df(path, agent_event_path, GRT_conversion_rate)
    events_list_of_dicts = convert_pandas_df_to_list_of_dicts(df)
    return events_list_of_dicts

def load_all_events_to_pandas_df(path, agent_event_path = None, GRT_conversion_rate = -18):
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
    
def convert_pandas_df_to_list_of_dicts(all_events, GRT_conversion_rate = -18):
    # print(all_events.loc[:, ['blockNumber', 'logIndex']])    

    # create a dict from the df where duplicate timesteps appear in a list of dicts under the same timestep index. 
    # NOTE: there should be no duplicates anymore.
    event_types = ['stakeDelegateds', 'stakeDelegatedLockeds', 'stakeDelegatedWithdrawns', 'allocationCloseds', 
                   'allocationCollecteds', 'stakeDepositeds', 'rewardsAssigneds', 'delegationParametersUpdateds',
                   'allocationCreateds']
    events_list_of_dicts = []
    for event_type in event_types:
        events = all_events[all_events['type'] == event_type]
        print(f'{event_type}: {len(events)} events')
        # print(events['timestep'])
        d = events.groupby(level=0).apply(lambda x: x.to_dict('records')).to_dict()
        

        convertFromLongStrToEth(d, 'tokens', GRT_conversion_rate)
        # print(d)
        try:
            convertFromLongStrToEth(d, 'shares', GRT_conversion_rate) 
            convertFromLongStrToEth(d, 'amount', GRT_conversion_rate)            
            convertFromLongStrToEth(d, 'curationFees', GRT_conversion_rate) 
            convertFromLongStrToEth(d, 'rebateFees', GRT_conversion_rate) 
            convertFromLongStrToEth(d, 'delegationFees', GRT_conversion_rate) 
            convertFromLongStrToDecimalPercent(d, 'indexingRewardCut')
            convertFromLongStrToDecimalPercent(d, 'queryFeeCut')
        except KeyError:
            print('KEYERROR!!!')
            pass
        events_list_of_dicts.append(d)
    print(f'TOTAL NUMBER OF EVENTS: {len(all_events)}')
    print(f'You should set SIMULATION_TIME_STEPS in config.py to a minimum of {len(all_events)} to capture all events.')
    print()
    return events_list_of_dicts


# def load_delegation_event_sequence_from_csv(path, blockNumberShift = 11474307, blocksPerEpoch = 6500, limit = None, GRT_conversion_rate = -18):
#     df = pd.read_csv(path)
#     # limit number of records read in 
#     if limit is not None:
#         df = df.head(limit)
#     else:
#         pass
#     # print(f'loading {path}...')
    
#     df['timestep'] = (df.blockNumber - blockNumberShift) / blocksPerEpoch + 1
#     df.timestep = df.timestep.astype(int)
    
#     # set the index to timestep inplace and don't drop timestep from the df.
#     df.set_index('timestep', inplace=True, drop=False)

#     # create a dict from the df where duplicate timesteps appear in a list of dicts under the same timestep index.
#     d = df.groupby(level=0).apply(lambda x: x.to_dict('records')).to_dict()
#     # print(f'{d=}')
    
#     convertFromLongStrToDecimal(d, 'tokens', GRT_conversion_rate)
#     try:
#         convertFromLongStrToDecimal(d, 'shares', GRT_conversion_rate) 
#         convertFromLongStrToDecimal(d, 'amount', GRT_conversion_rate)
#     except KeyError:
#         pass
#     # d['tokens'] = d['tokens'].apply(lambda x: int(x) * GRT_conversion_rate)
#     print(f'loaded {path}.')
#     return d
    

# def total_stake_deposited(stake_deposited_events):
#     total = 0
#     if stake_deposited_events:
#         for stake_deposited_event in stake_deposited_events:
#             total += stake_deposited_event['tokens']    
#     return total

if __name__ == '__main__':
    event_path = 'another_indexer/single_indexer'
    # event_path = 'multiple_indexer/multipleIndexer.csv'
    # event_path = 'multiple_indexer/allindexer/allEvents.csv'
    
    # agent_event_path = 'multiple_indexer/agent_events/agent_events.csv'
    agent_event_path = None

    delegation_events, undelegation_events, withdraw_events, rewards_assigned_events, \
            allocation_collected_events, stake_deposited_events, rewards_assigned_events, \
            delegation_parameter_events, \
            allocation_created_events = load_all_events(event_path, agent_event_path)
    print(allocation_created_events)


