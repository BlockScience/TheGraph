from decimal import Decimal
from model.parts.delegator import Delegator


class Portfolio(Delegator):
    def __init__(self, delegator_id, holdings=Decimal(10000000000), eth_holdings=Decimal(10000), gas_spent=Decimal(0),
                 indexer_shares={},
                 indexer_revenues={}, indexer_price={}, indexer_realized_price={}, indexer_yield={},
                 indexer_in_tokens={}, private_price=None, private_yield=None,
                 indexer_locked_tokens={}, withdraw_block_number={}, delegate_block_number={}):

        super().__init__(delegator_id, holdings=holdings)
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
        return f'{self.id=}, {self.shares=}, {self.holdings=}, {self.undelegated_tokens=}, {self.plan=}'
