from .heuristic_agent import HeuristicAgent
from .delegate_front_runner_rules import DelegateFrontRunnerRules
class DelegateFrontRunner(HeuristicAgent):

    def __init__(self, id, rules : DelegateFrontRunnerRules,
                initialAccountBalance):
        super().__init__(id, rules, initialAccountBalance)
        self._inputs = []
        self._states = [
            {
                # get this from indexer.delegators
                'delegations'    : {},
            }
        ]
    
    def inputs(self, newInput):
        self._inputs.append(
            {
                'availableIndexers'         : newInput['availableIndexers'],
                'currentPeriod'             : newInput['currentPeriod'],
                'disputeChannelEpochs'      : newInput['disputeChannelEpochs'],
                'allocationDays'            : newInput['allocationDays'],
                'delegationUnbondingPeriod' : newInput['delegationUnbondingPeriod'],
                'accountBalance'            : newInput['accountBalance']
            }
        )
        

    def updateState(self):
        state = {
            # 'delegations'    : self._states[-1]['delegations'],
            'delegations': self._inputs[-1]['availableIndexers']['delegators'] if 'delegators' in self._inputs[-1]['availableIndexers'] else {}
        }
        
        output = self.output
        if output:
            for plan in output:
                if plan['status'] == "have cleared delegation":
                    state['delegations'].pop(plan['target'], None)
                else:
                    state['delegations'].update(plan)
                    
        
        self._states.append(state)
    
    def generatePlan(self):
        state           = self._states[-1]
        strategy        = self._strategies[-1]
        inpt            = self._inputs[-1]
    
        # there won't be any plans if there aren't any allocations to a subgraph.
        t = inpt['currentPeriod']
        delegationPlans = []
        for indexer_id, indexer in inpt['availableIndexers'].items():
            for subgraph in indexer.subgraphs.values():
                for allocation in subgraph.allocations.values(): 
                    plan = {}
                    # the following are the 'if-then' structures for the [C01] front-running attack
                    if t == allocation.start_period + inpt['allocationDays'] - 1: # allocation time in days/epochs
                        if indexer_id not in state['delegations'] or \
                                (state['delegations'][indexer]['status'] != "have delegated" and
                                indexer[allocation]['state'] not in ("claim", "close")):
                            if strategy['delegate']['amount'] <= self.holdings:
                                # correct python: plan = dict(strategy['delegate'],
                                #  **{'target' : indexer}) leaves rule unchanged 
                                #  but updates target for plan; pseudocode used below for semantics
                                strategy['delegate'].update({'target' : indexer}) 
                                plan = strategy['delegate'] # maybe i want the whole strategy
                    elif state['delegations'] and indexer_id in state['delegations']:
                        if t == allocation.start_period + inpt['allocationDays'] + inpt['disputeChannelEpochs']: # epoch = day
                            if state['delegations'][indexer]['status'] == "have delegated":
                                    if indexer[allocation]['state'] == "close":
                                        strategy['claim'].update({'target' : indexer})
                                        plan = strategy['claim']
                                    elif indexer[allocation]['state'] == "claim":
                                        strategy['undelegate'].update({'target' : indexer})
                                        plan = strategy['undelegate']
                        elif t == allocation.start_period + inpt['allocationDays'] + \
                            inpt['disputeChannelEpochs'] + inpt['delegationUnbondingPeriod']:
                            if state['delegations'][indexer]['status'] == "have sent undelegate()":
                                strategy['withdraw'].update({'target' : indexer})
                                plan = strategy['withdraw']
                            elif state['delegations'][indexer]['status'] == "have sent withdraw()":
                                plan = strategy['checkBalance']
                            elif state['delegations'][indexer]['status'] == "have sent checkAccountBalance":
                                if inpt['accountBalance'] > self.holdings:
                                    strategy['clear'].update({'target' : indexer})     
                                    plan = strategy['clear']
                    if plan: 
                        delegationPlans.append(plan)
        self.plan = delegationPlans
    
    def generateOutput(self):
        output = []
        for event in self.plan:
            output.append(event)
        self.output = output
        return output
