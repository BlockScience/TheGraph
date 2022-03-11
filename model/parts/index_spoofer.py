from .heuristic_agent import HeuristicAgent
from .index_spoofer_rules import IndexSpoofingRules
from decimal import Decimal

class IndexSpoofer(HeuristicAgent):
    def __init__(self, indexer_id, rules: IndexSpoofingRules,
                initialaccount_balance):
        super().__init__(indexer_id, rules, initialaccount_balance)
        self._inputs = []
        self._states = [
            {
                'stake': {},
                # 'subgraphs': {},
                # 'available_funds': initialaccount_balance,
                # 'timeWaited': {}
            }
        ]

    def inputs(self, newInput):
        self._inputs.append(
            {
                'available_subgraphs': newInput['available_subgraphs'],
                'currentPeriod': newInput['currentPeriod'],
                'delegation_unbonding_period': newInput['delegation_unbonding_period'],
                'account_balance': newInput['account_balance']
            }
        )

    def generate_plan(self):
        if self.output:
            self.plan = {}
            return

        strategy        = self._strategies[-1]
        inpt            = self._inputs[-1]
    
        plan = {}
        current_period = inpt['currentPeriod']
        staked = self.cumulative_deposited_stake > 0
        delegated = self.delegators[1].shares > 0
        funds = self.GRT
        indexer_revenue = self.indexer_revenue_cut
        allocated_subgraph = self.subgraphs
        index_rewards = self.buffered_rewards_assigned
        rewardTransferred = 0
        print(indexer_revenue)
        if allocated_subgraph['1'].allocations == {}  and inpt['available_subgraphs']:
            for avail_subgraph in inpt['available_subgraphs'].keys():
                open_allocations = [allocation for allocation in inpt['available_subgraphs'][avail_subgraph].allocations.values() if allocation.tokens != 0]
                allocations = [allocation for allocation in inpt['available_subgraphs'][avail_subgraph].allocations.values()]
                if len(open_allocations) == 0 and inpt['available_subgraphs']:
                        if staked and strategy['delegate']['tokens'] > self.delegators[1].holdings:
                            # delegate to self
                            if strategy['delegate']['tokens'] <= self.delegators[1].holdings:
                                plan = strategy['delegate']
                                plan['indexer'] = self.id
                                plan['delegator'] = self.id
                                plan['tokens'] = self.delegators[1].holdings / Decimal(1.1)
                                plan['allocationID'] = '1'
                                plan['subgraphDeploymentID'] = avail_subgraph
                                self.plan = plan
                                return
                        elif not delegated and strategy['stake']['tokens'] > funds:
                            # create an ownIndexer stake
                            if strategy['stake']['tokens'] <= funds:
                                plan = strategy['stake']
                                plan['indexer'] = self.id
                                plan['delegator'] = self.id
                                plan['tokens'] = funds / Decimal(1.1)
                                plan['subgraphDeploymentID'] = avail_subgraph
                                self.plan = plan
                                return
                            # have staked and delegated, so open an allocation
                        else:
                            if strategy['open']['tokens'] <= funds:
                                plan = strategy['open']
                                plan['indexer'] = self.id
                                plan['epoch'] = current_period
                                plan['allocationID'] = '1'
                                plan['subgraphDeploymentID'] = avail_subgraph
                                plan['tokens'] = funds / Decimal(1.1)
                                self.plan = plan
                                return
                                #plan['queryFeeCut'] = 0.99
                                #plan['indexingRewardCut'] = 0.99
            self.plan = plan
        elif inpt['available_subgraphs']:
            for avail_subgraph in inpt['available_subgraphs'].keys():
                allocations = [allocation for allocation in inpt['available_subgraphs'][avail_subgraph].allocations.values() if allocation.tokens != 0]
                plan = {}
                if avail_subgraph not in allocated_subgraph.keys():
                    if strategy['open']['tokens'] <= funds:
                        plan = strategy['open']
                        plan['indexer'] = self.id
                        plan['epoch'] = current_period
                        plan['allocationID'] = '1'
                        plan['subgraphDeploymentID'] = avail_subgraph
                        plan['tokens'] = funds / Decimal(1.1)
                        self.plan = plan
                        return
                        #plan['queryFeeCut'] = 0.99
                        #plan['indexingRewardCut'] = 0.99                          
                else:
                    if indexer_revenue is None:
                        # set indexingRewardCut for this subgraph's allocation
                        plan = strategy['set_cut']
                        plan['queryFeeCut'] = 1
                        plan['indexingRewardCut'] = 1
                        plan['indexer'] = self.id
                        self.plan = plan
                        return
                    else:
                        for allocation in allocations:
                            if current_period - allocation.start_period < strategy['wait']['timeWaited']:
                            # wait according to agent preferences on waiting time, timeWaited
                                # plan = strategy['wait']
                                # plan['indexer']  = self.id
                                # plan['subgraphDeploymentID'] = avail_subgraph
                                pass
                            else:
                                #print(index_rewards)
                                # if index_rewards <= Decimal(0.0000001):
                                #    plan = strategy['give_rewards']
                                #    plan['indexer'] = self.id
                                #    plan['amount'] = allocation.tokens * Decimal(0.05)
                                #    self.plan = plan
                                #    rewardTransferred += 1
                                #    return
                                if allocation.tokens != 0:
                                    if indexer_revenue != 0:
                                    # waited long enough,  switch reward cut to zero
                                        plan = strategy['set_cut']
                                        plan['indexer'] = self.id
                                        plan['queryFeeCut'] = 0
                                        plan['indexingRewardCut'] = 0
                                        self.plan = plan
                                        rewardTransferred += 1
                                        return
                                    else:
                                        # waited long enough and index cut is zero, close the allocation
                                        plan = strategy['close']
                                        plan['indexer'] = self.id
                                        plan['allocationID'] = '1'
                                        plan['subgraphDeploymentID'] = avail_subgraph
                                        self.plan = plan
                                        return
            if plan: 
                self.plan = plan
            if rewardTransferred == len(allocated_subgraph) and len(allocated_subgraph) > 0:
                plan = {}
                allocations = [allocation for allocation in inpt['available_subgraphs'][list(inpt['available_subgraphs'].keys())[0]].allocations.values() if allocation.tokens != 0]
                for allocation in allocations:
                    if current_period >= allocation.start_period + inpt['delegation_unbonding_period']:
                        plan = strategy['withdraw']
                        plan['indexer'] = self.id
                        plan['delegator'] = self.id
                        plan['tokens'] = Decimal(1)
                        self.plan = plan
                        return
                    else:
                        # rewards have been distributed, undelegate
                        plan = strategy['undelegate']
                        plan['indexer'] = self.id
                        plan['delegator'] = self.id
                        plan['shares'] = self.shares
                        plan['until'] = current_period + inpt['delegation_unbonding_period']
                        self.plan = plan
                        return
                if plan: 
                    self.plan = plan
                    
        self.plan = plan

    def generate_output(self):
        self.output = []
        if self.plan:
            # output must be a list of events.
            self.output.append(self.plan)
        