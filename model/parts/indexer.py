from decimal import Decimal
from model.parts.delegate_front_runner import DelegateFrontRunner
from model.parts.utility_delegator import UtilityDelegator, UtilityComponentsDelegator
from model.parts.delegate_front_runner_rules import DelegateFrontRunnerRules

from ..sys_params import params

initial_account_balance = params['delegator_initial_holdings'][0]
opportunity_cost = params['opportunity_cost'][0]
rules = DelegateFrontRunnerRules(initial_account_balance)

# G = how much will they delegate if they delegate
G = initial_account_balance

# TODO: Make interest_rate/opportunity_cost a param.
# this is the interest rate, r

amount_to_delegate = 1000000
components = UtilityComponentsDelegator(amount_to_delegate, opportunity_cost)


class Indexer:
    def __init__(self, indexer_id, pool_delegated_stake=Decimal(0), shares=Decimal(0), pool_locked_stake=Decimal(0),
                 # indexer_revenue=Decimal(0),
                 GRT=Decimal(0), ETH=Decimal(0), cumulative_indexing_revenue=Decimal(0),
                 cumulative_query_revenue=Decimal(0), cumulative_non_indexer_revenue=Decimal(0),
                 cumulative_deposited_stake=Decimal(0), initial_stake_deposited=False):
        self.id = indexer_id
        self.pool_delegated_stake = pool_delegated_stake
        self.shares = shares
        # self.delegators = {1: DelegateFrontRunner(1, rules, initial_account_balance)}  # key is delegator ID, value is delegator object.
        self.delegators = {1: UtilityDelegator(1, initial_account_balance, components)}  # key is delegator ID, value is delegator object.
        self.pool_locked_stake = pool_locked_stake

        # removed as not used.
        # self.indexer_revenue = indexer_revenue
        self.GRT = GRT
        self.ETH = ETH

        # cumulative_indexing_revenue is the sum of all component subgraphs' indexing revenue.
        self.cumulative_indexing_revenue = cumulative_indexing_revenue
        self.cumulative_query_revenue = cumulative_query_revenue
        self.cumulative_non_indexer_revenue = cumulative_non_indexer_revenue

        # cumulative_deposited_stake is the amount of indexer stake deposited til now.
        self.cumulative_deposited_stake = cumulative_deposited_stake
        self.initial_stake_deposited = initial_stake_deposited

        # query_fee_cut must be initialized by an event
        self.query_fee_cut = None

        # indexer_revenue_cut must be initialized by an event
        self.indexer_revenue_cut = None

        # initial_stake_deposited is a boolean saying whether the initial stake has been deposited
        self.initial_stake_deposited = False
        self.holdings = 0

        self.subgraphs = {}  # key is subgraphDeploymentID, value is Subgraph

        self.buffered_rewards_assigned = 0  # this is indexing rewards--we cannot attribute to subgraph until allocationCloseds event
        self.most_recent_indexing_reward = 0
