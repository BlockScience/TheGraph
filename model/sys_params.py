R_i_rate = [0.03]

indexer_allocation_rate = [0.0050]  # ASSUMED share of minted by subgraph by indexer
blocks_per_day = 100
unbonding_days = 28

allocation_days = [28]

delegation_tax = [0.005]
unbonding_timeblock = [unbonding_days*blocks_per_day]
delegation_leverage = [16]

query_fee_cut = [0.10]

params = {
        "r_del": [10],        #	Indexer’s initial delegated stake
        "s_del": [10],    #	Indexer’s initial delegated stake share of pool
        "expected_revenue": [7],
        "indexer_revenue_cut": [0.25],         # 1-theta  (theta is what all of the other delegators get)
        "arrival_rate": [0.5],
        "expected_initial_token_holdings": [25],
        "delegator_estimation_noise_mean": [0],
        "delegator_estimation_noise_variance": [1],  # proportional to expected_revenue
        "total_delegated_stake_to_revenue_token_exchange_rate": [1],
        "delegator_activity_rate": [0.5],
        "mininum_required_price_pct_diff_to_act": [0.02],
        "risk_adjustment": [0.7],  # cut 30% of the value off due to risk
        # "half_life_vesting_rate": [0.5], # this is the fraction of shares that vest each timestep if using half life vesting
        # "cliff_vesting_timesteps": [3], # this is the number of timesteps until shares are fully vested
        'delegation_tax': delegation_tax, # tax percentage from delegated tokens to be burned
        'unbonding_timeblock': unbonding_timeblock, # time unbonded tokens are frozen from being eligibble to be withdrawn
        'delegation_leverage': delegation_leverage, # tax percentage from delegated tokens to be burned
        'R_i_rate': R_i_rate, # indexer reward revenue rate (inflationary rewards)
        'allocation_days': allocation_days, # time for allocation
        'indexer_allocation_rate': indexer_allocation_rate, # ASSUMED share of minted by subgraph by indexer
        'query_fee_cut': query_fee_cut, # query fee indexer cut rate



}