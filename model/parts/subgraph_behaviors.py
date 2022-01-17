from .subgraph import Subgraph
from .allocation import Allocation

def allocation_created_events(params, step, sL, s):
    timestep = s['timestep']

    # TODO increment by injected_event_shift to get real timestep.
    # if previous event shift is < current event shift, WE HAVE AN EVENT from agent!
    allocation_created_events = params['allocation_created_events'].get(timestep)
    
    #TODO: interleave output from agent.

    return {'allocation_created_events': allocation_created_events}

def create_allocations(params, step, sL, s, inputs):
    key = 'indexers'
    indexers = s[key]

    event = inputs['allocation_created_events'][0] if inputs['allocation_created_events'] else None
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
        print(f'ALLOCATION CLOSED EVENT')
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


