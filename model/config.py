from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim

from .psub import psubs
from .state import genesis_state
from .sys_params import params
from .sim_setup import SIMULATION_TIME_STEPS, MONTE_CARLO_RUNS

# Parameters
# Values are lists because they support sweeping.
simulation_config = config_sim({
        'N': MONTE_CARLO_RUNS, 
        'T': range(SIMULATION_TIME_STEPS), # number of timesteps
        'M': params,
})

exp = Experiment()

exp.append_configs(sim_configs=simulation_config,
                   initial_state=genesis_state,
                   partial_state_update_blocks=psubs)


# from cadCAD import configuration

# from .psub import psubs
# from .state import genesis_state
# from .sys_params import params

# # Parameters
# # Values are lists because they support sweeping.
# simulation_config = configuration.utils.config_sim({
#     "T": range(100),
#     "N": 1,
#     'M': params
# })

# exp = configuration.Experiment()

# exp.append_configs(sim_configs=simulation_config,
#                    initial_state=genesis_state,
#                    partial_state_update_blocks=psubs)