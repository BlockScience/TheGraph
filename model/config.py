from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim
from cadCAD import configs
# from .state_variables import initial_state
# from .partial_state_update_block import partial_state_update_block
from .sys_params import params 
from .sim_setup import SIMULATION_TIME_STEPS, MONTE_CARLO_RUNS
from .psub import psubs
from .state import genesis_state

print(configs)

sim_config = config_sim(
    {
        'N': MONTE_CARLO_RUNS, 
        'T': range(SIMULATION_TIME_STEPS), # number of timesteps
        'M': params,
    }
)

exp = Experiment()

exp.append_configs(
    sim_configs=sim_config,
    initial_state=genesis_state,
    partial_state_update_blocks=psubs
    # config_list=configs
    )

print(configs)
