# The abstract class 'AbstractAgent' is used, 
# assumed to lie within an 'agent' module
#from model.parts.delegate_front_runner import DelegateFrontRunner
from model.parts.subgraph import Subgraph
from .abstract_agent import AbstractAgent
from model.parts.delegator import Delegator
from .indexer import Indexer
from decimal import Decimal
 

class HeuristicAgent(Indexer):

    def __init__(self, indexer_id, rules, initialaccount_balance):  # Dict[id, rule]):
        super().__init__(indexer_id, GRT=initialaccount_balance, subgraphs = {'1': Subgraph()}, delegators = {1: Delegator(1, holdings = Decimal(10e9))})
        self._strategies = [rules.rules]
        
    def beliefs(self):
        # Heuristic agents do not have beliefs about the environment
        return None
        
    # def updateState(self): #, states : states, inputs : inputs):
    #     # Heuristic agents do not condition on anything other than
    #     # their internal state and external inputs to update their
    #     # internal state
    #     pass
    
    def update_beliefs(self):
        # Heuristic agents do not have beliefs to update
        return None
    
    def generate_strategies(self):
        # Heuristic agents do not generate strategies
        return None
    
    def generate_plan(self):
        # Heuristic agents test alternative rules against their state
        # and return plans that meet rule criteria (if any)
        pass
    
    # def selectPlan(self):
    #     # If multiple plans are available, logic for selecting
    #     # between them should be placed here
    #     pass
    
    def generate_output(self, plan):
        # Application of the selected plan occurs here
        pass
