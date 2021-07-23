# def account_global_state_from_delegator_states(params, step, sL, s):
#     previous_shares = s['shares']
#     print('previous_shares',previous_shares)

#     previous_pool_delegated_stake = s['pool_delegated_stake']

#     # invariant is the value of function V that doesn't change. always S**2/R
#     # NOTE: previous_pool_delegated_stake == 0 might be a bad condition?
#     invariant = 0
#     if previous_pool_delegated_stake > 0:
#         invariant = previous_shares / previous_pool_delegated_stake

#     # sum the share shares of all delegators
#     shares = sum([d.shares for d in s['delegators'].values()])
#     print('shares',shares)

#     # back out the pool_delegated_stake using the same invariant/function as above.
#     pool_delegated_stake = 0
#     if invariant > 0:
#         pool_delegated_stake = shares / invariant


#     # spot price is the derivative at the point of the curve where we are
#     spot_price = 0
#     if shares > 0:
#         spot_price = pool_delegated_stake / shares
#     print('shares',shares)

#     # pool_delegated_stake_token_holdings = sum([d.pool_delegated_stake_token_holdings for d in s['delegators'].values()])
#     # revenue_token_holdings = sum([d.revenue_token_holdings for d in s['delegators'].values()])
    
#     return {'shares': shares,
#             'pool_delegated_stake': pool_delegated_stake,
#             'spot_price': spot_price}


# def compute_half_life_vested_shares(params, step, sL, s, inputs):
#     """ calculate how many shares are vested using half_life vesting """
#     key = 'delegators'
    
#     delegators = s['delegators']

#     half_life_vesting_rate = params['half_life_vesting_rate']
    
#     for delegator in delegators.values():
#         # for future computation speed, vest them in chunks, it doesn't matter which chunk
#         shares_vesting_this_period = delegator.unvested_shares * half_life_vesting_rate
#         for timestep in delegator._unvested_shares:
#             remaining_shares_to_vest = shares_vesting_this_period
#             if delegator._unvested_shares[timestep] > remaining_shares_to_vest:
#                 delegator._unvested_shares[timestep] -= remaining_shares_to_vest
#                 break
#             else:
#                 # 0 out and go onto the next one
#                 remaining_shares_to_vest -= delegator._unvested_shares[timestep]
#                 delegator._unvested_shares[timestep] = 0
                
#         delegator.vested_shares += shares_vesting_this_period
#     # print(f'{delegator.vested_shares=}, {delegator.unvested_shares=}, {delegator.shares=}')
#     value = delegators

#     return key, value
        

# def compute_cliff_vested_shares(params, step, sL, s, inputs):
#     """ calculate how many shares are vested using cliff vesting """
#     key = 'delegators'
#     delegators = s['delegators']
#     timestep = s['timestep']

#     cliff_vesting_timestep = timestep - params['cliff_vesting_timesteps']
    
#     for delegator in delegators.values():
#         if cliff_vesting_timestep in delegator._unvested_shares:
#             shares_vesting_this_period = delegator._unvested_shares[cliff_vesting_timestep]
#             delegator.vested_shares += shares_vesting_this_period
#             delegator._unvested_shares[cliff_vesting_timestep] = 0
#             # print(f'{shares_vesting_this_period=}, {delegator.vested_shares=}, {delegator._unvested_shares=}')
#         else:
#             # no shares are being vested this timestep
#             pass

#     value = delegators
#     return key, value

    
def store_shares(params, step, sL, s, inputs):
    key = 'shares'
    # add shares of all delegators
    shares = sum([d.shares for d in s['delegators']])    
    return key, shares


def store_pool_delegated_stake(params, step, sL, s, inputs):
    key = 'pool_delegated_stake'
    pool_delegated_stake = sum([d.delegated_tokens for d in s['delegators']])    
    return key, pool_delegated_stake

def increment_epoch(params, step, sL, s, inputs):
    key = 'epoch'
    if s['timestep'] == 100:
        s['epoch'] += 1
    return key, s['epoch']

