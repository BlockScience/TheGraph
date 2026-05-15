class Subgraph():
    def __init__(self):
        # these are the cumulative fees collected by the parent indexer for this subgraph.

        # R
        self.tokens = 0

        # Q_i
        self.indexing_fees = 0

        # Q_q
        self.query_fees = 0
        
    def ROI_indexing(self):
        print(f'{self.indexing_fees=}, {self.tokens=}')
        return (self.indexing_fees + self.tokens) / self.tokens

    def ROI_query(self):
        print(f'{self.query_fees=}, {self.tokens=}')
        return (self.query_fees + self.tokens) / self.tokens

        
