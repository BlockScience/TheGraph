from .utils import get_shifted_event


def revenue_amt(params, step, sL, s):
    indexer_id = None
    subgraph_id = None
    indexing_fee_amt = 0
    query_fee_amt = 0
    slash_amt = 0
    rewards_assigned_events = get_shifted_event(s, sL, params['rewards_assigned_events'])
    if rewards_assigned_events is not None:
        indexing_fee_amt = sum([e['amount'] for e in rewards_assigned_events])
        indexer_id = rewards_assigned_events[0]['indexer']

    allocation_closed_events = get_shifted_event(s, sL, params['allocation_closed_events'])
    if allocation_closed_events is not None:
        indexer_id = allocation_closed_events[0]['indexer']
        subgraph_id = allocation_closed_events[0]['subgraphDeploymentID']

    allocation_collected_events = get_shifted_event(s, sL, params['allocation_collected_events'])
    if allocation_collected_events is not None:
        query_fee_amt = sum([e['tokens'] for e in allocation_collected_events])
        indexer_id = allocation_collected_events[0]['indexer']
        subgraph_id = allocation_collected_events[0]['subgraphDeploymentID']


    return {'indexer_id': indexer_id,
            'subgraph_id': subgraph_id,
            'indexing_fee_amt': indexing_fee_amt,
            'query_fee_amt': query_fee_amt}


def revenue_process(params, step, sL, s, inputs):
    key = 'indexers'
    value = s['indexers']
    indexer_id = inputs['indexer_id']
    indexing_revenue = inputs['indexing_fee_amt']
    query_revenue = inputs['query_fee_amt']
    if inputs['indexer_id']:
        s['indexers'][inputs['indexer_id']].GRT += inputs['indexing_fee_amt']
        indexer = value[inputs['indexer_id']]
        if inputs['indexing_fee_amt'] or indexer.buffered_rewards_assigned:
            if inputs['subgraph_id']:
                # it's an allocation_closed_event or allocation_created_event or allocation_collected_event
                subgraph = indexer.subgraphs[inputs['subgraph_id']]
                print(f'--before {subgraph.indexing_fees=}')
                print('EVENT: ALLOCATION CLOSED EVENT/ASSIGN INDEXING FEE TO SUBGRAPH')
                subgraph.indexing_fees += indexer.buffered_rewards_assigned
                print(f'--after {subgraph.indexing_fees=}')
                indexer.cumulative_indexing_revenue += indexer.buffered_rewards_assigned
                
        else:
            print('EVENT: REWARDS ASSIGNED/INDEXING FEE EVENT')
            # it's a rewards assigned events, so just buffer the rewards until we figure out what subgraph to assign them to.
            indexer.buffered_rewards_assigned += inputs['indexing_fee_amt']
    if indexing_revenue != 0 or query_revenue != 0:
        indexer = s['indexers'][indexer_id]
        query_fee_cut = indexer.query_fee_cut
        indexing_revenue_cut = indexer.indexer_revenue_cut
        revenue_to_indexer = (indexing_revenue + 
                              query_revenue -
                              calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut))
        indexer.holdings += revenue_to_indexer
    
        if not indexer.pool_delegated_stake.is_zero():
            query_fee_cut = indexer.query_fee_cut
            indexing_revenue_cut = indexer.indexer_revenue_cut

            # 5.2 D+ = D + Ri * (1 - phi)
            non_indexer_revenue = calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut)
            
            indexer.pool_delegated_stake += non_indexer_revenue

        indexer.cumulative_non_indexer_revenue += calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut)

    if inputs['query_fee_amt']:
        print('EVENT: ALLOCATION COLLECTED/QUERY FEE EVENT')
        indexer = s['indexers'][inputs['indexer_id']]
        subgraph = indexer.subgraphs[inputs['subgraph_id']]
        indexer.cumulative_query_revenue += inputs['query_fee_amt']
        subgraph.query_fees += inputs['query_fee_amt']

    return key, value


def calculate_revenue_to_indexer_pool(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut):
    """ Calculate and distribute query and indexing rewards to indexer pool """
    # D+ = D + Ri * (1 - alpha)
    # Indexing rewards - indexer cut.    
    non_indexer_revenue_cut = (1 - indexing_revenue_cut) * indexing_revenue    

    # D+ = D + Rq * (1 - phi)
    # Query rewards - indexer cut.   
    # TODO: is this right?!    
    non_indexer_query_fee_cut = 0
    # non_indexer_query_fee_cut = (1 - query_fee_cut) * query_revenue

    non_indexer_revenue_net = non_indexer_revenue_cut + non_indexer_query_fee_cut   
    return non_indexer_revenue_net    


