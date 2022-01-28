import pandas as pd
import numpy as np

# import os
# import sys
# module_path = os.path.abspath(os.path.join('..'))
# print(module_path)
# sys.path.append(module_path)
# from .model.parts.utils import *
# import model.parts.utils
# from model.sys_params import *
from model.sim_setup import SIMULATION_TIME_STEPS

df = pd.read_pickle(r'experiment.p')
df.reset_index(inplace=True)
pd.set_option('display.max_rows', None)

if __name__ == '__main__':
    print("UNITTEST RESULTS")
    debug = False
    delegate_front_runner = list(df.iloc[SIMULATION_TIME_STEPS-1].indexers.values())[0].delegators[1]
    print(delegate_front_runner)
    # show here's when they acted, undelegated, delegated, here's what they made
    


