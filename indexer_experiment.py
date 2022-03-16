# This file is an alternative to running in a jupyter notebook.
from model import run
import sys
import pickle

# must import config even though it looks like it's not being used.
from model import config

sys.path.append("..")

df = run.run()
with open('index_spoofer_scenario_2.p', 'wb') as f:
    pickle.dump(df, f)


