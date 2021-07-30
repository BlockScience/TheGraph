from model.parts.delegator_behaviors import process_delegation_event

""" indexing fees increase shares
query fees do not increase shares """

def revenue_amt(params, step, sL, prev_state):
    timestep = prev_state['timestep']
    
    indexing_fee_events = params['indexing_fee_events'].get(timestep)
    if indexing_fee_events is None:
        indexing_fee_amt = 0
    else:
        indexing_fee_amt = sum([e['tokens'] for e in indexing_fee_events])
    
    query_fee_events = params['query_fee_events'].get(timestep)
    if query_fee_events is None:
        query_fee_amt = 0
    else:
        query_fee_amt = sum([e['tokens'] for e in query_fee_events])

    return {'indexing_fee_amt': indexing_fee_amt,
            'query_fee_amt': query_fee_amt}

def mint_GRT(params, step, sL, prev_state, inputs):
    # print('storing revenue')
    key = 'GRT'
    GRT = prev_state['GRT']
    
    # TODO: Check this.
    delta = inputs['indexing_fee_amt']
    
    return key, GRT + delta

def store_query_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'query_revenue'
    # indexer_allocation_rate = params['indexer_allocation_rate']
    query_fees =  inputs['query_fee_amt']

    return key, query_fees

def store_indexing_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'indexing_revenue'
    indexer_allocation_rate = params['indexer_allocation_rate']
    revenue_amt = inputs['revenue_amt']
    indexer_rewards = revenue_amt * indexer_allocation_rate
    query_fees =  inputs['query_fee_amt']   
    return key, indexer_rewards

def store_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'period_revenue'
    indexer_allocation_rate = params['indexer_allocation_rate']
    # query_fees =  inputs['revenue_amt']
    # minted_rewards = inputs['minted_rewards']
    # indexer_rewards = minted_rewards * indexer_allocation_rate
    indexer_rewards = revenue_amt * indexer_allocation_rate

    # return key, indexer_rewards + query_fees
    return key, indexer_rewards

def distribute_revenue_to_delegators(params, step, sL, s, inputs):
    """ Calculate and distribute query and indexing rewards to delegators """
    indexing_revenue = inputs['indexing_fee_amt']
    query_revenue = inputs['query_fee_amt']   

    query_fee_cut = params['query_fee_cut']
    indexing_revenue_cut = params['indexer_revenue_cut']
    # step 1: collect revenue from the state
    
    # 5.2 D+ = D + Ri * (1 - phi)
    pool_delegated_stake = sum([d.delegated_tokens for d in s['delegators'].values()])

    for id, delegator in s['delegators'].items():
        print(f'{id=}, {s["timestep"]=}, {delegator.shares=}')
        if id == 'indexer':
            # step 2: distribute indexer share IN ADDITION to indexer's delegator share.
            # NOTE: skip pool reward, handle that in distribute_revenue_to_pool
            revenue_to_indexer = calculate_revenue_to_indexer(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut)
            delegator.holdings += revenue_to_indexer

        ## NOTE: Non-indexer delegators get nothing.  Their rewards are added back to the pool and no new shares are issues.
        
    key = 'delegators'
    value = s['delegators']
    return key, value

def distribute_revenue_to_pool(params, step, sL, s, inputs):
    """ Calculate and distribute query and indexing rewards to indexer pool """
    pool_delegated_stake = s['pool_delegated_stake']

    indexing_revenue = inputs['indexing_fee_amt']
    query_revenue = inputs['query_fee_amt']

    query_fee_cut = params['query_fee_cut']
    indexing_revenue_cut = params['indexer_revenue_cut']
    non_indexer_revenue_net = calculate_revenue_to_indexer(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut)
    pool_delegated_stake += non_indexer_revenue_net
    print(f'{pool_delegated_stake=}')
    key = 'pool_delegated_stake'
    return key, pool_delegated_stake

def calculate_revenue_to_indexer(indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut):
    """ Calculate and distribute query and indexing rewards to indexer pool """
    # step 1: collect revenue from the state
    # D+ = D + Ri * (1 - alpha)
    # Indexing rewards - indexer cut.    
    non_indexer_revenue_cut = (1 - indexing_revenue_cut) * indexing_revenue    

    # D+ = D + Rq * (1 - phi)
    # Query rewards - indexer cut.
    non_indexer_query_fee_cut = (1 - query_fee_cut) * query_revenue

    non_indexer_revenue_net = non_indexer_revenue_cut + non_indexer_query_fee_cut   
    return non_indexer_revenue_net    