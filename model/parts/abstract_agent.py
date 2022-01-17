# The abstract base class is used
from abc import ABC, abstractmethod
 
class AbstractAgent(ABC):
    
    # technically AbstractAgent is never instantiated, but enforcing
    # __init__ ensures subclasses respect identifier requirement
    # note also no hint for type of identifier (str, int etc.)
    @abstractmethod
    def __init__(self, identifier):
        self.id = identifier
        self.output = {}
        self.plan = [] # a list of plans
        self.state = {}

    @property
    def inputs(self):
        # input is a reserved method in python
        return self._inputs # List[inpt]
    
    @inputs.setter
    def inputs(self, newInput):
        self._inputs.append(newInput)
    
    @property
    def beliefs(self):
        return self._beliefs # List[belief]
    
    @property
    def strategies(self):
        return self._strategies # List[strategy]
    
    
    # @abstractmethod
    # def updateState(self, state):
    #     # overridden for subclass state update
    #     # abstract class does nothing
    #     pass
    
    @abstractmethod
    def updateBeliefs(self, beliefs : beliefs):
        # overridden for subclass belief update
        # abstract class does nothing
        pass
    
    @abstractmethod
    def generateStrategies(self):
        # overridden for subclass strategy generation
        # abstract class does nothing
        pass
    
    @abstractmethod
    def generatePlan(self):
        # overridden for subclass plan generation
        # abstract class does nothing
        pass
    
    # @abstractmethod
    # def selectPlan(self):
    #     # overridden for subclass plan selection
    #     # abstract class does nothing
    #     pass
    
    @abstractmethod
    def generateOutput(self, plan):
        # overridden for subclass output generation
        # abstract class does nothing
        pass
    
    def getAction(self):
        # self.updateState()
        self.updateBeliefs()
        self.generateStrategies()
        self.generatePlan()
        # self.selectPlan()
        self.generateOutput() 