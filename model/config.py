from cadCAD import configuration

from .psub import psubs
from .state import genesis_state

# Parameters
# Values are lists because they support sweeping.
simulation_config = configuration.utils.config_sim({
    "T": range(90),
    "N": 1,
    'M': {
#         "required_stake": [5],        # S_min
#         "epoch_length": [1],          # in days
#         "min_epochs": [28],           # tau
#         "allocation_per_epoch": [25],
#         "min_horizon": [7],           # H_min
#         "min_brokers": [3],           # n_min
#         "max_brokers": [5],           # n_max
        "initial_reserve": [10],
        "expected_revenue": [3],
        "owners_share": [0.25],         # 1-theta  (theta is what all of the other delegators get)
        "arrival_rate": [0.5],
        "expected_reserve_token_holdings": [5],
        "delegator_estimation_noise_mean": [0],
        "delegator_estimation_noise_variance": [1],  # proportional to expected_revenue
        "reserve_to_revenue_token_exchange_rate": [1],
        "delegator_activity_rate": [0.5],
    }
})

exp = configuration.Experiment()

exp.append_configs(sim_configs=simulation_config,
                   initial_state=genesis_state,
                   partial_state_update_blocks=psubs)
