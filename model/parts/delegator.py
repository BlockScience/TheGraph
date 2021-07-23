import random
""" A Delegator is an actor who delegates native tokens to the revenue sharing pool
for shares in the revenue stream. """


class Delegator(object):
    # autoincrementing id.
    delegate_counter = 0

    def __init__(self, shares=0, holdings=0, expected_revenue=0, discount_rate=.9,
                 delegator_activity_rate=0.5, minimum_shares=0):
        # initialize delegator state
        self.id = Delegator.delegate_counter

        self.shares = shares

        # Tokens locked in delegation, d
        self.delegated_tokens = 0
        
        # Tokens locked in undelegation, l  
        self.undelegated_tokens = 0

        # Freeze time (measure in block time)
        self.locked_until = 0

        # Amount of free/withdrawn token the delegator is holding, h
        self.holdings = holdings

        # self.expected_revenue = expected_revenue

        # used to discount cash flows. 1 / (1 - discount_rate)
        self.time_factor = 1 / (1 - discount_rate)
        
        # self.delegator_activity_rate = delegator_activity_rate

        self.minimum_shares = minimum_shares

        # increment counter for next delegator ID
        Delegator.delegate_counter += 1

    
   
    # member of the sharing pool (True/False)
    def is_member(self):
        return self.shares > 0

    def getWithdrawableDelegatedTokens(self, timestep):
        if timestep > self.locked_until:
            return self.undelegated_tokens

    def withdraw(self):
        self.holdings += self.undelegated_tokens
        self.undelegated_tokens = 0
        self.locked_until = 0


    def set_undelegated_tokens(self, unbonding_timeblock, undelegated_tokens):
        self.undelegated_tokens = undelegated_tokens
        self.locked_until = unbonding_timeblock
   
    def will_act(self):
        # flip a uniform random variable, compare to activity, rate, if it's below, then set to act.
        rng = random.random()
        return rng < self.delegator_activity_rate

    def collectDelegationQueryRewards(self):
        return 0
    def collectDelegationIndexingRewards(self):
        return 0

