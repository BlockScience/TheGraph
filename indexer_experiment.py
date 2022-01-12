### This file is an alternative to running in a jupyter notebook.

import pandas as pd
import numpy as np
from model import config
import cProfile
from pstats import Stats, SortKey

do_profiling = True
if do_profiling:
    with cProfile.Profile() as pr:
        pd.options.display.float_format = '{:.2f}'.format

        from model import run
        df = run.run()
        import pickle
        with open('experiment.p', 'wb') as f:
            pickle.dump(df, f)

        with open('profiling_stats.txt', 'w') as stream:
            stats = Stats(pr, stream=stream)
            stats.strip_dirs()
            # stats.sort_stats('time')
            stats.sort_stats('time')
            stats.dump_stats('.prof_stats')
            stats.print_stats()