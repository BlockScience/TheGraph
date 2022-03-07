from .subgraph import Subgraph
from .allocation import Allocation
# from .utils import get_shifted_events

#
# def allocation_created_events(params, step, sL, s):
#     key = 'allocation_created_events'
#     events = get_shifted_events(s, sL, params[key])
#     return {key: events}


def create_allocations(params, step, sL, s, inputs):
    key = 'indexers'
    indexers = s[key]

    event = inputs['event'][0] if inputs['event'] else None
    if event:
        print(f'ALLOCATION CREATED EVENT')
        # process allocation_created_event
        indexerID = event['indexer']
        assert(int(event['epoch']) == s['epoch'])
        indexer = indexers[indexerID]
        subgraphID = event['subgraphDeploymentID']
        if subgraphID not in indexer.subgraphs:
            subgraph = Subgraph()
            indexer.subgraphs[subgraphID] = subgraph
        else:
            subgraph = indexer.subgraphs[subgraphID]
        
        allocation = Allocation(event['allocationID'], event['tokens'], event['epoch'])
        subgraph.allocations[event['allocationID']] = allocation
        
        print(f'{subgraph.ROI_indexing()=}, {subgraph.ROI_query()=}')
    return key, indexers


# def allocation_closed_events(params, step, sL, s):
#     key = 'allocation_closed_events'
#     events = get_shifted_events(s, sL, params[key])
#     return {key: events}


def close_allocations(params, step, sL, s, inputs):
    key = 'indexers'
    indexers = s[key]

    event = inputs['event'][0] if inputs['event'] else None
    if event:
        # process allocation_closed_event
        print(f'ALLOCATION CLOSED EVENT')
        indexerID = event['indexer']

        indexer = indexers[indexerID]
        subgraphID = event['subgraphDeploymentID']
        if subgraphID not in indexer.subgraphs:
            subgraph = Subgraph()
            indexer.subgraphs[subgraphID] = subgraph
        else:
            subgraph = indexer.subgraphs[subgraphID]

        # 0 out tokens instead of deleting allocation for delegate_front_runner.            
        subgraph.allocations[event['allocationID']].tokens = 0
        # del subgraph.allocations[event['allocationID']]

    return key, indexers


