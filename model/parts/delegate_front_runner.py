from .heuristic_agent import HeuristicAgent
from .delegate_front_runner_rules import DelegateFrontRunnerRules
class DelegateFrontRunner(HeuristicAgent):

    def __init__(self, id, rules : DelegateFrontRunnerRules,
                initialAccountBalance):
        super().__init__(id, rules, initialAccountBalance)
        self._inputs = []
        self.state = [
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
        
    # updateState should save the delegator's delegations to different indexers
    # def updateState(self):
    #     # this gets the only indexer id. 
    #     indexer_id = list(self._inputs[-1]['availableIndexers'].keys())[0]
    #     if self._inputs[-1]['availableIndexers'][indexer_id].delegators:

    #         state = {
    #             'delegations': self.output
    #         }
    #     else:
    #         state = {}
                    
    #     output = self.output
    #     if output:
    #         if output['status'] == "have cleared delegation":
    #             state['delegations'].pop(output['target'], None)
    #         else:
    #             state['delegations'].update(output)
                    
        
    #     self.state = state
    
    # def generatePlan(self):
    #     state           = self.state
    #     strategy        = self._strategies[-1]
    #     inpt            = self._inputs[-1]
    
    #     # there won't be any plans if there aren't any allocations to a subgraph.
    #     t = inpt['currentPeriod']
    #     delegationPlans = []
    #     for indexer_id, indexer in inpt['availableIndexers'].items():
    #         for subgraph in indexer.subgraphs.values():
    #             for allocation in subgraph.allocations.values(): 
    #                 plan = {}
    #                 # the following are the 'if-then' structures for the [C01] front-running attack
    #                 if t == allocation.start_period + inpt['allocationDays'] - 1: # allocation time in days/epochs
                        
    #                     # (state['delegations'][indexer]['status'] != "have delegated" and
    #                     if indexer_id not in state['delegations'] or \
    #                             self.shares == 0 and \
    #                             indexer[allocation]['state'] not in ("claim", "close"):
    #                         if strategy['delegate']['amount'] <= self.holdings:
    #                             # correct python: plan = dict(strategy['delegate'],
    #                             #  **{'target' : indexer}) leaves rule unchanged 
    #                             #  but updates target for plan; pseudocode used below for semantics
    #                             strategy['delegate'].update({'target' : indexer}) 
    #                             plan = strategy['delegate'] # maybe i want the whole strategy
    #                 elif state['delegations'] and indexer_id in state['delegations']:
    #                     if t == allocation.start_period + inpt['allocationDays'] + inpt['disputeChannelEpochs']: # epoch = day
    #                         # if state['delegations'][indexer]['status'] == "have delegated":
    #                         if self.shares > 0:
    #                                 if indexer[allocation]['state'] == "close":
    #                                     strategy['claim'].update({'target' : indexer})
    #                                     plan = strategy['claim']
    #                                 elif indexer[allocation]['state'] == "claim":
    #                                     strategy['undelegate'].update({'target' : indexer})
    #                                     plan = strategy['undelegate']
    #                     elif t == allocation.start_period + inpt['allocationDays'] + \
    #                         inpt['disputeChannelEpochs'] + inpt['delegationUnbondingPeriod']:
    #                         if state['delegations'][indexer]['status'] == "have sent undelegate()":
    #                             strategy['withdraw'].update({'target' : indexer})
    #                             plan = strategy['withdraw']
    #                         elif state['delegations'][indexer]['status'] == "have sent withdraw()":
    #                             plan = strategy['checkBalance']
    #                         elif state['delegations'][indexer]['status'] == "have sent checkAccountBalance":
    #                             if inpt['accountBalance'] > self.holdings:
    #                                 strategy['clear'].update({'target' : indexer})     
    #                                 plan = strategy['clear']
    #                 if plan: 
    #                     delegationPlans.append(plan)
    #     self.plan = delegationPlans

    # this only works for one indexer currently because delegator is an attribute of an indexer.
    def generatePlan(self):
        inpt = self._inputs[-1]
        strategy        = self._strategies[-1]
        currentPeriod = inpt['currentPeriod']
        plan = None
        withdrawn = self.shares == 0
        delegated = self.shares > 0
        undelegated = self.undelegated_tokens > 0

        # For each available indexer, the FRD checks to see if they have already delegated to that indexer.
        for indexer in inpt['availableIndexers'].values():            
            
            # If the FRD has not delegated to that indexer, they check to see what the available allocations are for that indexer.
            if not delegated:
                for subgraph in indexer.subgraphs.values():
                    for allocation in subgraph.allocations.values():
                        # If there is an allocation from that indexer which is available to delegate to, the FRD checks to see if the allocation may shortly close (this depends upon the starting time of the allocation, i.e. how long it has been open).
                        if currentPeriod == allocation.start_period + inpt['allocationDays'] - 1: # allocation time in days/epochs
                            # If the allocation may shortly close, the FRD delegates to that allocation, for that indexer, if they have the available funds to do so. This is the start of the front-running attack.
                            if self.holdings > 0: 
                                plan = strategy['delegate']
                                break
            # If the FRD has delegated to that indexer, the FRD checks to see if it’s time to begin the process of undelegating.
            else:
                for subgraph in indexer.subgraphs.values():
                    for allocation in subgraph.allocations.values():
                        # If enough time has passed to allow undelegation to commence (this depends upon the time allowed for disputes to resolve), the FRD first checks to see if the allocation has already closed, or if indexing rewards have already been claimed.
                        if currentPeriod == allocation.start_period + inpt['allocationDays'] + inpt['disputeChannelEpochs']: 
                            # If the allocation has already closed and indexing rewards have already been claimed, the FRD undelegates from that indexer.
                            # If the allocation has already closed but indexing rewards have not been claimed, the FRD issues a claim for the indexing rewards.
                            # TODO: add if indexing rewards have been claimed.
                            indexing_rewards_claimed = False
                            allocation_closed = allocation.tokens == 0
                            if allocation_closed:
                                if indexing_rewards_claimed:
                                    plan = strategy['undelegate']
                                else:
                                    plan = strategy['claim']
                        # If enough time has passed to allow withdrawing their delegation to commence (this depends upon both the time allowed for disputes to resolve, and upon the unbonding period for delegators), the FRD checks to see if they’ve already undelegated, or if they’ve already withdrawn their delegation.
                        if currentPeriod == allocation.start_period + inpt['allocationDays'] + inpt['disputeChannelEpochs'] + inpt['delegationUnbondingPeriod']:
                            # If they’ve already undelegated, they withdraw their delegation.
                            
                            if undelegated:
                                plan = strategy['withdraw'] 
                            
                            # If they’ve already withdrawn their delegation, they check to see if their available funds has increased due to their withdrawn delegation.                            
                            # NOTE: nothing needs to be done here.
                            # If their available funds has increased, they stop keeping track of this delegation and clear it from their memory. This is the end of the front-running attack.
                            # NOTE: nothing needs to be done here.
        return plan
    def generateOutput(self):
        if self.plan:
            # for event in self.plan[-1]:
                # this appends the keys of the plan, but what should it do?
            self.output = self.plan[-1]


