from .heuristic_agent import HeuristicAgent
from .delegate_front_runner_rules import DelegateFrontRunnerRules


class DelegateFrontRunner(HeuristicAgent):

    def __init__(self, delegator_id, rules: DelegateFrontRunnerRules,
                 initialaccount_balance):
        super().__init__(delegator_id, rules, initialaccount_balance)
        self._inputs = []
        self.state = [
            {
                # get this from indexer.delegators
                'delegations': {},
            }
        ]
    
    def inputs(self, newInput):
        # todo: only save current input, no need for all historical inputs.
        self._inputs.append(
            {
                'available_indexers': newInput['available_indexers'],
                'current_period': newInput['current_period'],
                'dispute_channel_epochs': newInput['dispute_channel_epochs'],
                'allocation_days': newInput['allocation_days'],
                'delegation_unbonding_period_epochs': newInput['delegation_unbonding_period_epochs'],
                'account_balance': newInput['account_balance'],
                'delegation_tax_rate': newInput['delegation_tax_rate'],
                'minimum_delegation_period_epochs': newInput['minimum_delegation_period_epochs'],
            }
        )

    # this only works for one indexer currently because delegator is an attribute of an indexer.
    def generate_plan(self):
        # if self.output exists then this timestep is actually already an agent action.  zero out the plan here and move onto the next timestep.
        if self.output:
            self.plan = {}
            return
        
        inpt = self._inputs[-1]
        strategy = self._strategies[-1]
        current_period = inpt['current_period']
        print(f'{current_period=}')                        
        plan = {}

        # For each available indexer, the FRD checks to see if they have already delegated to that indexer.
        for indexer in inpt['available_indexers'].values():            
            
            # If the FRD has not delegated to that indexer, they check to see what the available allocations are for that indexer.
            if not self.is_delegated() and not self.is_undelegated():  # should we delegate?
                for subgraph_id, subgraph in indexer.subgraphs.items():
                    allocations = [allocation for allocation in subgraph.allocations.values() if allocation.tokens != 0]
                    # allocations = subgraph.allocations.values()
                    for allocation in allocations:
                        # If there is an allocation from that indexer which is available to delegate to, the FRD checks to see if the allocation may shortly close (this depends upon the starting time of the allocation, i.e. how long it has been open).
                        if current_period == allocation.start_period + inpt['allocation_days'] - 1:  # allocation time in days/epochs
                            # If the allocation may shortly close, the FRD delegates to that allocation, for that indexer, if they have the available funds to do so. This is the start of the front-running attack.
                            if self.holdings > 0:
                                plan = strategy['delegate']
                                plan['delegator'] = self.id
                                plan['indexer'] = indexer.id
                                plan['tokens'] = self.holdings * (1 - inpt['delegation_tax_rate'])
                                plan['allocationID'] = allocation.allocation_id
                                plan['subgraphDeploymentID'] = subgraph_id
                                plan['until'] = current_period + inpt['minimum_delegation_period_epochs']
                                self.plan = plan
                                return
            # If the FRD has delegated to that indexer, the FRD checks to see if it’s time to begin the process of undelegating.
            else:  # should we undelegate or withdraw?
                # if FRD has delegated and not yet undelegated, check if he should undelegate.
                allocation = indexer.subgraphs[self.subgraph_id].allocations[self.allocation_id]
                if not self.is_undelegated():  # should we undelegate?
                    # for subgraph in indexer.subgraphs.values():
                    #     allocation = indexer.subgr
                    #     for allocation in subgraph.allocations.values():

                    # If enough time has passed to allow undelegation to commence (this depends upon the time allowed for disputes to resolve), the FRD first checks to see if the allocation has already closed, or if indexing rewards have already been claimed.
                    if current_period >= allocation.start_period + inpt['allocation_days'] + inpt['dispute_channel_epochs']:
                        # If the allocation has already closed and indexing rewards have already been claimed, the FRD undelegates from that indexer.
                        # If the allocation has already closed but indexing rewards have not been claimed, the FRD issues a claim for the indexing rewards.
                        # NOTE: allocation_closed and claim events always occur in the same timeblock, so if the allocation closed, we should undelegate.
                        allocation_closed = allocation.tokens == 0
                        if allocation_closed:
                            if current_period >= self.locked_in_delegation_until:
                                plan = strategy['undelegate']
                                plan['delegator'] = self.id
                                plan['indexer'] = indexer.id
                                plan['shares'] = self.shares
                                plan['until'] = current_period + inpt['delegation_unbonding_period_epochs']
                                self.plan = plan
                                return
                else:  # should we withdraw?  if FRD has undelegated already and has tokens locked in undelegation
                    # If enough time has passed to allow withdrawing their delegation to commence (this depends upon both the time allowed for disputes to resolve, and upon the unbonding period for delegators), the FRD checks to see if they’ve already undelegated, or if they’ve already withdrawn their delegation.
                    if current_period >= allocation.start_period + inpt['allocation_days'] + inpt['dispute_channel_epochs'] + inpt['delegation_unbonding_period_epochs']:
                        # If they’ve already undelegated, they withdraw their delegation.
                        if current_period >= self.locked_in_undelegation_until:
                            plan = strategy['withdraw']
                            plan['delegator'] = self.id
                            plan['indexer'] = indexer.id
                            plan['tokens'] = self.undelegated_tokens
                            self.plan = plan
                            return
                        # If they’ve already withdrawn their delegation, they check to see if their available funds has increased due to their withdrawn delegation.
                        # NOTE: nothing needs to be done here.
                        # If their available funds has increased, they stop keeping track of this delegation and clear it from their memory. This is the end of the front-running attack.
                        # NOTE: nothing needs to be done here.
        self.plan = plan

    def generate_output(self):
        self.output = []
        if self.plan:
            # output must be a list of events.
            self.output.append(self.plan)


