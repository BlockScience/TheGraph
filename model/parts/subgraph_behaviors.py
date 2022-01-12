from .subgraph import Subgraph
from .allocation import Allocation

def allocation_created_events(params, step, sL, s):
    timestep = s['timestep']
    allocation_created_events = params['allocation_created_events'].get(timestep)
    
    return {'allocation_created_events': allocation_created_events}

def create_allocations(params, step, sL, s, inputs):
    key = 'indexers'
    indexers = s[key]

    event = inputs['allocation_created_events'][0] if inputs['allocation_created_events'] else None
    if event:
        # process allocation_collected_event
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


def allocation_closed_events(params, step, sL, s):
    timestep = s['timestep']
    allocation_closed_events = params['allocation_closed_events'].get(timestep)
    return {'allocation_closed_events': allocation_closed_events}

def close_allocations(params, step, sL, s, inputs):
    key = 'indexers'
    indexers = s[key]

    event = inputs['allocation_closed_events'][0] if inputs['allocation_closed_events'] else None
    if event:
        # process allocation_closed_event
        indexerID = event['indexer']

        indexer = indexers[indexerID]
        subgraphID = event['subgraphDeploymentID']
        if subgraphID not in indexer.subgraphs:
            subgraph = Subgraph()
            indexer.subgraphs[subgraphID] = subgraph
        else:
            subgraph = indexer.subgraphs[subgraphID]
        
        del subgraph.allocations[event['allocationID']]

    return key, indexers


