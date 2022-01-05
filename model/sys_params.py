from .parts import utils
from decimal import *
from sys import platform

R_i_rate = [0.03]

indexer_allocation_rate = [0.0050]  # ASSUMED share of GRT minted by subgraph by indexer

# 100 timesteps/blocks per day/epoch
blocks_per_epoch = 6500
unbonding_days = 28
unbonding_timeblock = [unbonding_days*blocks_per_epoch]
dispute_channel_epochs = 7
allocation_days = [28]
# represents multiply by 10e-18 to get GRT
GRT_conversion_rate = -18
# delegation tax rate is 0.5% as documented here: https://thegraph.com/docs/delegating#delegation-risks 
delegation_tax_rate = [Decimal(0.005)]
delegation_leverage = [16]
delegator_initial_holdings = [Decimal(10e9)]

# TODO: this will come from allocation file
# these are indexer cuts
# query_fee_cut = [Decimal(0.8)]
# indexer_revenue_cut = [Decimal(0.8)]
agent_event_path = None

# 1 indexer
event_path = 'another_indexer/single_indexer/singleIndexer.csv'
# event_path = 'another_indexer/single_indexer/singleIndexer_200events_a.csv'
# event_path = 'GraphQL_data/singleIndexer.csv'

# 2 indexers
# event_path = 'multiple_indexer/multipleIndexer.csv'

# event_path = 'multiple_indexer/3indexer/3indexer.csv'
# agent_event_path = 'multiple_indexer/agent_events/agent_events.csv'
# event_path = 'multiple_indexer/allindexer/allEvents.csv'

delegation_events, undelegation_events, withdraw_events, allocation_closed_events, \
        allocation_collected_events, stake_deposited_events, rewards_assigned_events, \
        delegation_parameter_events, \
        allocation_created_events, all_events = utils.load_all_events(event_path, agent_event_path)

# print(delegation_events)
params = {
        "r_del": [10],        #	Indexer’s initial delegated stake
        "s_del": [10],        # Indexer’s initial delegated stake share of pool
        "expected_revenue": [7],
        "arrival_rate": [0.5],
        "expected_initial_token_holdings": [25],
        "delegator_estimation_noise_mean": [0],
        "delegator_estimation_noise_variance": [1],  # proportional to expected_revenue
        "pool_delegated_stake_to_revenue_token_exchange_rate": [1],
        "mininum_required_price_pct_diff_to_act": [0.02],
        "risk_adjustment": [0.7],  # cut 30% of the value off due to risk
        'delegation_tax_rate': delegation_tax_rate, # Beta_del: tax percentage from delegated tokens to be burned
        'unbonding_timeblock': unbonding_timeblock, # time unbonded tokens are frozen from being eligible to be withdrawn
        'delegation_leverage': delegation_leverage, # tax percentage from delegated tokens to be burned
        'R_i_rate': R_i_rate, # indexer reward revenue rate (inflationary rewards)
        'allocation_days': allocation_days, # time for allocation
        'indexer_allocation_rate': indexer_allocation_rate, # ASSUMED share of minted by subgraph by indexer
        'delegation_tokens_events': [delegation_events],
        'undelegation_shares_events': [undelegation_events],
        'withdraw_tokens_events': [withdraw_events],
        'allocation_closed_events': [allocation_closed_events],
        'allocation_collected_events': [allocation_collected_events],
        'stake_deposited_events': [stake_deposited_events],
        'rewards_assigned_events': [rewards_assigned_events],
        'delegation_parameter_events': [delegation_parameter_events],
        'delegator_initial_holdings': delegator_initial_holdings,
        'allocation_created_events': [allocation_created_events],
        'all_events': [all_events],
        'blocks_per_epoch': [blocks_per_epoch],
        'dispute_channel_epochs': [dispute_channel_epochs],
        'unbonding_days': [unbonding_days],
}
