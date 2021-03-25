def get_value_private_price(delegator, supply, owners_share, reserve_to_revenue_token_exchange_rate, reserve, risk_adjustment):
    # NOTE: this is the discounted value of the dividends
    dividend_value = delegator.dividend_value(supply, owners_share, reserve_to_revenue_token_exchange_rate)

    # NOTE: this is the current spot price, from the invariant
    share_value = 2 * reserve / supply

    risk_adjusted_share_value = share_value * risk_adjustment

    value_private_prices = dividend_value + risk_adjusted_share_value

    # print(f'{timestep=}, {private_price=}')
    return value_private_prices


def get_regression_to_mean_price(previous_avg_price, spot_price, smoothing_factor):
    """
    exponential moving average at last timestep, over past 14 days
    the idea is that the spot_price reverts to this mean.
    avg_price(t) = (1-alpha) * avg_price(t-1) + alpha * price(t)
    """

    # print(f'{sL=}')
    regression_to_mean_price = 0
    if previous_avg_price:

        regression_to_mean_price = (1 - smoothing_factor) * previous_avg_price + smoothing_factor * spot_price
    return regression_to_mean_price


def get_trendline_price(spot_price, regression_to_mean_price):
    # TODO: implement this
    # trend_price = price + price.diff().ewm(halflife = param['halflife']).mean()
    trendline_price = 0

    # if not last_n_spot_prices.empty:
    #     trendline_price = last_n_spot_prices + last_n_spot_prices.diff().ewm(halflife=halflife).mean()
    # if regression_to_mean_price is higher than spot price, we think it will trend higher
    trendline_price = spot_price + (spot_price - regression_to_mean_price)

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
    # num_days_for_trends = params['num_days_for_trends']
    reserve_to_revenue_token_exchange_rate = params['reserve_to_revenue_token_exchange_rate']

    # halflife = params['halflife']
    smoothing_factor = params['smoothing_factor']
    spot_price = s['spot_price']

    # # earliest index to consider for trend analysis
    # earliest_index = -num_days_for_trends - 1

    # # -1 is last substep
    # last_n_spot_prices_list = [state[-1]['spot_price'] for state in sL[earliest_index:-1]]
    # last_n_spot_prices = pd.DataFrame({'spot_price': last_n_spot_prices_list})
    for delegator in delegators.values():
        # non-time series calculations
        delegator.value_private_prices[timestep] = get_value_private_price(delegator, supply, owners_share,
                                                                           reserve_to_revenue_token_exchange_rate, reserve, risk_adjustment)
        # print(f'{delegator.value_private_prices[timestep]=}')

        # time series_calculations
        if timestep-1 in delegator.regression_to_mean_prices:
            previous_avg_price = delegator.regression_to_mean_prices[timestep-1]
            delegator.regression_to_mean_prices[timestep] = get_regression_to_mean_price(previous_avg_price, spot_price, smoothing_factor)

            delegator.trendline_prices[timestep] = get_trendline_price(spot_price, delegator.regression_to_mean_prices[timestep])

            delegator.private_prices[timestep] = (delegator.regression_to_mean_prices[timestep] * delegator.component_weights[0] +
                                                  delegator.value_private_prices[timestep] * delegator.component_weights[1] +
                                                  delegator.trendline_prices[timestep] * delegator.component_weights[2])

            # print(f'{delegator.regression_to_mean_prices[timestep]=}')
            # print(f'{delegator.trendline_prices[timestep]=}')
            # print(f'{delegator.private_prices[timestep]=}')

        else:
            # NOTE: have to initialize this somehow or it is never calculated as it's based on prior values.
            delegator.regression_to_mean_prices[timestep] = spot_price

            delegator.private_prices[timestep] = delegator.value_private_prices[timestep]

    # print(delegators)
    key = 'delegators'
    value = delegators
    return key, value
