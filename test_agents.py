import pandas as pd
from model.sim_setup import SIMULATION_TIME_STEPS

df = pd.read_pickle(r'experiment.p')
df.reset_index(inplace=True)
pd.set_option('display.max_rows', None)


def show_final_results():
    delegator_one = list(df.iloc[SIMULATION_TIME_STEPS-1].indexers.values())[0].delegators[1]
    print(delegator_one)


def show_all_delegations():
    for timestep in range(1529):
        # delegator_one = list(df.iloc[timestep].indexers.values())[0].delegators[1]
        delegator_one = df.iloc[timestep].delegator_portfolios[1]
        # shares = delegate_front_runner.shares
        # holdings = delegate_front_runner.holdings
        # undelegated_tokens = delegate_front_runner.undelegated_tokens
        print(f'{timestep=}, {delegator_one.pretty_print()}')


if __name__ == '__main__':
    print("UNITTEST RESULTS")
    # show_final_results()

    show_all_delegations()
    # show here's when they acted, undelegated, delegated, here's what they made
    


