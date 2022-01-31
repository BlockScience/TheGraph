from model.parts.delegator import Delegator
# from .utils import get_shifted_events
from decimal import *


# def delegate_actions(params, step, sL, s):
#     """ this just gets all of the events at this timestep into policy variables """
#     key = 'delegation_events'
#     delegation_events = get_shifted_events(s, sL, params['delegation_tokens_events'], 'delegate')
#     return {key: delegation_events}
#
#
# def undelegate_actions(params, step, sL, s):
#     """ this just gets all of the events at this timestep into policy variables """
#     key = 'undelegation_events'
#     delegation_events = get_shifted_events(s, sL, params['undelegation_shares_events'], 'undelegate')
#     return {key: delegation_events}
#
#
# def withdraw_actions(params, step, sL, s):
#     """ this just gets all of the events at this timestep into policy variables """
#     key = 'withdraw_events'
#     delegation_events = get_shifted_events(s, sL, params['withdraw_tokens_events'], 'withdraw')
#     return {key: delegation_events}


def delegate(params, step, sL, s, inputs):
    event = inputs['event'][0] if inputs['event'] is not None else None
    if event:
        indexer = s['indexers'][event['indexer']]
        print("DELEGATE EVENT", event)
        # Step 3: Delegate
        # NOTE: must recompute global shares each time because it affects how many tokens go where.
        # TODO: don't think we need to compute shares each time because we have only one event per timestep.
        # shares = sum([d.shares for d in indexer.delegators.values()])
        # Try it this way.
        shares = indexer.shares
        
        delegation_tax_rate = params['delegation_tax_rate']        
        initial_holdings = params['delegator_initial_holdings']
        delegators = indexer.delegators

        delegator_id = event['delegator']
        if delegator_id == 1:
            print('agent delegation')
        if delegator_id not in delegators:
            delegators[delegator_id] = Delegator(delegator_id, holdings=initial_holdings)
        
        delegator = delegators[delegator_id]        
        delegation_tokens_quantity = event['tokens']

        indexer = process_delegation_event(delegation_tokens_quantity, delegator,
                                           delegation_tax_rate, indexer.pool_delegated_stake, shares,
                                           indexer)

    key = 'indexers'
    return key, s['indexers']


def process_delegation_event(delegation_tokens_quantity, delegator, delegation_tax_rate, pool_delegated_stake, shares, indexer):
    # NOTE: allow this for now.
    # if delegation_tokens_quantity >= delegator.holdings:
    #     delegation_tokens_quantity = delegator.holdings        
    delegator.holdings -= delegation_tokens_quantity
    
    # 5 * (0.995) / 10 * 10 = 4.975
    print(f'BEFORE DELEGATION: {pool_delegated_stake=}, {shares=}, {delegation_tax_rate=}, {delegation_tokens_quantity=}')

    # NOTE: this is the calculation if tax hadn't already been taken out before event was created.
    # new_shares = delegation_tokens_quantity * (1 - delegation_tax_rate) \
    #     if pool_delegated_stake.is_zero() \
    #     else ((delegation_tokens_quantity * (1 - delegation_tax_rate)) / pool_delegated_stake) * shares

    # NOTE: Tax is already taken out at this point.
    new_shares = delegation_tokens_quantity \
        if pool_delegated_stake.is_zero() \
        else (delegation_tokens_quantity / pool_delegated_stake) * shares

    # NOTE: pool_delegated_stake must be updated AFTER new_shares is calculated
    pool_delegated_stake += delegation_tokens_quantity
    delegator.shares += new_shares
    indexer.shares += new_shares
    # shares += new_shares
    # store shares locally only--it has to be recomputed each action block because we don't save it until bookkeeping
    print(f'AFTER DELEGATION: {pool_delegated_stake=}, {shares+new_shares=}, {delegation_tax_rate=}, {delegation_tokens_quantity=}')
    return indexer


def undelegate(params, step, sL, s, inputs):
    event = inputs['event'][0] if inputs['event'] is not None else None
    if event:
        indexer = s['indexers'][event['indexer']]
    
        # shares needs to be kept updated
        # shares = sum([d.shares for d in indexer.delegators.values()])

        delegator_id = event['delegator']
        if delegator_id == 1:
            print('agent undelegation')
        try:
            delegator = indexer.delegators[delegator_id]                
        except KeyError:
            print(f'''ERROR: Undelegation attempted on an Indexer that has not been Delegated to.
                      {indexer.id=}
                      {delegator_id=}''')
            key = 'indexers'
            value = s['indexers']
            return key, value

        undelegation_shares_quantity = event['shares']
        print(f'''EVENT: UNDELEGATE (before)--
            {delegator_id=}, 
            {delegator.holdings=}, 
            {delegator.undelegated_tokens=}, 
            {delegator.shares=}
            {undelegation_shares_quantity=}''')

        if undelegation_shares_quantity < 0:
            # require a non-zero amount of shares
            print(f'WARN: undelegation shares quantity < 0 ({undelegation_shares_quantity})')
        else:

            if undelegation_shares_quantity > delegator.shares:
                # require delegator to have enough shares in the pool to undelegate
                print(f'WARN: undelegation shares quantity > delegator shares held. ({undelegation_shares_quantity=}, {delegator.shares=})')
                undelegation_shares_quantity = delegator.shares

            # Withdraw tokens if available
            # TODO: make this accurate (28 days not timesteps)
            # withdrawableDelegatedTokens = delegator.getWithdrawableDelegatedTokens(timestep)
            # if withdrawableDelegatedTokens > 0:
            #     print(f'INFO: tokens withdrawn {withdrawableDelegatedTokens=}')
            #     delegator.withdraw(withdrawableDelegatedTokens)
            if indexer.shares < 0.000000000001:
                print(f'''EXCEPTION, no shares to undelegate,
                        {s['timestep']=}
                        {indexer.id=}''')
                
            undelegated_tokens = undelegation_shares_quantity * (indexer.pool_delegated_stake / indexer.shares)
            until = event['until']
            delegator.set_undelegated_tokens(until, undelegated_tokens)
            delegator.shares -= undelegation_shares_quantity
            indexer.pool_delegated_stake -= undelegated_tokens
            indexer.shares -= undelegation_shares_quantity
            print(f'''  (after)--
                        {delegator_id=}, 
                        {delegator.holdings=}, 
                        {undelegated_tokens=},
                        {delegator.undelegated_tokens=}, 
                        {delegator.shares=}
                        {until=}
                        {undelegation_shares_quantity=}''')
    key = 'indexers'
    value = s['indexers']
    return key, value


def withdraw(params, step, sL, s, inputs):
    #  loop through acting delegators id list
    effective_timestep = s['timestep'] - s['injected_event_shift']
    event = inputs['event'][0] if inputs['event'] is not None else None
    if event:
        indexer = s['indexers'][event['indexer']]
    
        delegator_id = event['delegator']
        if delegator_id == 1:
            print('agent withdraw')
        delegator = indexer.delegators[delegator_id]
        tokens = event['tokens']
        print(f'''EVENT: WITHDRAW (before)--
                    {delegator_id=}, 
                    {delegator.holdings=}, 
                    {delegator.undelegated_tokens=}, 
                    {delegator.shares=}
                    {tokens=}''')
        withdrawableDelegatedTokens = delegator.getWithdrawableDelegatedTokens(effective_timestep)
        if withdrawableDelegatedTokens > tokens:
            delegator.withdraw(tokens)
        elif withdrawableDelegatedTokens > 0:
            delegator.withdraw(withdrawableDelegatedTokens)
        else:
            pass

        print(f'''EVENT: WITHDRAW (after)--
                    {delegator_id=}, 
                    {delegator.holdings=}, 
                    {delegator.undelegated_tokens=}, 
                    {delegator.shares=}
                    {tokens=}
                    {withdrawableDelegatedTokens=}''')
    key = 'indexers'
    value = s['indexers']
    return key, value
