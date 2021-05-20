
import scipy.stats as stats


def revenue_amt(params, step, prev_state, state):
    revenue_amt = params["expected_revenue"] * stats.expon.rvs()
    # print(f'{revenue_amt=}')
    return {'revenue_amt': revenue_amt}


def store_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'period_revenue'
    value = inputs['revenue_amt']

    return key, value


def distribute_revenue(params, step, sL, s, inputs):
    revenue = s['period_revenue']
    indexer_revenue_cut = params['indexer_revenue_cut']
    shares = s['shares']

    # step 1: collect revenue from the state
    non_indexer_revenue_cut = ((1-indexer_revenue_cut) * revenue)
    revenue_per_share = non_indexer_revenue_cut / shares

    for id, delegator in s['delegators'].items():
        if id == 0:
            # step 2: get owners share, theta
            delegator.revenue_token_holdings += indexer_revenue_cut * revenue
        
        #  step 3: distribute non-owners share
        # print(f'{delegator.shares=}')
        delegator.revenue_token_holdings += delegator.shares * revenue_per_share
    
    key = 'delegators'
    value = s['delegators']
    return key, value
