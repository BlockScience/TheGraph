import pandas as pd


def get_value_private_price(delegator, supply, owners_share, reserve_to_revenue_token_exchange_rate, reserve, risk_adjustment):
    # NOTE: this is the discounted value of the dividends
    dividend_value = delegator.dividend_value(supply, owners_share, reserve_to_revenue_token_exchange_rate)

    # NOTE: this is the current spot price, from the invariant
    share_value = 2 * reserve / supply

    risk_adjusted_share_value = share_value * risk_adjustment

    value_private_prices = dividend_value + risk_adjusted_share_value

    # print(f'{timestep=}, {private_price=}')
    return value_private_prices


def get_regression_to_mean_price(last_n_spot_prices, halflife):
    """
    exponential moving average at last timestep, over past 14 days
    the idea is that the spot_price reverts to this mean.
    """

    # print(f'{sL=}')
    regression_to_mean_price = 0
    if not last_n_spot_prices.empty:
        regression_to_mean_price = last_n_spot_prices.ewm(halflife=halflife).mean().iloc[-1]
        # print(f'{exponential_moving_average=}')
        # print(f'{last_n_spot_prices=}')

    return regression_to_mean_price


def get_trendline_price(last_n_spot_prices, halflife):
    # TODO: implement this
    trendline_price = 0
    if not last_n_spot_prices.empty:
        trendline_price = last_n_spot_prices + last_n_spot_prices.diff().ewm(halflife=halflife).mean()
    return trendline_price


def compute_and_store_private_prices(params, step, sL, s, inputs):
    """
    There are 3 components to private price for a typical market actor.
    1) regression to mean (smooth weighted average)
    2) private price
    3) trendline price
    """
    delegators = s['delegators']
    supply = s['supply']
    reserve = s['reserve']
    timestep = s['timestep']
    owners_share = params['owners_share']
    risk_adjustment = params['risk_adjustment']
    num_days_for_trends = params['num_days_for_trends']
    reserve_to_revenue_token_exchange_rate = params['reserve_to_revenue_token_exchange_rate']
    halflife = params['halflife']

    # earliest index to consider for trend analysis
    earliest_index = -num_days_for_trends - 1

    # -1 is last substep
    last_n_spot_prices_list = [state[-1]['spot_price'] for state in sL[earliest_index:-1]]
    last_n_spot_prices = pd.DataFrame({'spot_price': last_n_spot_prices_list})

    for delegator in delegators.values():
        delegator.regression_to_mean_prices[timestep] = get_regression_to_mean_price(last_n_spot_prices, halflife)
        delegator.value_private_prices[timestep] = get_value_private_price(delegator, supply, owners_share,
                                                                           reserve_to_revenue_token_exchange_rate, reserve, risk_adjustment)
        delegator.trendline_prices[timestep] = get_trendline_price(last_n_spot_prices, halflife)
        delegator.private_prices[timestep] = (delegator.regression_to_mean_prices[timestep] * delegator.component_weights[0] +
                                              delegator.value_private_prices[timestep] * delegator.component_weights[1] +
                                              delegator.trendline_prices[timestep] * delegator.component_weights[2])

        print(f'{delegator.regression_to_mean_prices[timestep]=}')
        print(f'{delegator.value_private_prices[timestep]=}')
        print(f'{delegator.trendline_prices[timestep]=}')
        print(f'{delegator.private_prices[timestep]=}')

    # print(delegators)
    key = 'delegators'
    value = delegators
    return key, value
