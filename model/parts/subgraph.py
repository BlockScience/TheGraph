class Subgraph:
    def __init__(self):
        # these are the cumulative fees collected by the parent indexer for this subgraph.
        # Q_i
        self.indexing_fees = 0

        # Q_q
        self.query_fees = 0

        self.allocations = {}  # key is allocationID, value is allocation object.

    @property
    def tokens(self):
        return sum(allocation.tokens for allocation in self.allocations.values())
        
    def ROI_indexing(self):
        print(f'{self.indexing_fees=}, {self.tokens=}')
        return (self.indexing_fees + self.tokens) / self.tokens

    def ROI_query(self):
        print(f'{self.query_fees=}, {self.tokens=}')
        return (self.query_fees + self.tokens) / self.tokens

        
