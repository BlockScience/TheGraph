import random


def may_act_this_timestep(params, step, sL, s):
    acting_delegator_ids = []
    for id, delegator in s['delegators'].items():
        if delegator.will_act():
            acting_delegator_ids.append(id)

    # randomize list.
    random.shuffle(acting_delegator_ids)

    return {'acting_delegator_ids': acting_delegator_ids}

# NOTE: this most likely needs to be changed, but i put it here so tax can be taken at same level
def delegator_action(params, step, sL, s):
    # who delegates, 
    # how many tokens.
    delegation_tokens_quantity = params['delegation_tokens_quantity']
    undelegation_shares_quantity = params['undelegation_shares_quantity']
    withdraw_tokens_quantity = params['withdraw_tokens_quantity']
    return {'delegation_tokens_quantity': delegation_tokens_quantity,
            'undelegation_shares_quantity': undelegation_shares_quantity,
            'withdraw_tokens_quantity': withdraw_tokens_quantity}

def delegate(params, step, sL, s, inputs):
    #  loop through acting delegators id list
    pool_delegated_stake = sum([d.delegated_tokens for d in s['delegators'].values()])
    # NOTE: must recompute global shares each time because it affects how many tokens go where.
    # shares = s['shares']
    shares = sum([d.shares for d in s['delegators'].values()])
    delegation_tax_rate = params['delegation_tax_rate']
    acting_delegator_ids = inputs['acting_delegator_ids']
    delegation_tokens_quantity = inputs['delegation_tokens_quantity']

    # print(f'act: {acting_delegator_ids=}')
    for delegator_id in acting_delegator_ids:
        # accounting of current state (previous actor will have changed it)
        # NOTE: order of purchase doesn't matter, so we don't need updated pool state to calculate.
        if delegator_id == 0:
            continue
        delegator = s['delegators'][delegator_id]        

        if delegation_tokens_quantity >= delegator.holdings:
            delegation_tokens_quantity = delegator.holdings        

        delegator.holdings -= delegation_tokens_quantity
        delegator.delegated_tokens += delegation_tokens_quantity * (1 - delegation_tax_rate)
        pool_delegated_stake += delegation_tokens_quantity * (1 - delegation_tax_rate)
        # 5 * (0.995) / 10 * 10 = 4.975
        print(f'{pool_delegated_stake=}, {shares=}')
        new_shares = ((delegation_tokens_quantity * (1 - delegation_tax_rate)) / pool_delegated_stake) * shares
        delegator.shares += new_shares
        # store shares locally only--it has to be recomputed each action block because we don't save it until bookkeeping
        shares += new_shares 
        print(f'ACTION: DELEGATE--{delegator_id=}, {delegator.holdings=}, {delegator.delegated_tokens=}, {delegator.undelegated_tokens=}, {delegator.shares=}')
        
    key = 'delegators'
    value = s['delegators']
    return key, value

def account_for_tax(params, step, sL, s, inputs):
    key = 'GRT'
    delegation_tokens_quantity = inputs['delegation_tokens_quantity']
    delegation_tax_rate = params['delegation_tax_rate']
    
    tax = delegation_tax_rate * delegation_tokens_quantity
    value = s['GRT'] - tax
    return key, value

def undelegate(params, step, sL, s, inputs):
    
    # pool_delegated_stake needs to be updated
    # pool_delegated_stake = s['pool_delegated_stake']
    pool_delegated_stake = sum([d.delegated_tokens for d in s['delegators'].values()])
    
    # shares needs to be kept updated
    # shares = s['shares']
    shares = sum([d.shares for d in s['delegators'].values()])
    
    timestep = s['timestep']
    acting_delegator_ids = inputs['acting_delegator_ids']
    # undelegation_shares_quantity = inputs['undelegation_shares_quantity']
    # print(f'act: {acting_delegator_ids=}')
    
    #  loop through acting delegators id list
    for delegator_id in acting_delegator_ids:
        if delegator_id == 0:
            # indexer doesn't undelegate everything
            continue
        delegator = s['delegators'][delegator_id]
        undelegation_shares_quantity = delegator.shares

        if undelegation_shares_quantity < 0:
            # require a non-zero amount of shares
            continue

        if undelegation_shares_quantity > delegator.shares:
            # require delegator to have enough shares in the pool to undelegate
            undelegation_shares_quantity = delegator.shares

        # Withdraw tokens if available
        withdrawableDelegatedTokens = delegator.getWithdrawableDelegatedTokens(timestep)
        if withdrawableDelegatedTokens > 0:
            delegator.withdraw()

        undelegated_tokens = undelegation_shares_quantity * pool_delegated_stake / shares
        unbonding_timestep = params['unbonding_timeblock'] + timestep
        delegator.set_undelegated_tokens(unbonding_timestep, undelegated_tokens)
        delegator.delegated_tokens -= undelegated_tokens
        delegator.shares -= undelegation_shares_quantity
        pool_delegated_stake -= undelegation_shares_quantity
        shares -= undelegation_shares_quantity
        print(f'ACTION: UNDELEGATE--{delegator_id=}, {delegator.holdings=}, {delegator.delegated_tokens=}, {delegator.undelegated_tokens=}, {delegator.shares=}')
    key = 'delegators'
    value = s['delegators']
    return key, value

def withdraw(params, step, sL, s, inputs):
    #  loop through acting delegators id list
    timestep = s['timestep']
    acting_delegator_ids = inputs['acting_delegator_ids']
    # print(f'act: {acting_delegator_ids=}')
    
    for delegator_id in acting_delegator_ids:
        if delegator_id == 0:
            continue
        delegator = s['delegators'][delegator_id]
        
        withdrawableDelegatedTokens = delegator.getWithdrawableDelegatedTokens(timestep)
        if withdrawableDelegatedTokens > 0:
            delegator.withdraw()
        print(f'ACTION: WITHDRAW--{delegator_id=}, {delegator.holdings=}, {delegator.delegated_tokens=}, {delegator.undelegated_tokens=}, {delegator.shares=}')
    key = 'delegators'
    value = s['delegators']
    return key, value
