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

        self.shares = 0

        # Tokens locked in delegation, d
        self.delegated_tokens = 0
        
        # Tokens locked in undelegation, l.  {key=locked_until_timestep, value=num_tokens}
        self._undelegated_tokens = {}

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

    # property tag makes it so you can call it without parentheses ()
    @property
    def unvested_shares(self):
        return sum(s for s in self._unvested_shares.values())

    @property
    def shares(self):
        return self.unvested_shares + self.vested_shares

    def set_shares(self, timestep, shares):
        self._unvested_shares[timestep] = shares

    def dividend_value(self, shares, indexer_revenue_cut, total_delegated_stake_to_revenue_token_exchange_rate):
        """ take belief of revenue * your shares / total shares """
        revenue_per_period_per_share = 0
        # if shares > 0:
        #     # this is always 0 if self.shares = 0
        #     revenue_per_period_per_share = self.expected_revenue * (1 - indexer_revenue_cut) * self.shares / shares

        assert(shares > 0)

        # owners share is resolved before any share percentage calculation
        revenue_per_period_per_share = self.expected_revenue * (1 - indexer_revenue_cut) / shares

        total_delegated_stake_asset_per_period_per_share = revenue_per_period_per_share * \
            total_delegated_stake_to_revenue_token_exchange_rate

        total_delegated_stake_asset_per_share_time_corrected = total_delegated_stake_asset_per_period_per_share * \
            self.time_factor

        # print(f'dividend_value: {self.id=}, {shares=}, {self.expected_revenue=}, {revenue_per_period_per_share=}, \
        #     {total_delegated_stake_asset_per_period_per_share=}, {total_delegated_stake_asset_per_share_time_corrected=}')
        return total_delegated_stake_asset_per_share_time_corrected

    
    def will_act(self):
        # flip a uniform random variable, compare to activity, rate, if it's below, then set to act.
        rng = random.random()
        return rng < self.delegator_activity_rate

    def delegate(self):
        # f is free tokens or self.revenue_token_holdings
        # f+ = f - delta_d
        # TODO: figure out how many tokens are delegated
        delegated_tokens = 5
        self.revenue_token_holdings = self.revenue_token_holdings - delegated_tokens
        # d+ = d + delta_d
        self.holdings  = 
        tax = delta_d * beta_del
        GRT+ = GRT - tax
        D+ = D + delta_d * (1-beta_del)
        deltaS = delta_d*(1-beta_del)*D*S
        S+ = S + delta_s
        s+ = s + delta_s

        return 0
    def undelegate(self):
        return 0
    def withdraw(self):
        return 0
    def collectDelegationQueryRewards(self):
        return 0
    def collectDelegationIndexingRewards(self):
        return 0

#     def buy_shares(self, shares, total_delegated_stake, spot_price,
#                     mininum_required_price_pct_diff_to_act,
#                     timestep, delegation_tax):
#         """
#             compare private price to spot price -- just changed
#             look at difference between spot and private price.
#             if it's low, buy.  close, do nothing.  high, sell
#             if sell, compute amount of shares to burn such that realized price is equal to private price
#             if that amount is > amt i have, burn it all (no short sales)
#         """                    
#         private_price = self.private_prices[timestep]
#         pct_price_diff = 0
#         if spot_price > 0:
#             pct_price_diff = abs((private_price - spot_price) / spot_price)

#         created_shares = 0
#         added_total_delegated_stake = 0
#         # print(f'buy_or_sell: DELEGATOR {self.id} -- {private_price=}, {spot_price=}, {pct_price_diff=}, {self.total_delegated_stake_token_holdings=}, {self.shares=}')
#         if pct_price_diff < mininum_required_price_pct_diff_to_act:
#             # don't act.
#             return created_shares, added_total_delegated_stake

#         if private_price > spot_price:
#             # print(f'buy_or_sell: DELEGATOR {self.id} -- WANTS TO BUY')
#             # BUY ###
#             # figure out how much delegator spending, then buy it

#             # this formula, not used, is when the delegator buys until private_price == realized_price
#             # added_total_delegated_stake = (private_price * shares * (private_price * shares - 2 * total_delegated_stake))/total_delegated_stake
#             # created_shares = shares * ((1 + added_total_delegated_stake / total_delegated_stake) ^ (1/2)) - shares
#             # assert(private_price == realized_price)

#             # this formula stops buying when spot_price is equal to private_price
#             added_total_delegated_stake = (private_price * shares) - total_delegated_stake

#             # can't spend total_delegated_stake you don't have
#             if added_total_delegated_stake > self.total_delegated_stake_token_holdings:
#                 added_total_delegated_stake = self.total_delegated_stake_token_holdings
#             created_shares = shares * (added_total_delegated_stake * (1 - delegation_tax)) / total_delegated_stake
#             self._unvested_shares[timestep] = created_shares
#             # print('shares',shares)

#             # then update the state

#             # delegator:
#             #   increasing shares
#             #   decreasing total_delegated_stake_token_holdings
#             # system:
#             #   increasing total shares
#             #   increasing total_delegated_stake

#         elif private_price < spot_price:
#             # SELL ###
#             # print(f'buy_or_sell: DELEGATOR {self.id} -- WANTS TO SELL')
#             burned_shares = ((2 * total_delegated_stake * shares) - (private_price * shares ** 2)) / (2 * total_delegated_stake)

#             # can only sell vested shares
#             shares_count = self.vested_shares

#             # can't burn shares you don't have.
#             if burned_shares > shares_count:
#                 burned_shares = shares_count

#             # can't burn shares you're not allowed to burn (original delegator's 10)
#             if shares_count - burned_shares < self.minimum_shares:
#                 burned_shares = shares_count - self.minimum_shares

#             created_shares = -burned_shares
#             # payout
#             total_delegated_stake_paid_out = total_delegated_stake - total_delegated_stake * (1 - burned_shares / shares) ** 2
#             added_total_delegated_stake = -total_delegated_stake_paid_out

#             self.vested_shares -= burned_shares
            
#             # delegator:
#             #   decreasing shares
#             #   increasing total_delegated_stake_token_holdings
#             # system:
#             #   decreasing total shares
#             #   decreasing total_delegated_stake
        
#         # final_spot_price = (2 * (total_delegated_stake + added_total_delegated_stake)) / (shares + created_shares)
#         # acceptable_tolerance = mininum_required_price_pct_diff_to_act
#         # diff = abs(private_price - final_spot_price)
#         # print(f'buy_or_sell: DELEGATOR {self.id} -- {private_price=}, {final_spot_price=}, {diff=}, {acceptable_tolerance=}')
        
#         # NOTE: we cannot assert(diff < acceptable_tolerance) for all cases because the diff won't be less than acceptable_tolerance in all cases
#         # for example: the delegator is not allowed to sell due to a minimum number of shares.
#         # assert(diff < acceptable_tolerance)

#         self.total_delegated_stake_token_holdings -= added_total_delegated_stake

#         # if created_shares > 0:
#         #     print(f'buy_or_sell: DELEGATOR {self.id} -- BOUGHT {created_shares=} for {added_total_delegated_stake=}')
#         # elif created_shares < 0:
#         #     print(f'buy_or_sell: DELEGATOR {self.id} -- SOLD {created_shares=} for {added_total_delegated_stake=}')

#         return created_shares, added_total_delegated_stake

# # test that i input a value of dR, i get the right value of dS
