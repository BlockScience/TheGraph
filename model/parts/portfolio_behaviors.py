from .portfolio import Portfolio
from decimal import Decimal

def delegate_portfolio(params, step, sL, s, inputs):
    if params['portfolio_tracking'] == True:
        portfolios = s['delegator_portfolios']
        event = inputs['event'][0] if inputs['event'] is not None else None
        delegation_tax_rate = params['delegation_tax_rate']
        print(event['delegator'])
        if event['delegator'] in params['delegator_list'] or len(params['delegator_list']) == 0:
            indexerID = event['indexer']
            delegatorID = event['delegator']
            indexer = s['indexers'][event['indexer']]
            pool_delegated_stake = indexer.pool_delegated_stake
            try:
                portfolios[delegatorID]
            except KeyError:
                portfolio = Portfolio(delegatorID)
                portfolios[delegatorID] = portfolio
            else:
                portfolio = portfolios[delegatorID]
            portfolio.holdings -= event['tokens'] / (1 - delegation_tax_rate)
            shares = sum([d.shares for d in indexer.delegators.values()])
            try:
                portfolio.indexer_in_tokens[indexerID]
            except KeyError:
                portfolio.indexer_in_tokens[indexerID] = event['tokens'] / (1 - delegation_tax_rate)
            else:
                portfolio.indexer_in_tokens[indexerID] += event['tokens'] / (1 - delegation_tax_rate) # to calculate ROI, won't sum to pool delegated stake 
            try:
                portfolio.indexer_shares[indexerID]
            except KeyError:
                portfolio.indexer_shares[indexerID] = event['tokens'] if pool_delegated_stake.is_zero() \
                                                     else (event['tokens'] / pool_delegated_stake) * shares
            else:
                portfolio.indexer_shares[indexerID] += event['tokens'] if pool_delegated_stake.is_zero() \
                                                     else (event['tokens'] / pool_delegated_stake) * shares
            portfolio.indexer_price[indexerID] = portfolio.indexer_shares[indexerID] / portfolio.indexer_in_tokens[indexerID]
            try:
                portfolio.delegate_block_number[indexerID]
            except KeyError:
                portfolio.delegate_block_number[indexerID] = []
                portfolio.delegate_block_number[indexerID].append(event['blockNumber'])
            else:
                portfolio.delegate_block_number[indexerID].append(event['blockNumber'])
            portfolio.gas_spent += params['delegation_gas_cost']
        key = 'delegator_portfolios'
        return key, s['delegator_portfolios']
    else:
        return 'delegator_portfolios', s['delegator_portfolios']

def undelegate_portfolio(params, step, sL, s, inputs):
    if params['portfolio_tracking'] == True:
        portfolios = s['delegator_portfolios']
        event = inputs['event'][0] if inputs['event'] is not None else None    
        if event['delegator'] in params['delegator_list'] or len(params['delegator_list']) == 0:
            indexerID = event['indexer']
            delegatorID = event['delegator']
            portfolio = portfolios[delegatorID]
            try:
                portfolio.indexer_locked_tokens[indexerID]
            except KeyError:
                portfolio.indexer_locked_tokens[indexerID] = event['tokens']
            else:
                portfolio.indexer_locked_tokens[indexerID] += event['tokens']
            # value based on average of 2-3 most common gas costs from etherscan, still figuring out best source to obtain actual data
            portfolio.gas_spent += params['undelegate_gas_cost']
        key = 'delegator_portfolios'
        return key, s['delegator_portfolios']
    else:
        return 'delegator_portfolios', s['delegator_portfolios']
        
    
def withdraw_portfolio(params, step, sL, s, inputs):
    if params['portfolio_tracking'] == True:
        portfolios = s['delegator_portfolios']
        event = inputs['event'][0] if inputs['event'] is not None else None    
        if event['delegator'] in params['delegator_list'] or len(params['delegator_list']) == 0:
            indexerID = event['indexer']
            delegatorID = event['delegator']
            portfolio = portfolios[delegatorID]
            portfolio.holdings += event['tokens']
            try:
                portfolio.indexer_locked_tokens[indexerID]
            except KeyError:
                portfolio.indexer_locked_tokens[indexerID] = event['tokens']
            else:
                portfolio.indexer_locked_tokens[indexerID] -= event['tokens']
            try:
                portfolio.indexer_revenues[indexerID]
            except KeyError:
                portfolio.indexer_revenues[indexerID] = event['tokens']
            else:
                portfolio.indexer_revenues[indexerID] += event['tokens']
            try:
                portfolio.withdraw_block_number[indexerID]
            except KeyError:
                portfolio.withdraw_block_number[indexerID] = []
                portfolio.withdraw_block_number[indexerID].append(event['blockNumber'])
            else:
                portfolio.delegate_block_number[indexerID].append(event['blockNumber'])
            investment_time = portfolio.withdraw_block_number[indexerID][-1] - portfolio.delegate_block_number[indexerID][0] 
            try:
                portfolio.indexer_ROI_time[indexerID]
            except KeyError:
                portfolio.indexer_ROI_time[indexerID] = 1/Decimal(investment_time) * (portfolio.indexer_revenues[indexerID] / portfolio.indexer_in_tokens[indexerID]) + 1
            else:
                portfolio.indexer_ROI_time[indexerID] = 1/Decimal(investment_time) * (portfolio.indexer_revenues[indexerID] / portfolio.indexer_in_tokens[indexerID]) + 1
            portfolio.indexer_ROI[indexerID] = (portfolio.indexer_revenues[indexerID] / portfolio.indexer_in_tokens[indexerID]) + 1
            portfolio.indexer_realized_price[indexerID] = portfolio.indexer_shares[indexerID] / portfolio.indexer_revenues[indexerID]
            portfolio.ROI = sum(portfolio.indexer_ROI.values()) 
            portfolio.ROI_time = sum(portfolio.indexer_ROI_time.values())
            # value based on average of 2-3 most common gas costs from etherscan, still figuring out best source to obtain actual data
            portfolio.gas_spent += params['withdraw_gas_cost']
        key = 'delegator_portfolios'
        return key, s['delegator_portfolios']
    else:
        return 'delegator_portfolios', s['delegator_portfolios']
        