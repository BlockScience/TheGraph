from model.parts.portfolio import Portfolio


class UtilityComponents(object):
    def __init__(self, components=None):
        if components:
            self.beliefs = components['beliefs']
            self.attributes = components['attributes']
            self.utility = components['utility']
            self.actions = components['actions']

    def get_properties(self):
        return {
              # '_beliefs': self._beliefs,
              '_utility': self._utility,
              '_actions': self._actions,
              '_attributes': self._attributes
        }


class UtilityAgent(Portfolio):

    def __init__(self, delegator_id, initialaccount_balance, components):
        super().__init__(delegator_id, holdings=initialaccount_balance)
        # self.components = components
        for p in components.get_properties():
            setattr(self, p, components.get_properties()[p])

    @property
    def beliefs(self):
        return self._beliefs

    @property
    def utility(self):
        return self._utility

    @property
    def attributes(self):
        return self._attributes

    @property
    def actions(self):
        return self._actions

    # def updateState(self): #, states : states, inputs : inputs):
    #     # Heuristic agents do not condition on anything other than
    #     # their internal state and external inputs to update their
    #     # internal state
    #     pass

    @beliefs.setter
    def update_beliefs(self):
        pass
    
    def generate_strategies(self):
        pass
    
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
