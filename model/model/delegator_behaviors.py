import random


def may_act_this_timestep(params, step, sL, s):
    acting_delegator_ids = []
    for id, delegator in s['delegators'].items():
        if delegator.will_act():
            acting_delegator_ids.insert(id)

    # randomize list.
    random.shuffle(acting_delegator_ids)

    return {'acting_delegator_ids': acting_delegator_ids}


def act(params, step, sL, s, inputs):    
    #  loop through acting delegators id list
    
    for inputs['acting_delegator_ids']:
        # within the loop, delegators will first
        #   accounting of current state

        #   previous actor will have changed it
        #   active delegator computes their evaluation (private price)
        #   compare private price to spot price -- just changed
        #  look at difference between spot and private price. 
        #    if it's low, buy.  close, do nothing.  high, sell
        #  if sell, compute amount of shares to burn such that realized price is equal to private price
        #    if that amount is > amt i have, burn it all (no short sales)
        #  if buy, compute amount of reserve to add such that realized price is equal to private price
        #    if the amount is greater than reserve assets i have personally, then do it all
        # 



    should_make_claims = inputs['should_make_claims']
    # apply each claim




    for broker_id, should_make_claim in should_make_claims.items():
        if should_make_claim:
            s['brokers'][broker_id].holdings += \
                 s['brokers'][broker_id].claimable_funds
            s['brokers'][broker_id].claimable_funds = 0

    key = 'make_claims'
    value = s['brokers']
    return key, value

