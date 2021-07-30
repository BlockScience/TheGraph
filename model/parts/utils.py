import pandas as pd
from decimal import Decimal

def convertFromLongStrToDecimal(d, field, GRT_conversion_rate):
    for events in d.values():
        for event in events:                       
            # sometimes it comes in as a number, sometimes as a string
            event[field] = str(event[field])

            # put in a decimal place 18 chars from the right then convert to double to avoid overflow error.
            try:
                event[field] = Decimal(event[field][:len(event[field]) - -GRT_conversion_rate] + "." + event[field][GRT_conversion_rate:])
            except:
                event[field] = Decimal(0)

def load_delegation_event_sequence_from_csv(path, blockNumberShift = 11474307, blocksPerEpoch = 6500, limit = None, GRT_conversion_rate = -18):
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
    # print(f'{d=}')
    
    convertFromLongStrToDecimal(d, 'tokens', GRT_conversion_rate)
    convertFromLongStrToDecimal(d, 'shares', GRT_conversion_rate) 

    # d['tokens'] = d['tokens'].apply(lambda x: int(x) * GRT_conversion_rate)
    print(f'loaded {path}.')
    return d
