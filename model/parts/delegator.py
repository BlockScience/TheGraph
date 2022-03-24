# A Delegator is really a delegation now and not a delegator.  A portfolio is a delegator that can delegate to many delegations.
class Delegator:
    def __init__(self, delegator_id, shares=0):
        # super().__init__(delegator_id)

        self.shares = shares

        # Epoch at which undelegation is allowed
        self.locked_in_delegation_until = 0

        # Tokens locked in undelegation, l2222222
        self.undelegated_tokens = 0

        # Epoch at which withdraw is allowed
        self.locked_in_undelegation_until = 0

        self.has_rewards_assigned_since_delegation = False

    def __repr__(self):
        return f'{self.id=}, {self.shares=}, {self.holdings=}, {self.undelegated_tokens=}, {self.plan=}'

    def get_withdrawable_delegated_tokens(self, epoch):
        if epoch >= self.locked_in_undelegation_until:
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

    def is_delegated(self):
        return self.shares > 0

    def is_undelegated(self):
        return self.undelegated_tokens > 0
