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
       

    # this only works for one indexer currently because delegator is an attribute of an indexer.
    def generatePlan(self):
        inpt = self._inputs[-1]
        strategy        = self._strategies[-1]
        currentPeriod = inpt['currentPeriod']
        print(f'{currentPeriod=}')                        
        plan = {}
        # withdrawn = self.shares == 0
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
                                plan['delegator'] = self.id
                                plan['indexer'] = indexer.id
                                break
            # If the FRD has delegated to that indexer, the FRD checks to see if it’s time to begin the process of undelegating.
            else:
                for subgraph in indexer.subgraphs.values():
                    for allocation in subgraph.allocations.values():
                        # If enough time has passed to allow undelegation to commence (this depends upon the time allowed for disputes to resolve), the FRD first checks to see if the allocation has already closed, or if indexing rewards have already been claimed.
                        if currentPeriod == allocation.start_period + inpt['allocationDays'] + inpt['disputeChannelEpochs']: 
                            # If the allocation has already closed and indexing rewards have already been claimed, the FRD undelegates from that indexer.
                            # If the allocation has already closed but indexing rewards have not been claimed, the FRD issues a claim for the indexing rewards.
                            # NOTE: allocation_closed and claim events always occur in the same timeblock, so if the allocation closed, we should undelegate.
                            allocation_closed = allocation.tokens == 0
                            if allocation_closed:
                                plan = strategy['undelegate']
                                plan['delegator'] = self.id
                                plan['indexer'] = indexer.id
                                plan['shares'] = self.shares
                                break
                        # If enough time has passed to allow withdrawing their delegation to commence (this depends upon both the time allowed for disputes to resolve, and upon the unbonding period for delegators), the FRD checks to see if they’ve already undelegated, or if they’ve already withdrawn their delegation.
                        if currentPeriod == allocation.start_period + inpt['allocationDays'] + inpt['disputeChannelEpochs'] + inpt['delegationUnbondingPeriod']:
                            # If they’ve already undelegated, they withdraw their delegation.
                            
                            if undelegated:
                                plan = strategy['withdraw'] 
                                plan['delegator'] = self.id
                                plan['indexer'] = indexer.id
                                plan['tokens'] = self.undelegated_tokens
                                break
                            # If they’ve already withdrawn their delegation, they check to see if their available funds has increased due to their withdrawn delegation.                            
                            # NOTE: nothing needs to be done here.
                            # If their available funds has increased, they stop keeping track of this delegation and clear it from their memory. This is the end of the front-running attack.
                            # NOTE: nothing needs to be done here.
        self.plan = plan

    
    def generateOutput(self):
        self.output = []
        if self.plan:
            # output must be a list of events.
            self.output.append(self.plan)


