
BETA_del = [0.003]

params = {
        "r_del": [10],        #	Indexer’s initial delegated stake
        "s_del": [10],    #	Indexer’s initial delegated stake share of pool
        "expected_revenue": [7],
        "indexer_revenue_cut": [0.25],         # 1-theta  (theta is what all of the other delegators get)
        "arrival_rate": [0.5],
        "expected_reserve_token_holdings": [25],
        "delegator_estimation_noise_mean": [0],
        "delegator_estimation_noise_variance": [1],  # proportional to expected_revenue
        "reserve_to_revenue_token_exchange_rate": [1],
        "delegator_activity_rate": [0.5],
        "mininum_required_price_pct_diff_to_act": [0.02],
        "risk_adjustment": [0.7],  # cut 30% of the value off due to risk
        "half_life_vesting_rate": [0.5], # this is the fraction of shares that vest each timestep if using half life vesting
        "cliff_vesting_timesteps": [3], # this is the number of timesteps until shares are fully vested
        'BETA_del': BETA_del, # tax percentage from delegated tokens to be burned
}