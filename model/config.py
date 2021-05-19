# from cadCAD import configuration
from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim

from .psub import psubs
from .state import genesis_state
from .sys_params import params


# Parameters
# Values are lists because they support sweeping.
simulation_config = config_sim({
    "T": range(90),
    "N": 1,
    'M': params
})

exp = Experiment()

exp.append_configs(sim_configs=simulation_config,
                   initial_state=genesis_state,
                   partial_state_update_blocks=psubs)
