from model.parts.abstract_agent import AbstractAgent
""" A Delegator is an actor who delegates native tokens to the revenue sharing pool
for shares in the revenue stream. """


class Delegator(AbstractAgent):
    def __init__(self, delegator_id, shares=0, holdings=0,
                 minimum_shares=0):
        super().__init__(delegator_id)

        self.shares = shares

        # Amount of free/withdrawn token the delegator is holding, h
        self.holdings = holdings

        # Epoch at which undelegation is allowed
        self.locked_in_delegation_until = 0

        # Tokens locked in undelegation, l
        self.undelegated_tokens = 0

        # Epoch at which withdraw is allowed
        self.locked_in_undelegation_until = 0

        # Not allowed to sell below this amount
        self.minimum_shares = minimum_shares

        self.epoch_of_last_action = 0
        self.has_rewards_assigned_since_delegation = False

    def __repr__(self):
        return f'{self.id=}, {self.shares=}, {self.holdings=}, {self.undelegated_tokens=}, {self.plan=}'

    def get_withdrawable_delegated_tokens(self, epoch):
        if epoch > self.locked_in_undelegation_until:
            return self.undelegated_tokens
        else:
            return 0

    def withdraw(self, tokens):
        self.holdings += tokens
        self.undelegated_tokens -= tokens
        self.locked_in_undelegation_until = 0

    def set_undelegated_tokens(self, until, undelegated_tokens):
        self.undelegated_tokens += undelegated_tokens
        self.locked_in_undelegation_until = until

    def beliefs(self):
        return None
        
    # def updateState(self): #, states : states, inputs : inputs):
    #     pass
    
    def update_beliefs(self):
        return None
    
    def generate_strategies(self):
        return None
    
    def generate_plan(self):
        pass
    
    def select_plan(self):
        pass
    
    def generate_output(self, plan):
        pass

    def is_delegated(self):
        return self.shares > 0

    def is_undelegated(self):
        return self.undelegated_tokens > 0
