# The base class 'HeuristicAgent' is used, 
# assumed to lie within an 'agent' module
from heuristic_agent import HeuristicAgent
 
class DelegateAttacker(HeuristicAgent):

    def __init__(self, identifier, rules): # : Dict[id, rule]):
        super().__init__(identifier, rules)
        
    def updateState(self): #, states : states, inputs : inputs, outputs: outputs):
        self._states.append(
                # List of available allocations 
                #     and their starting periods 
                #     and the agent internal state for each,
                # current period $t$,
                # current available funds $GRT$,
                # global delegation parameters (such as disputeChannelEpochs,
                #     delegationUnbondingPeriod, etc.),
                # delegation events since previous period $t-1$
        )
    
    def generatePlans(self, states, strategies):
        # Technically, each of the inner 'if' blocks is a separate strategy, 
        # with the 'if' statement itself assessing the feasibility 
        # of the plan it encloses
        # for each available allocation in states;
        #     if $t$ is allocation start + 27:
        #         self._plans.append(
        #             delegate fixed amount $G$ to this allocation
        #         )  and set internal state "have delegated to this allocation"
        #         if $G <= GRT$, otherwise delegate nothing 
        #     else if $t$ is allocation start + 28 + disputeChannelEpochs
        #         and internal state has "have delegated to this allocation"
        #         and allocation close() event has been sent
        #         and allocation claim() event has not been sent:
        #         self._plans.append(
        #             send claim() event
        #         )
        #     else if $t$ is allocation start + 28 + disputeChannelEpochs
        #         and internal state has "have delegated to this allocation"
        #         and allocation claim() event has been sent:
        #         self._plans.append(
        #             send undelegate() event
        #         ) and set internal state "have sent undelegate event"
        #     else if $t$ is allocation start + 28 + disputeChannelEpochs +
        #         delegationUnbondingPeriod 
        #         and internal state has "have delegated to this allocation" 
        #         and internal state has "have sent undelegate event":
        #         self._plans.append(
        #             send withdrawDelegated() event
        #         ) and set internal state "have sent withdraw event"
        #     else if $t$ is allocation start + 28 + disputeChannelEpochs +
        #         delegationUnbondingPeriod 
        #         and internal state has "have delegated to this allocation" 
        #         and internal state has "have sent withdraw event":
        #         if states contains account crediting 
        #             from withdraw delegation event:
        #             clear internal state for this allocation
        #             add credited amount to $GRT$
    
    def selectPlan(self, plans):
        return plans[-1] # latest plan
    
    def generateOutput(self, plan):
        # Application of the selected plan occurs here
        return plan
