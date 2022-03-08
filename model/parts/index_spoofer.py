from .heuristic_agent import HeuristicAgent
from .index_spoofer_rules import IndexSpoofingRules

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

        state           = self._states[-1]
        strategy        = self._strategies[-1]
        inpt            = self._inputs[-1]
    
        plan = {}
        current_period = inpt['currentPeriod']
        staked = self.cumulative_deposited_stake > 0
        delegated = self.shares > 0
        funds = self.GRT
        indexer_revenue = self.indexer_revenue_cut
        allocated_subgraph = self.subgraphs
        rewardTransferred = 0
        for subgraph in inpt['available_subgraphs'].values():
            allocations = [allocation for allocation in subgraph.allocations.values() if allocation.tokens != 0]
            if len(allocations) == 0 and inpt['available_subgraphs']:
                    if staked:
                # delegate to self
                        if strategy['delegate']['tokens'] <= funds:
                            plan = strategy['delegate']
                            plan['indexer'] = self.id
                            plan['delegator'] = self.id
                            plan['subgraphDeploymentID'] = inpt['available_subgraphs'].keys()[0]
                    elif not staked:
                        # create an ownIndexer stake
                        if strategy['stake']['tokens'] <= funds:
                            plan = strategy['stake']
                            plan['indexer'] = self.id
                            plan['delegator'] = self.id
                            plan['subgraphDeploymentID'] = inpt['available_subgraphs'].keys()[0]
                    else:
                        # have staked and delegated, so open an allocation
                        if strategy['open']['tokens'] <= funds:
                            plan = strategy['open']
                            plan['indexer'] = self.id
                            plan['epoch'] = current_period
                            plan['allocationID'] = '1'
                            plan['subgraphDeploymentID'] = inpt['available_subgraphs'].keys()[0]
                    self.plan = plan
            elif inpt['available_subgraphs']:
                for avail_subgraph in inpt['available_subgraphs']:
                    plan = {}
                    if avail_subgraph not in allocated_subgraph.keys():
                        if strategy['open']['tokens'] <= funds:
                            plan = strategy['open']
                            plan['indexer'] = self.id
                            plan['epoch'] = current_period
                            plan['allocationID'] = '1'
                            plan['subgraphDeploymentID'] = subgraph
                    else:
                        if indexer_revenue is None:
                            # set indexingRewardCut for this subgraph's allocation
                            plan = strategy['set_cut']
                            plan['amount'] = 1
                            plan['indexer'] = self.id
                        else:
                            for allocation in allocations:

                                if current_period - allocation.start_period < strategy['wait']['timeWaited']:
                                # wait according to agent preferences on waiting time, timeWaited
                                    plan = strategy['wait']
                                    plan['indexer']  = self.id
                                    plan['subgraphDeploymentID'] = subgraph
                                else:
                                    if subgraph['status'] == "rewardPaid": 
                                        rewardTransferred += 1
                                    elif subgraph['status'] != "closed":
                                        if indexer_revenue != 0:
                                        # waited long enough,  switch reward cut to zero
                                            plan = strategy['set_cut']
                                            plan['indexer'] = self.id
                                            plan['amount'] = 0
                                    else:
                                        # waited long enough and index cut is zero, close the allocation
                                        plan = strategy['close']
                                        plan['indexer'] = self.id
                    if plan: 
                        self.plan = plan
            if rewardTransferred == len(allocated_subgraph) and len(allocated_subgraph) > 0:
                plan = {}
                if current_period >= inpt['delegation_unbonding_period']:
                    if not delegated:
                        # check balance to see if delegation reward has been deposited
                        plan = strategy['checkBalance']
                        state['stake']['status'] = 'have sent checkAccountBalance'
                    elif state['stake']['status'] == "have sent checkAccountBalance":
                        # clear the delegation
                        plan = strategy['clear']
                        plan['indexer'] = self.id
                    else:
                        # withdraw from delegation to recoup rewards from allocation
                        plan = strategy['withdraw']
                        plan['indexer'] = self.id
                else:
                    # rewards have been distributed, undelegate
                    plan = strategy['undelegate']
                    plan['indexer'] = self.id
                    plan['delegator'] = self.id
                    plan['until'] = current_period + inpt['delegation_unbonding_period']
                if plan: 
                    self.plan = plan
                    
            self.plan = plan

    def generate_output(self):
        self.output = []
        if self.plan:
            # output must be a list of events.
            self.output.append(self.plan)
        