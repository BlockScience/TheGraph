### This file is an alternative to running in a jupyter notebook.

import pandas as pd
import numpy as np
from model import config


pd.options.display.float_format = '{:.2f}'.format

from model import run
df = run.run()
import pickle
with open('experiment.p', 'wb') as f:
    pickle.dump(df, f)
df
