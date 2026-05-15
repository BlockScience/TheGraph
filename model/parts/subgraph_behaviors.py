from .subgraph import Subgraph

def allocation_created_events(params, step, sL, s):
    timestep = s['timestep']
    allocation_created_events = params['allocation_created_events'].get(timestep)
    return {'allocation_created_events': allocation_created_events}

def create_allocations(params, step, sL, s, inputs):
    key = 'indexers'
    indexers = s[key]

    event = inputs['event'][0] if inputs['event'] else None
    if event:
        # process allocation_collected_event
        indexerID = event['indexer']

        indexer = indexers[indexerID]
        subgraphID = event['subgraphDeploymentID']
        if subgraphID not in indexer.subgraphs:
            subgraph = Subgraph()
            indexer.subgraphs[subgraphID] = subgraph
        else:
            subgraph = indexer.subgraphs[subgraphID]
        subgraph.tokens += event['tokens']
        # these are not on allocation_created event
        # subgraph.indexing_fees += event['rebateFees']
        # subgraph.query_fees += event['curationFees']
        print(f'{subgraph.ROI_indexing()=}, {subgraph.ROI_query()=}')
    return key, indexers


def allocation_closed_events(params, step, sL, s):
    timestep = s['timestep']
    allocation_closed_events = params['allocation_closed_events'].get(timestep)
    return {'allocation_closed_events': allocation_closed_events}

def close_allocations(params, step, sL, s, inputs):
    key = 'indexers'
    indexers = s[key]

    event = inputs['event'][0] if inputs['event'] else None
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
        subgraph.tokens -= event['tokens']
        # these are not on allocation_closed event
        # subgraph.indexing_fees += event['rebateFees']
        # subgraph.query_fees += event['curationFees']
        # print(f'{subgraph.ROI_indexing()=}, {subgraph.ROI_query()=}')
    return key, indexers


