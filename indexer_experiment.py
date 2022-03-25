# This file is an alternative to running in a jupyter notebook.
from model import run
import sys
import pickle

# must import config even though it looks like it's not being used.
from model import config

sys.path.append("..")

df = run.run()
with open('index_spoofer_scen_3_no_slash_slash_pct.p', 'wb') as f:
    pickle.dump(df, f)

with open('index_spoofer_scen_3_no_slash_slash_pct_config.p', 'wb') as fp:
    pickle.dump(config.simulation_config, fp)
# scen_3_config = config.simulation_config
