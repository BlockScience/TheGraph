import pandas as pd

def load_delegation_event_sequence_from_csv(path, blockNumberShift = 11474307, blocksPerEpoch = 6500, limit = None):
    df = pd.read_csv(path)
    # limit number of records read in 
    if limit is not None:
        df = df.head(limit)
    else:
        pass
    # print(f'loading {path}...')
    
    # create new 
    df['timestep'] = (df.blockNumber - blockNumberShift) / blocksPerEpoch + 1
    df.timestep = df.timestep.astype(int)
    
    # set the index to timestep inplace and don't drop timestep from the df.
    df.set_index('timestep', inplace=True, drop=False)

    # create a dict from the df where duplicate timesteps appear in a list of dicts under the same timestep index.
    d = df.groupby(level=0).apply(lambda x: x.to_dict('records')).to_dict()

    print(f'loaded {path}.')
    return d
