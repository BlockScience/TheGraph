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
                'subgraphs': {},
                'available_funds': initialaccount_balance,
                'timeWaited': {}
            }
        ]

    def input(self, newInput):
        self._inputs.append(
            {
                'availableSubgraphs': newInput['availableSubgraphs'],
                'currentPeriod': newInput['currentPeriod'],
                'delegation_unbonding_period': newInput['delegationUnbondingPeriod'],
                'accountBalance': newInput['accountBalance']
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
        delegated = self.shares > 0
        funds = self.GRT
        if not state['subgraphs'] and inpt['availableSubgraphs']:
            if state['stake']['status'] == "have staked to self":
                # delegate to self
                if strategy['delegate']['tokens'] <= funds:
                    plan = strategy['delegate']
                    plan['indexer'] = self.id
                    plan['delegator'] = self.id
                    plan['subgraphDeploymentID'] = inpt['availableSubgraphs'][0]
            elif state['stake']['status'] != "have delegated to self":
                # create an ownIndexer stake
                if strategy['stake']['tokens'] <= funds:
                    plan = strategy['stake']
                    plan['indexer'] = self.id
                    plan['delegator'] = self.id
                    plan['subgraphDeploymentID'] = inpt['availableSubgraphs'][0]
            else:
                # have staked and delegated, so open an allocation
                if strategy['open']['tokens'] <= delegated:
                    plan = strategy['open']
                    plan['target'] = inpt['availableSubgraphs'][0]
            self.plan = plan
        elif inpt['availableSubgraphs']:
            rewardTransferred = 0
            for subgraph in inpt['availableSubgraphs']:
                plan = {}
                if subgraph not in state['subgraphs']:
                    if strategy['open']['tokens'] <= state['stake']['available']:
                        plan = strategy['open']
                        plan['target'] = subgraph
                else:
                    if state['stake']['indexingRewardCut'] is None:
                        # set indexingRewardCut for this subgraph's allocation
                        plan = strategy['set_cut']
                        plan['amount'] = 1
                        plan['target'] = self.id
                    else:
                        if state['timeWaited'][subgraph] < strategy['wait']['timeWaited']:
                            # wait according to agent preferences on waiting time, timeWaited
                            plan = strategy['wait']
                            plan['target'] = subgraph
                        else:
                            if subgraph['status'] == "rewardPaid": 
                                rewardTransferred += 1
                            elif subgraph['status'] != "closed":
                                if state['stake']['indexingRewardCut'] != 0:
                                    # waited long enough,  switch reward cut to zero
                                    plan = strategy['set_cut']
                                    plan['target'] = subgraph
                                    plan['amount'] = 0
                                else:
                                    # waited long enough and index cut is zero, close the allocation
                                    plan = strategy['close']
                                    plan['target'] = subgraph
                if plan: 
                    self.plan = plan
        if rewardTransferred == len(state['subgraphs']):
            plan = {}
            if current_period >= state['stake']['undelegatePeriod'] + \
                inpt['delegationUnbondingPeriod']:
                if state['stake']['status'] is "have withdrawn from own delegation":
                    # check balance to see if delegation reward has been deposited
                    plan = strategy['checkBalance']
                elif state['stake']['status'] is "have sent checkAccountBalance":
                    # clear the delegation
                    plan = strategy['clear']
                    plan['target'] = self.id
                else:
                    # withdraw from delegation to recoup rewards from allocation
                    plan = strategy['withdraw']
                    plan['target'] = self.id
            else:
                # rewards have been distributed, undelegate
                plan = strategy['undelegate'].update({'target' : self.identifier, 'undelegatePeriod' : current_period})
                plan['target'] = self.id
                plan['until'] = current_period + inpt['delegation_unbonding_period']
            if plan: 
                self.plan = plan
                
        self.plan = plan

    def generate_output(self):
        self.output = []
        if self.plan:
            # output must be a list of events.
            self.output.append(self.plan)
        