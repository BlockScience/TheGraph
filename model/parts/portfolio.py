from decimal import Decimal
from model.parts.abstract_agent import AbstractAgent


# A portfolio is a Delegator that can have delegations to many indexers
# We are only making it a Delegator to get access to ...

class Portfolio(AbstractAgent):
    def __init__(self, delegator_id, holdings=Decimal(10000000000), eth_holdings=Decimal(10000), gas_spent=Decimal(0),
                 indexer_shares={},
                 indexer_revenues={}, indexer_price={}, indexer_realized_price={}, indexer_yield={},
                 indexer_in_tokens={}, private_price=None, private_yield=None,
                 indexer_locked_tokens={}, withdraw_block_number={}, delegate_block_number={}):

        super().__init__(delegator_id)
        # self.id = delegator_id

        # Amount of free/withdrawn token the delegator is holding, h
        self.holdings = holdings

        # delegations is all of the delegations made by THIS Delegator,
        # not to be confused with delegators on the indexer, which is all of the delegations for that Indexer.
        self.delegations = {}  # key = indexer_id, value = "Delegator"

        self.eth_holdings = eth_holdings
        self.gas_spent = gas_spent
        self.indexer_shares = indexer_shares
        self.indexer_revenues = indexer_revenues
        self.indexer_price = indexer_price
        self.indexer_realized_price = indexer_realized_price
        self.indexer_in_tokens = indexer_in_tokens
        self.indexer_locked_tokens = indexer_locked_tokens
        self.delegate_block_number = delegate_block_number
        self.withdraw_block_number = withdraw_block_number

    def __str__(self):
        """
        Print all attributes of the class
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    def pretty_print(self):
        return f'{self.id=}, {self.plan=}'

    def beliefs(self):
        return None

    # def updateState(self): #, states : states, inputs : inputs):
    #     pass

    def update_beliefs(self):
        return None

    def generate_strategies(self):
        return None

    def generate_plan(self):
        pass

    def select_plan(self):
        pass

    def generate_output(self, plan):
        pass
