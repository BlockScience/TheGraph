from decimal import Decimal

class Portfolio():
    def __init__(self, id, holdings = Decimal(100000000), eth_holdings = Decimal(10000), gas_spent = Decimal(0), ROI = Decimal(0), ROI_time = Decimal(0), indexer_shares = {},
                indexer_revenues = {}, indexer_price = {}, indexer_realized_price = {}, indexer_yield = {},
                indexer_in_tokens = {}, private_price = None, private_yield = None, 
                indexer_locked_tokens = {}, action_block_number = {}, indexer_ROI = {}):
        self.id = id
        self.holdings = holdings
        self.eth_holdings = eth_holdings
        self.gas_spent = gas_spent
        self.ROI = ROI
        self.ROI_time = ROI_time
        self.indexer_shares = indexer_shares
        self.indexer_revenues = indexer_revenues
        self.indexer_price = indexer_price
        self.indexer_realized_price = indexer_realized_price
        self.indexer_in_tokens = indexer_in_tokens
        self.indexer_locked_tokens = indexer_locked_tokens
        self.delegate_block_number = action_block_number
        self.withdraw_block_number = withdraw_block_number
        self.indexer_ROI = indexer_ROI
        self.indexer_ROI_time = indexer_ROI_time