def compute_and_store_private_prices(params, step, sL, s, inputs):
    delegators = s['delegators']
    supply = s['supply']
    reserve = s['reserve']
    timestep = s['timestep']
    indexer_revenue_cut = params['indexer_revenue_cut']
    risk_adjustment = params['risk_adjustment']
    reserve_to_revenue_token_exchange_rate = params['reserve_to_revenue_token_exchange_rate']
    private_price = 0
    
    for delegator in delegators.values():
        # NOTE: this is the discounted value of the dividends
        dividend_value = delegator.dividend_value(supply, indexer_revenue_cut, reserve_to_revenue_token_exchange_rate)
        
        # NOTE: this is the current spot price, from the invariant
        share_value = reserve / supply
        
        risk_adjusted_share_value = share_value * risk_adjustment
        
        private_price = dividend_value + risk_adjusted_share_value
        # print(f'{timestep=}, {private_price=}')
        delegator.private_prices[timestep] = private_price
    
    # print(delegators)
    key = 'delegators'
    value = delegators
    return key, value
