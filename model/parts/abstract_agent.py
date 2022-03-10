# The abstract base class is used
from abc import ABC, abstractmethod


class AbstractAgent(ABC):
    
    # technically AbstractAgent is never instantiated, but enforcing
    # __init__ ensures subclasses respect identifier requirement
    # note also no hint for type of identifier (str, int etc.)
    @abstractmethod
    def __init__(self, identifier):
        self.id = identifier
        # FRD needs to keep track of the allocation he delegated to for undelegation purposes.
        self.allocation_id = ''
        self.subgraph_id = ''
        self.output = []
        self.plan = None  # changed to None from empty list of plans
        self.state = {}
        self._inputs = []
        self._beliefs = []
        self._strategies = []

    @property
    def inputs(self):
        # input is a reserved method in python
        return self._inputs  # List[inpt]
    
    @inputs.setter
    def inputs(self, newInput):
        self._inputs.append(newInput)
    
    @property
    def beliefs(self):
        return self._beliefs  # List[belief]
    
    @property
    def strategies(self):
        return self._strategies  # List[strategy]

    @abstractmethod
    def update_beliefs(self, beliefs: beliefs):
        # overridden for subclass belief update
        # abstract class does nothing
        pass

    @abstractmethod
    def generate_strategies(self):
        # overridden for subclass strategy generation
        # abstract class does nothing
        pass

    @abstractmethod
    def generate_plan(self):
        # overridden for subclass plan generation
        # abstract class does nothing
        pass

    @abstractmethod
    def generate_output(self, plan):
        # overridden for subclass output generation
        # abstract class does nothing
        pass

    def get_action(self):
        # self.updateState()
        self.update_beliefs()
        self.generate_strategies()
        self.generate_plan()
        # self.selectPlan()
        self.generate_output()
