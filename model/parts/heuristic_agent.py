# The abstract class 'AbstractAgent' is used, 
# assumed to lie within an 'agent' module
from .abstract_agent import AbstractAgent
from model.parts.delegator import Delegator
 

class HeuristicAgent(Delegator):

    def __init__(self, id, rules, initialAccountBalance): # Dict[id, rule]):
        super().__init__(id, holdings=initialAccountBalance)
        self._strategies = [rules.rules]
        
    def beliefs(self):
        # Heuristic agents do not have beliefs about the environment
        return None
        
    def updateState(self): #, states : states, inputs : inputs):
        # Heuristic agents do not condition on anything other than
        # their internal state and external inputs to update their
        # internal state
        pass
    
    def updateBeliefs(self):
        # Heuristic agents do not have beliefs to update
        return None
    
    def generateStrategies(self):
        # Heuristic agents do not generate strategies
        return None
    
    def generatePlan(self):
        # Heuristic agents test alternative rules against their state
        # and return plans that meet rule criteria (if any)
        pass
    
    # def selectPlan(self):
    #     # If multiple plans are available, logic for selecting
    #     # between them should be placed here
    #     pass
    
    def generateOutput(self, plan):
        # Application of the selected plan occurs here
        pass