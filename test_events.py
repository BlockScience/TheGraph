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
max_timestep = len(df)

def test_delegation(debug):
    delegation_events_dict = {i:j for (i, j) in delegation_events.items() if i < max_timestep}
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
    print(f"Delegation | Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   

def test_undelegation(debug):
    undelegation_events_dict = {i:j for (i, j) in undelegation_events.items() if i < max_timestep}
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
    print(f"Undelegation | Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   


def test_withdraw(debug):
    withdraw_events_dict = {i:j for (i, j) in withdraw_events.items() if i < max_timestep}

    if debug:
        print("EXPECTED TRUTH--Tokens withdrawn via withdraw events:")
        for timestep, withdraw_event in withdraw_events_dict.items():
            print(f"{timestep}, {withdraw_event[0]['delegator']}, {withdraw_event[0]['tokens']}")
    
        print("MODELED RESULTS--Tokens locked in undelegation.")
        for timestep, withdraw_event in withdraw_events_dict.items():
            event = withdraw_event[0]
            new_tokens_withdrawn = df.iloc[timestep-1].indexers[event['indexer']].delegators[event['delegator']].holdings
            old_tokens_withdrawn = df.iloc[timestep-2].indexers[event['indexer']].delegators[event['delegator']].holdings
            tokens_withdrawn = new_tokens_withdrawn - old_tokens_withdrawn
            print(f"{timestep}, {withdraw_event[0]['delegator']}, {tokens_withdrawn=}")
    
    if debug:
        print("UNITTEST RESULTS")
    cntExact = 0
    cntReallyClose = 0
    cntClose = 0
    cnt = 0
    cntWrong = 0
    for timestep, withdraw_event in withdraw_events_dict.items():
        event = withdraw_event[0]
        new_tokens_withdrawn = df.iloc[timestep-1].indexers[event['indexer']].delegators[event['delegator']].holdings
        old_tokens_withdrawn = df.iloc[timestep-2].indexers[event['indexer']].delegators[event['delegator']].holdings
        tokens_withdrawn = new_tokens_withdrawn - old_tokens_withdrawn
        if debug:
            print(f"Event: Timestep={timestep}, Delegator ID={event['delegator']}, Tokens Withdrawn={event['tokens']}")
            print(f"Model: Timestep={timestep}, Delegator ID={event['delegator']}, Tokens Withdrawn={tokens_withdrawn}")
        # print("Withdraw Amount Equal?", event[0]['tokens'] == tokens_withdrawn)
        # print()
        try:
            ratio =  abs(event['tokens'] / tokens_withdrawn)
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
    print(f"Withdraw | Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   

def test_rewards_assigned(debug):
    if debug:    
        print("EXPECTED TRUE INDEXING REWARDS FROM REWARDS ASSIGNED EVENTS:")
        for timestep, rewards_assigned_events_list in rewards_assigned_events.items():
            if rewards_assigned_events_list is None:
                indexing_fee_amt = 0
            else:
                indexing_fee_amt = sum([e['amount'] for e in rewards_assigned_events_list])        
            print(indexing_fee_amt)
            # print(f"{timestep}, {stake_deposited_event[0]['tokens']}")
        
    if debug:
        print("MODELED RESULTS")
    # TODO: weave in indexer_revenue_cut events
    # indexer #1
    # indexer_revenue_cut = 0.89
    # indexer #2
    indexer_revenue_cut = Decimal(0.8)
    # print(df.iloc[timestep])
    # is_first = True
    rewards_assigned_modeled = {}
    rewards_assigned_dict = {i:j for (i, j) in rewards_assigned_events.items() if i < max_timestep}
    for timestep, stake_deposited_event in rewards_assigned_dict.items():
        # back indexing rewards out from increase in pool_delegated_stake / 0.11 * 0.89
        event = stake_deposited_event[0]
        new_rewards_assigned = df.iloc[timestep-1].indexers[event['indexer']].pool_delegated_stake
        old_rewards_assigned = df.iloc[timestep-2].indexers[event['indexer']].pool_delegated_stake
        rewards_assigned =(new_rewards_assigned - old_rewards_assigned) / (1 - indexer_revenue_cut) 
        rewards_assigned_modeled[timestep] = rewards_assigned
        if debug:
            print(f"{timestep}, {rewards_assigned=}")
            
    if debug:
        print("UNITTEST RESULTS")
    # print(rewards_assigned_events)
    cntExact = 0
    cntReallyClose = 0
    cntClose = 0
    cnt = 0
    cntWrong = 0
    for timestep, rewards_assigned_event in rewards_assigned_dict.items():
        # back indexing rewards out from increase in pool_delegated_stake / 0.11 * 0.89
        modeled_rewards_assigned = rewards_assigned_modeled[timestep]
        event_rewards_assigned = rewards_assigned_event[0]['amount']
        if debug:
            print(f"Event: Timestep={timestep}, Indexing Reward Tokens={event_rewards_assigned}")
            print(f"Model: Timestep={timestep}, Indexing Reward Tokens={modeled_rewards_assigned}")
        # print("Tokens Within 1%?", 0.99 <= abs(event_rewards_assigned / modeled_rewards_assigned) <= 1.01)
        # print()
        try:
            ratio = abs(modeled_rewards_assigned / event_rewards_assigned)
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
    print(f"Indexing Rewards | Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")           

def test_allocation_collecteds(debug):
    allocation_collected_events_dict = {i:j for (i, j) in allocation_collected_events.items() if i < max_timestep}
    
    if debug:

        print("EXPECTED TRUE QUERY REWARDS FROM STAKE DEPOSITED EVENTS:")
        for timestep, allocation_collected_events_list in allocation_collected_events_dict.items():
            if allocation_collected_events_list is None:
                query_fee_amt = 0
            else:
                query_fee_amt = sum([e['tokens'] for e in allocation_collected_events_list])
            print(f"{timestep}, {query_fee_amt}")
    
    if debug:
        print("MODELED RESULTS")
        for timestep, allocation_collected_events_list in allocation_collected_events_dict.items():    
            event = allocation_collected_events_list[0]
            new_query_fee_amt = df.iloc[timestep-1].indexers[event['indexer']].cumulative_query_revenue
            old_query_fee_amt = df.iloc[timestep-2].indexers[event['indexer']].cumulative_query_revenue
            query_fee_amt = new_query_fee_amt - old_query_fee_amt
            print(f"{timestep}, {query_fee_amt=}")

    if debug:
        print("UNITTEST RESULTS")
    cntExact = 0
    cntReallyClose = 0
    cntClose = 0
    cnt = 0
    cntWrong = 0
    for timestep, allocation_collected_events_list in allocation_collected_events_dict.items():
        if allocation_collected_events_list is None:
            event_query_fee_amt = 0
        else:
            event_query_fee_amt = sum([e['tokens'] for e in allocation_collected_events_list])
        event = allocation_collected_events_list[0]
        new_query_fee_amt = df.iloc[timestep-1].indexers[event['indexer']].cumulative_query_revenue
        old_query_fee_amt = df.iloc[timestep-2].indexers[event['indexer']].cumulative_query_revenue
        model_query_fee_amt = new_query_fee_amt - old_query_fee_amt
        if debug:
            print(f"Event: Timestep={timestep-1}, Query Reward Tokens={event_query_fee_amt}")
            print(f"Model: Timestep={timestep-1}, Query Reward Tokens={model_query_fee_amt}")

        try:
            ratio =  abs(event_query_fee_amt / model_query_fee_amt)
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
    print(f"Allocation Collecteds | Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   
    
def test_allocation_createds(debug):
    events_dict = {i:j for (i, j) in allocation_created_events.items() if i < max_timestep}
    
    if debug:
        print("EXPECTED TRUE ALLOCATION CREATED EVENTS:")
        for timestep, events_list in events_dict.items():
            if events_list is None:
                allocation_created = 0
            else:
                allocation_created = sum([e['tokens'] for e in events_list])
            print(f"{timestep}, {allocation_created}")
    
    if debug:
        print("MODELED RESULTS")
        for timestep, events_list in events_dict.items():    
            event = events_list[0]
            new_allocation_amt = df.iloc[timestep-1].indexers[event['indexer']].subgraphs[event['subgraphDeploymentID']].tokens
            try:
                old_allocation_amt = df.iloc[timestep-2].indexers[event['indexer']].subgraphs[event['subgraphDeploymentID']].tokens
            except KeyError:
                old_allocation_amt = 0
            model_allocation_amt = new_allocation_amt - old_allocation_amt
            print(f"{timestep}, {model_allocation_amt=}")

    if debug:
        print("UNITTEST RESULTS")
    cntExact = 0
    cntReallyClose = 0
    cntClose = 0
    cnt = 0
    cntWrong = 0
    for timestep, events_list in events_dict.items():
        if events_list is None:
            event_amt = 0
        else:
            event_amt = sum([e['tokens'] for e in events_list])
            event = events_list[0]
            new_allocation_amt = df.iloc[timestep-1].indexers[event['indexer']].subgraphs[event['subgraphDeploymentID']].tokens
            try:
                old_allocation_amt = df.iloc[timestep-2].indexers[event['indexer']].subgraphs[event['subgraphDeploymentID']].tokens
            except KeyError:
                old_allocation_amt = 0
            model_allocation_amt = new_allocation_amt - old_allocation_amt

        if debug:
            print(f"Event: Timestep={timestep-1}, Allocation Tokens={event_amt}")
            print(f"Model: Timestep={timestep-1}, Allocation Tokens={model_allocation_amt}")

        try:
            ratio =  abs(event_amt / model_allocation_amt)
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
    print(f"Allocation Createds | Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   
    
def test_allocation_closeds(debug):
    events_dict = {i:j for (i, j) in allocation_closed_events.items() if i < max_timestep}
    
    if debug:
        print("EXPECTED TRUE ALLOCATION CLOSED EVENTS:")
        for timestep, events_list in events_dict.items():
            if events_list is None:
                allocation_closed = 0
            else:
                allocation_closed = sum([e['tokens'] for e in events_list])
            print(f"{timestep}, {allocation_closed}")
    
    if debug:
        print("MODELED RESULTS")
        for timestep, events_list in events_dict.items():    
            event = events_list[0]
            new_allocation_amt = df.iloc[timestep-1].indexers[event['indexer']].subgraphs[event['subgraphDeploymentID']].tokens
            try:
                old_allocation_amt = df.iloc[timestep-2].indexers[event['indexer']].subgraphs[event['subgraphDeploymentID']].tokens
            except KeyError:
                old_allocation_amt = 0
            model_allocation_amt = new_allocation_amt - old_allocation_amt
            print(f"{timestep}, {model_allocation_amt=}")

    if debug:
        print("UNITTEST RESULTS")
    cntExact = 0
    cntReallyClose = 0
    cntClose = 0
    cnt = 0
    cntWrong = 0
    for timestep, events_list in events_dict.items():
        if events_list is None:
            event_amt = 0
        else:
            event_amt = sum([e['tokens'] for e in events_list])
            event = events_list[0]
            new_allocation_amt = df.iloc[timestep-1].indexers[event['indexer']].subgraphs[event['subgraphDeploymentID']].tokens
            try:
                old_allocation_amt = df.iloc[timestep-2].indexers[event['indexer']].subgraphs[event['subgraphDeploymentID']].tokens
            except KeyError:
                old_allocation_amt = 0
            model_allocation_amt = old_allocation_amt - new_allocation_amt

        if debug:
            print(f"Event: Timestep={timestep-1}, Allocation Tokens={event_amt}")
            print(f"Model: Timestep={timestep-1}, Allocation Tokens={model_allocation_amt}")

        try:
            ratio =  abs(event_amt / model_allocation_amt)
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
    print(f"Allocation Closeds | Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   


def test_stake_depositeds(debug):
    events_dict = {i:j for (i, j) in stake_deposited_events.items() if i < max_timestep}
    
    if debug:
        print("EXPECTED TRUE ALLOCATION CLOSED EVENTS:")
        for timestep, events_list in events_dict.items():
            if events_list is None:
                stake_deposited = 0
            else:
                stake_deposited = sum([e['tokens'] for e in events_list])
            print(f"{timestep}, {stake_deposited}")
    
    if debug:
        print("MODELED RESULTS")
        for timestep, events_list in events_dict.items():    
            event = events_list[0]
            new_deposited_stake = df.iloc[timestep-1].indexers[event['indexer']].cumulative_deposited_stake
            try:
                old_deposited_stake = df.iloc[timestep-2].indexers[event['indexer']].cumulative_deposited_stake
            except KeyError:
                old_deposited_stake = 0
            model_deposited_stake = new_deposited_stake - old_deposited_stake
            print(f"{timestep}, {model_deposited_stake=}")

    if debug:
        print("UNITTEST RESULTS")
    cntExact = 0
    cntReallyClose = 0
    cntClose = 0
    cnt = 0
    cntWrong = 0
    for timestep, events_list in events_dict.items():
        if events_list is None:
            event_amt = 0
        else:
            event_amt = sum([e['tokens'] for e in events_list])
            event = events_list[0]
            new_deposited_stake = df.iloc[timestep-1].indexers[event['indexer']].cumulative_deposited_stake
            try:
                old_deposited_stake = df.iloc[timestep-2].indexers[event['indexer']].cumulative_deposited_stake
            except KeyError:
                old_deposited_stake = 0
            model_deposited_stake = new_deposited_stake - old_deposited_stake
        if debug:
            print(f"Event: Timestep={timestep-1}, Deposited Stake Tokens={event_amt}")
            print(f"Model: Timestep={timestep-1}, Deposited Stake Tokens={model_deposited_stake}")

        try:
            ratio =  abs(event_amt / model_deposited_stake)
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
    print(f"Deposited Stake | Exact: {cntExact}, ReallyClose: {cntReallyClose}, Close: {cntClose}, Wrong: {cntWrong}, Total Number: {cnt}")   


if __name__ == '__main__':
    print("UNITTEST RESULTS")
    debug = False
    test_delegation(debug=debug)
    test_undelegation(debug=debug)
    test_withdraw(debug=debug)
    
    # this is indexing rewards
    test_rewards_assigned(debug=debug) 
    
    # this is query fees
    test_allocation_collecteds(debug=debug) 
    test_allocation_createds(debug=debug)
    
    # could be the same amount as created under assumption of no slashing 
    test_allocation_closeds(debug=debug) 
    
    # compare indexer.cumulative_deposited_stake before and after (this is the amount of indexing fees that does not go to pool)
    # if they are restaking, it goes to cumulative_deposited_stake, NOT holdings and vice versa.
    test_stake_depositeds(debug=debug) 



