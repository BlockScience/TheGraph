import random
""" A Delegator is an actor who delegates native tokens to the revenue sharing pool
for shares in the revenue stream. """


class Delegator:
    # autoincrementing id.
    delegate_counter = 0

    def __init__(self, shares=0, reserve_token_holdings=0, expected_revenue=0, time_factor=2,
                 delegator_activity_rate=0.5):
        # initialize broker state
        self.id = Delegator.delegate_counter

        self.shares = shares
        self.revenue_token_holdings = 0
        self.reserve_token_holdings = reserve_token_holdings
        self.expected_revenue = expected_revenue
        self.time_factor = time_factor  # used to discount cash flows. 1 / (1 - discount_rate)
        self.delegator_activity_rate = delegator_activity_rate

        # increment counter for next delegator ID
        Delegator.delegate_counter += 1

    # member of the sharing pool (True/False)
    def is_member(self):
        return self.shares > 0

    def private_price_point(self, supply, owners_share, reserve_to_revenue_token_exchange_rate):
        """ take belief of revenue * your shares / total shares """
        revenue_per_period_per_share = self.expected_revenue * (1 - owners_share) * self.shares / \
            supply

        reserve_asset_per_period_per_share = revenue_per_period_per_share * \
            reserve_to_revenue_token_exchange_rate

        reserve_asset_per_share_time_corrected = reserve_asset_per_period_per_share * \
            self.time_factor

        return reserve_asset_per_share_time_corrected

    def will_act(self):
        # flip a uniform random variable, compare to activity, rate, if it's below, then set to act.
        rng = random.random()
        return rng < self.delegator_activity_rate
