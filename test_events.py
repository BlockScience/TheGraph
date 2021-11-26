import pandas as pd
import numpy as np

# import os
# import sys
# module_path = os.path.abspath(os.path.join('..'))
# print(module_path)
# sys.path.append(module_path)
# from .model.parts.utils import *
# import model.parts.utils
from model.sys_params import *


df = pd.read_pickle(r'experiment.p')
df.reset_index(inplace = True)
pd.set_option('display.max_rows', None)

def test_delegation(debug):
    delegation_events_dict = delegation_events
    if debug:        
        print("EXPECTED TRUTH FROM DELEGATION EVENTS:")
        for timestep, events in delegation_events_dict.items():
            for event in events:        
                print(f"{timestep}, {event['delegator']}, {event['shares']}")

    if debug:
        print("MODELED RESULTS")
    delegation_event_shares = {}
    for timestep, events in delegation_events_dict.items():
        for event in events:
            # curTimestepShares = df.iloc[timestep-1].delegators[event['delegator']].shares
            curTimestepShares = df.iloc[timestep-1].indexers[event['indexer']].delegators[event['delegator']].shares
            try:
                # lastTimestepShares = df.iloc[timestep-2].delegators[event['delegator']].shares
                lastTimestepShares = df.iloc[timestep-2].indexers[event['indexer']].delegators[event['delegator']].shares
            except:
                lastTimestepShares = 0
            deltaShares = curTimestepShares - lastTimestepShares
            delegation_event_shares[timestep] = deltaShares
            if debug:
                print(f"{timestep}, {event['delegator']}, {delegation_event_shares[timestep]}")

    if debug:
        print("UNITTEST RESULTS")
    cntExact = 0
    cntReallyClose = 0
    cntClose = 0
    cnt = 0
    cntWrong = 0
    for timestep, events in delegation_events_dict.items():
        for event in events:
            # curTimestepShares = df.iloc[timestep-1].delegators[event['delegator']].shares
            curTimestepShares = df.iloc[timestep-1].indexers[event['indexer']].delegators[event['delegator']].shares
            try:
                # lastTimestepShares = df.iloc[timestep-2].delegators[event['delegator']].shares
                lastTimestepShares = df.iloc[timestep-2].indexers[event['indexer']].delegators[event['delegator']].shares
            except:
                # this is a new delegator.
                lastTimestepShares = 0
            deltaShares = curTimestepShares - lastTimestepShares

            if debug:
                print(f"Event: Timestep={timestep}, Delegator ID={event['delegator']}, Shares Granted={event['shares']}")
                print(f"Model: Timestep={timestep}, Delegator ID={event['delegator']}, Shares Granted={deltaShares}")
            
            try:
                ratio = abs(event['shares'] / deltaShares)
            except:
                ratio = np.inf
            exact = ratio == 1.0
            close = 0.99 <= ratio <= 1.01
            reallyClose = 0.99999 <= ratio <= 1.00001

            if exact:            
                cntExact += 1
            elif reallyClose:
                cntReallyClose += 1
            elif close:
                cntClose += 1
            else:
                cntWrong += 1
            cnt += 1
            if debug:
                print("Shares Equal?", exact)
                print("Shares Within 0.001%?", reallyClose)
                print("Shares Within 1%?", close)
                print(f"Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   
                print()
    print(f"Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   

def test_undelegation(debug):
    undelegation_events_dict = undelegation_events
    if debug:
        print("EXPECTED TRUTH--Tokens locked from undelegation events:")
        for timestep, events in undelegation_events_dict.items():
            print(f"{timestep}, {events[0]['delegator']}, {events[0]['tokens']}")
    
    if debug:
        print("MODELED RESULTS--Tokens locked in undelegation.")
    
    undelegation_tokens = {}
    for timestep, events in undelegation_events_dict.items():
        event = events[0]
        new_tokens = df.iloc[timestep-1].indexers[event['indexer']].delegators[event['delegator']].undelegated_tokens 
        old_tokens = df.iloc[timestep-2].indexers[event['indexer']].delegators[event['delegator']].undelegated_tokens
        undelegation_tokens[timestep] = new_tokens - old_tokens
        if debug:
            print(f"{timestep}, {events[0]['delegator']}, {undelegation_tokens[timestep]}")

    if debug:
        print("UNITTEST RESULTS")
    cntExact = 0
    cntReallyClose = 0
    cntClose = 0
    cnt = 0
    cntWrong = 0
    for timestep, event in undelegation_events_dict.items():
        if debug:
            print(f"Event: Timestep={timestep}, Delegator ID={event[0]['delegator']}, Tokens Undelegated={event[0]['tokens']}")
            print(f"Model: Timestep={timestep}, Delegator ID={event[0]['delegator']}, Tokens Undelegated={undelegation_tokens[timestep]}")
        try:
            ratio =  abs(event[0]['tokens'] / undelegation_tokens[timestep])
        except:
            ratio = np.inf
        exact = ratio == 1.0
        close = 0.99 <= ratio <= 1.01
        reallyClose = 0.99999 <= ratio <= 1.00001

        if exact:            
            cntExact += 1
        elif reallyClose:
            cntReallyClose += 1
        elif close:
            cntClose += 1
        else:
            cntWrong += 1
        cnt += 1
        if debug:
            print("Tokens Equal?", exact)
            print("Tokens Within 0.001%?", reallyClose)
            print("Tokens Within 1%?", close)
            print(f"Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   
            print()
    print(f"Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   
        

if __name__ == '__main__':
    print("UNITTEST RESULTS")
    debug = False
    test_delegation(debug=debug)
    test_undelegation(debug=debug)


