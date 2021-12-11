t

# The abstract class 'AbstractAgent' is used, 
# assumed to lie within an 'agent' module
from abstract_agent import AbstractAgent
 
class HeuristicAgent(AbstractAgent):

    def __init__(self, identifier, rules): # Dict[id, rule]):
        super().__init__(identifier)
        self._strategies = rules
        
    def beliefs(self):
        # Heuristic agents do not have beliefs about the environment
        return []
        
    def updateState(self, states : states, inputs : inputs):
        # Heuristic agents do not condition on anything other than
        # their internal state and external inputs to update their
        # internal state
        return pass
    
    def updateBeliefs(self):
        # Heuristic agents do not have beliefs to update
        return None
    
    def generateStrategies(self):
        # Heuristic agents do not generate strategies
        return None
    
    def generatePlans(self, states : states, strategies : strategies):
        # Heuristic agents test alternative rules against their state
        # and return plans that meet rule criteria (if any)
        return pass
    
    def selectPlan(self, plans : plans):
        # If multiple plans are available, logic for selecting
        # between them should be placed here
        return pass
    
    def generateOutput(self, plan : plan):
        # Application of the selected plan occurs here
        return pass