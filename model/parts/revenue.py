
import scipy.stats as stats
from model.parts.delegator_behaviors import process_delegation_event

def revenue_amt(params, step, sL, prev_state):
    # placeholder for query fee revenue
    # revenue_amt = params["expected_revenue"] * stats.expon.rvs()
    
    # print(f'{revenue_amt=}')
    # R_i_rate = params['R_i_rate']
    # allocation_days = params['allocation_days']
    timestep = prev_state['timestep']
    
    # TODO: Check this logic    
    allocation_collected_events = params['allocation_collected_events'].get(timestep)
    if allocation_collected_events is None:
        revenue_amt = 0
        minted_rewards = 0
    else:
        # print(f'{allocation_collected_events=}')
        revenue_amt = sum([int(e['tokens']) for e in allocation_collected_events])
        minted_rewards = revenue_amt

    
    # if timestep % allocation_days == 0:
    #     GRT = prev_state['GRT']
    #     minted_rewards = GRT * R_i_rate * allocation_days / 365 # annual inflation
    # else:
    #     minted_rewards = 0
    return {'revenue_amt': revenue_amt, 'minted_rewards': minted_rewards}

def mint_GRT(params, step, sL, prev_state, inputs):
    # print('storing revenue')
    key = 'GRT'
    GRT = prev_state['GRT']
    
    delta = inputs['minted_rewards']
    
    return key, GRT + delta

def store_query_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'query_revenue'
    # indexer_allocation_rate = params['indexer_allocation_rate']
    query_fees =  inputs['revenue_amt']

    return key, query_fees

def store_indexing_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'indexing_revenue'
    indexer_allocation_rate = params['indexer_allocation_rate']
    minted_rewards = inputs['minted_rewards']
    indexer_rewards = minted_rewards * indexer_allocation_rate

    return key, indexer_rewards

def store_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'period_revenue'
    indexer_allocation_rate = params['indexer_allocation_rate']
    query_fees =  inputs['revenue_amt']
    minted_rewards = inputs['minted_rewards']
    indexer_rewards = minted_rewards * indexer_allocation_rate

    return key, indexer_rewards + query_fees

def distribute_indexer_revenue(params, step, sL, s, inputs):
    indexer_revenue = s['indexer_revenue']
    indexing_revenue = s['indexing_revenue']
    query_revenue = s['query_revenue']   

    query_fee_cut = params['query_fee_cut']
    indexing_revenue_cut = params['indexer_revenue_cut']

    # step 1: collect revenue from the state
    # 5.1 Indexing Rewards: Ir = Ir + Ri * alpha
    indexer_revenue_cut = indexing_revenue_cut * indexing_revenue
    
    # 5.2 Query Fee: I+r = Ir + Ri * phi
    indexer_query_fee_cut = query_fee_cut * query_revenue
    
    key = 'indexer_revenue'
    return key, indexer_revenue + indexer_revenue_cut + indexer_query_fee_cut


def distribute_revenue(params, step, sL, s, inputs):
    """ Calculate and distribute query and indexing rewards to delegators """
    shares = sum([d.shares for d in s['delegators'].values()])
    indexing_revenue = s['indexing_revenue']
    query_revenue = s['query_revenue']   

    query_fee_cut = params['query_fee_cut']
    indexing_revenue_cut = params['indexer_revenue_cut']
    delegation_tax_rate = params['delegation_tax_rate']
    initial_holdings = params['delegator_initial_holdings']
    delegators = s['delegators']
    # step 1: collect revenue from the state
    non_indexer_revenue_cut = (1 - indexing_revenue_cut) * indexing_revenue
    
    # 5.2 D+ = D + Ri * (1 - phi)
    non_indexer_query_fee_cut = (1 - query_fee_cut) * query_revenue
    non_indexer_revenue_net = non_indexer_revenue_cut + non_indexer_query_fee_cut
    revenue_per_share = non_indexer_revenue_net / shares
    pool_delegated_stake = sum([d.delegated_tokens for d in s['delegators'].values()])

    for id, delegator in s['delegators'].items():
        print(f'{id=}, {s["timestep"]=}, {delegator.shares=}')
        if id == 'indexer':
            # step 2: distribute indexer share IN ADDITION to indexer's delegator share.
            # skip pool reward, handle that in distribute_revenue_to_pool
            revenue_to_indexer = calculate_revenue_to_indexer(pool_delegated_stake, indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut)
            delegator.holdings += revenue_to_indexer
            # TODO: should indexer auto delegate to his own pool?
            
        # step 3: distribute delegator share
        delegation_tokens_quantity = delegator.shares * revenue_per_share
        delegation = {'delegator':id, 
                        'tokens':delegation_tokens_quantity}
        
        # and autoredelegate.
        pool_delegated_stake, shares = process_delegation_event(delegation, delegators, initial_holdings, 
                                delegation_tax_rate, pool_delegated_stake, shares)     
            
        
    key = 'delegators'
    value = s['delegators']
    return key, value


def distribute_revenue_to_pool(params, step, sL, s, inputs):
    """ Calculate and distribute query and indexing rewards to indexer pool """
    pool_delegated_stake = s['pool_delegated_stake']

    indexing_revenue = s['indexing_revenue']
    query_revenue = s['query_revenue']   

    query_fee_cut = params['query_fee_cut']
    indexing_revenue_cut = params['indexer_revenue_cut']

    # step 1: collect revenue from the state
    revenue_to_indexer = calculate_revenue_to_indexer(pool_delegated_stake, indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut)
    print(f'{revenue_to_indexer=}')
    key = 'pool_delegated_stake'
    return key, revenue_to_indexer

def calculate_revenue_to_indexer(pool_delegated_stake, indexing_revenue, query_revenue, query_fee_cut, indexing_revenue_cut):
    """ Calculate and distribute query and indexing rewards to indexer pool """
    # step 1: collect revenue from the state
    non_indexer_revenue_cut = (1 - indexing_revenue_cut) * indexing_revenue
    non_indexer_query_fee_cut = (1 - query_fee_cut) * query_revenue
    non_indexer_revenue_net = non_indexer_revenue_cut + non_indexer_query_fee_cut
   
    return pool_delegated_stake + non_indexer_revenue_net    