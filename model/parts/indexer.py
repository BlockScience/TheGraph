from decimal import Decimal

class Indexer():
    def __init__(self, id, pool_delegated_stake = Decimal(0), shares = Decimal(0), pool_locked_stake = Decimal(0),
                indexer_revenue = Decimal(0), GRT = Decimal(0), cumulative_indexing_revenue = Decimal(0), 
                cumulative_query_revenue = Decimal(0), cumulative_non_indexer_revenue = Decimal(0),
                cumulative_deposited_stake = Decimal(0), initial_stake_deposited = False):
        self.id = id
        self.pool_delegated_stake = pool_delegated_stake
        self.shares = shares
        self.delegators = {} # key is delegator ID, value is delegator object.
        self.pool_locked_stake = pool_locked_stake
        self.indexer_revenue = indexer_revenue
        self.GRT = GRT
        self.cumulative_indexing_revenue = cumulative_indexing_revenue
        self.cumulative_query_revenue = cumulative_query_revenue
        self.cumulative_non_indexer_revenue = cumulative_non_indexer_revenue
        self.cumulative_deposited_stake = cumulative_deposited_stake
        self.initial_stake_deposited = initial_stake_deposited
        
        # query_fee_cut must be initialized by an event
        self.query_fee_cut = None
        
        # indexer_revenue_cut must be initialized by an event
        self.indexer_revenue_cut = None
        self.initial_stake_deposited = False 
        self.holdings = 0

        self.subgraphs = {} # key is subgraphDeploymentID, value is Subgraph

        self.buffered_rewards_assigned = 0 # this is indexing rewards--we cannot attribute to subgraph until allocationCloseds event