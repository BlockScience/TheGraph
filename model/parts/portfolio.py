from decimal import Decimal

class Portfolio():
    def __init__(self, id, holdings = Decimal(100000000), ROI = Decimal(0), indexer_shares = {},
                indexer_revenues = {}, indexer_price = {}, indexer_realized_price = {}, indexer_yield = {},
                indexer_in_tokens = {}, private_price = None, private_yield = None, 
                indexer_locked_tokens = {}):
        self.id = id
        self.holdings = holdings
        self.ROI = ROI
        self.indexer_shares = indexer_shares
        self.indexer_revenues = indexer_revenues
        self.indexer_price = indexer_price
        self.indexer_realized_price = indexer_realized_price
        self.indexer_yield = indexer_yield
        self.indexer_in_tokens = indexer_in_tokens
        self.indexer_locked_tokens = indexer_locked_tokens
        