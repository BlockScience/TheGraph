from .heuristic_agent import HeuristicAgent
from .delegate_front_runner_rules import DelegateFrontRunnerRules
 
class DelegateFrontRunner(HeuristicAgent):

    def __init__(self, id, rules : DelegateFrontRunnerRules,
                initialAccountBalance):
        super().__init__(id, rules)
        self._inputs = []
        self._outputs = []
        self._states = [
            {
                'delegations'    : None,
                'availableFunds' : initialAccountBalance
            }
        ]
        self._plans = []
    
    def inputs(self, newInput):
        self._inputs.append(
            {
                'availableIndexers'         : newInput['availableIndexers'],
                'currentPeriod'             : newInput['currentPeriod'],
                'disputeChannelEpochs'      : newInput['disputeChannelEpochs'],
                'delegationUnbondingPeriod' : newInput['delegationUnbondingPeriod'],
                'accountBalance'            : newInput['accountBalance']
            }
        )
        
    def updateState(self):
        state = {
            'delegations'    : self._states[-1]['delegations'],
            'availableFunds' : self._inputs[-1]['accountBalance']
        }
        
        if len(self._outputs) > 0:
            output = self._outputs[-1]
            for plan in output:
                if plan['status'] == "have cleared delegation":
                    state['delegations'].pop(plan['target'], None)
                else:
                    state['delegations'].update(plan)
                    
        
        self._states.append(state)
    
    def generatePlans(self):
        state           = self._states[-1]
        strategy        = self._strategies[-1]
        inpt            = self._inputs[-1]
    
        delegationPlans = []
        
        t = inpt['currentPeriod']
        for indexer_id, indexer in inpt['availableIndexers'].items():
            for subgraph in indexer.subgraphs.values():
                for allocation in subgraph.allocations.values():
                    plan = {}
                    # the following are the 'if-then' structures for the [C01] front-running attack
                    if t == allocation.start_period + 27: # allocation time in days/epochs
                        if indexer not in state['delegations'] or \
                        (state['delegations'][indexer]['status'] != "have delegated" and
                            indexer[allocation]['state'] not in ("claim", "close")):
                            if strategy['delegate']['amount'] <= state['availableFunds']:
                                # correct python: plan = dict(strategy['delegate'],
                                #  **{'target' : indexer}) leaves rule unchanged 
                                #  but updates target for plan; pseudocode used below for semantics
                                plan = strategy['delegate'].update({'target' : indexer}) 
                    if state['delegations'] and indexer_id in state['delegations']:
                        if t == allocation.start_period + 28 + inpt['disputeChannelEpochs']: # epoch = day
                            if state['delegations'][indexer]['status'] == "have delegated":
                                    if indexer[allocation]['state'] == "close":
                                        plan = strategy['claim'].update({'target' : indexer})
                                    elif indexer[allocation]['state'] == "claim":
                                        plan = strategy['undelegate'].update({'target' : indexer})
                        elif t == allocation.start_period + 28 + \
                            inpt['disputeChannelEpochs'] + inpt['delegationUnbondingPeriod']:
                            if state['delegations'][indexer]['status'] == "have sent undelegate()":
                                plan = strategy['withdraw'].update({'target' : indexer})
                            elif state['delegations'][indexer]['status'] == "have sent withdraw()":
                                plan = strategy['checkBalance']
                            elif state['delegations'][indexer]['status'] == "have sent checkAccountBalance":
                                if inpt['accountBalance'] > state['availableFunds']:
                                    plan = strategy['clear'].update({'target' : indexer})     
                    if plan: delegationPlans.append(plan)
        self._plans.append(delegationPlans)
    
    def selectPlan(self):
        return self._plans[-1] 
    
    def generateOutput(self):
        output = []
        for plan in self._plans[-1]:
            output.append(plan)
            # added JS
            self.outputs.append(plan)
        return output


