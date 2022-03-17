from decimal import Decimal
import random
def check_to_slash(params, step, sL, s, inputs):
    key = 'indexers'
    indexers = s['indexers']
    for indexer_id in indexers.keys():
        if indexers[indexer_id].indexer_revenue_cut is not None:
            if indexer_id in indexers[indexer_id].delegators.keys()\
                and indexers[indexer_id].indexer_revenue_cut > Decimal(0.99):
                should_slash = random.random()
                if should_slash < params['slashing_chance']:
                    indexers[indexer_id].cumulative_deposited_stake -= \
                   indexers[indexer_id].cumulative_deposited_stake * params['slashing_percentage']

    value = indexers
    return key, value 