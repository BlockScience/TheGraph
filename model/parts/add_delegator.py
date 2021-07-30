from . import delegator
import random
import scipy.stats as stats


# policy
def should_instantiate_delegate(params, step, sL, s):
    # flip a coin (1 joins if there's room and random says to)
    should_instantiate_delegate = False

    rng = random.random()
    if rng >= params['arrival_rate']:
        should_instantiate_delegate = True

    return {"should_instantiate_delegate": should_instantiate_delegate}
