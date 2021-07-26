def store_shares(params, step, sL, s, inputs):
    key = 'shares'
    # add shares of all delegators
    shares = sum([d.shares for d in s['delegators'].values()])    
    return key, shares


def store_pool_delegated_stake(params, step, sL, s, inputs):
    key = 'pool_delegated_stake'
    pool_delegated_stake = sum([d.delegated_tokens for d in s['delegators'].values()])    
    return key, pool_delegated_stake

def increment_epoch(params, step, sL, s, inputs):
    key = 'epoch'
    if s['timestep'] == 100:
        s['epoch'] += 1
    return key, s['epoch']

