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
    pool_delegated_stake = s['pool_delegated_stake']
    shares = s['shares']
    delegation_tax_rate = params['delegation_tax_rate']
    acting_delegator_ids = inputs['acting_delegator_ids']
    delegation_tokens_quantity = inputs['delegation_tokens_quantity']

    # print(f'act: {acting_delegator_ids=}')
    for delegator_id in acting_delegator_ids:
        # accounting of current state (previous actor will have changed it)
        # NOTE: order of purchase doesn't matter, so we don't need updated pool state to calculate.
        delegator = s['delegators'][delegator_id]
        
        if amount_delegated >= delegator.holdings:
            amount_delegated = delegator.holdings
        
        delegator.holdings -= delegation_tokens_quantity
        delegator.delegated_tokens += delegation_tokens_quantity
        
        new_shares = ((delegation_tokens_quantity * (1 - delegation_tax_rate)) / pool_delegated_stake) * shares
        delegator.shares += new_shares
        
    key = 'delegators'
    value = s['delegators']
    return key, value

def account_for_tax(params, step, sL, s, inputs):
    key = 'GRT'
    delegation_tokens_quantity = inputs['delegation_tokens_quantity']
    delegation_tax_rate = params['delegation_tax_rate']
    
    tax = delegation_tax_rate * delegation_tokens_quantity
    value = s['GRT'] - tax

def undelegate(params, step, sL, s, inputs):
    #  loop through acting delegators id list
    pool_delegated_stake = s['pool_delegated_stake']
    shares = s['shares']
    timestep = s['timestep']
    acting_delegator_ids = inputs['acting_delegator_ids']
    undelegation_shares_quantity = inputs['undelegation_shares_quantity']
    # print(f'act: {acting_delegator_ids=}')
    
    for delegator_id in acting_delegator_ids:
        delegator = s['delegators'][delegator_id]
        if undelegation_shares_quantity < 0:
            # require a non-zero amount of shares
            continue

        if undelegation_shares_quantity > delegator.shares:
            # require delegator to have enough shares in the pool to undelegate
            continue

        # Withdraw tokens if available
        withdrawableDelegatedTokens = delegator.getWithdrawableDelegatedTokens(timestep)
        if withdrawableDelegatedTokens > 0:
            delegator.withdraw()

        undelegated_tokens = undelegation_shares_quantity * pool_delegated_stake / shares
        unbonding_timestep = params['unbonding_timeblock'] + timestep
        delegator.set_undelegated_tokens(unbonding_timestep, undelegated_tokens)
        delegator.delegated_tokens -= undelegation_shares_quantity
        delegator.shares -= undelegation_shares_quantity

def withdraw(params, step, sL, s, inputs):
    #  loop through acting delegators id list
    timestep = s['timestep']
    acting_delegator_ids = inputs['acting_delegator_ids']
    # print(f'act: {acting_delegator_ids=}')
    
    for delegator_id in acting_delegator_ids:
        delegator = s['delegators'][delegator_id]
        
        # Validatrion
        withdrawableDelegatedTokens = delegator.getWithdrawableDelegatedTokens(timestep)
        if withdrawableDelegatedTokens > 0:
            delegator.withdraw()
