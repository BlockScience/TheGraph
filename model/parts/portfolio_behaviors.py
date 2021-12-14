from .portfolio import Portfolio
from decimal import Decimal

def delegate_portfolio(params, step, sL, s, inputs):
    portfolios = s['delegator_portfolios']
    event = inputs['delegation_events'][0] if inputs['delegation_events'] is not None else None
    delegation_tax_rate = params['delegation_tax_rate']
    if event:
        indexerID = event['indexer']
        delegatorID = event['delegator']
        indexer = s['indexers'][event['indexer']]
        pool_delegated_stake = indexer.pool_delegated_stake
        if delegatorID not in portfolios.keys():
            portfolio = Portfolio(delegatorID)
            portfolios[delegatorID] = portfolio
        else:
            portfolio = portfolios[delegatorID]
        portfolio.holdings -= event['tokens'] / (1 - delegation_tax_rate)
        shares = sum([d.shares for d in indexer.delegators.values()])
        if indexerID not in portfolio.indexer_in_tokens.keys():
            portfolio.indexer_in_tokens[indexerID] = event['tokens'] / (1 - delegation_tax_rate)
        else:
            portfolio.indexer_in_tokens[indexerID] += event['tokens'] / (1 - delegation_tax_rate) # to calculate ROI, won't sum to pool delegated stake 
        if indexerID not in portfolio.indexer_shares.keys():
            portfolio.indexer_shares[indexerID] = event['tokens'] if pool_delegated_stake.is_zero() \
                                                     else (event['tokens'] / pool_delegated_stake) * shares
        else:
            portfolio.indexer_shares[indexerID] += event['tokens'] if pool_delegated_stake.is_zero() \
                                                     else (event['tokens'] / pool_delegated_stake) * shares
        portfolio.indexer_price[indexerID] = portfolio.indexer_shares[indexerID] / portfolio.indexer_in_tokens[indexerID]
        if indexerID not in portfolio.delegate_block_number.keys():
            portfolio.delegate_block_number[indexerID] = []
            portfolio.delegate_block_number[indexerID].append(event['blockNumber'])
        else:
            portfolio.delegate_block_number[indexerID].append(event['blockNumber'])
        # value based on average of 2-3 most common gas costs from etherscan, still figuring out best source to obtain actual data
        portfolio.gas_spent += 96286
    key = 'delegator_portfolios'
    return key, s['delegator_portfolios']

def undelegate_portfolio(params, step, sL, s, inputs):
    portfolios = s['delegator_portfolios']
    event = inputs['undelegation_events'][0] if inputs['undelegation_events'] is not None else None    
    if event:
        indexerID = event['indexer']
        delegatorID = event['delegator']
        indexer = s['indexers'][event['indexer']]
        portfolio = portfolios[delegatorID]
        if indexerID not in portfolio.indexer_locked_tokens.keys():
            portfolio.indexer_locked_tokens[indexerID] = event['tokens']
        else:
            portfolio.indexer_locked_tokens[indexerID] += event['tokens']
        # value based on average of 2-3 most common gas costs from etherscan, still figuring out best source to obtain actual data
        portfolio.gas_spent += 107389
    key = 'delegator_portfolios'
    return key, s['delegator_portfolios']
        
    
def withdraw_portfolio(params, step, sL, s, inputs):
    portfolios = s['delegator_portfolios']
    event = inputs['withdraw_events'][0] if inputs['withdraw_events'] is not None else None    
    if event:
        indexerID = event['indexer']
        delegatorID = event['delegator']
        indexer = s['indexers'][event['indexer']]
        portfolio = portfolios[delegatorID]
        portfolio.holdings += event['tokens']
        if indexerID not in portfolio.indexer_locked_tokens.keys():
            portfolio.indexer_locked_tokens[indexerID] = event['tokens']
        else:
            portfolio.indexer_locked_tokens[indexerID] -= event['tokens']
        if indexerID not in portfolio.indexer_revenues.keys():
            portfolio.indexer_revenues[indexerID] = event['tokens']
        else:
            portfolio.indexer_revenues[indexerID] += event['tokens']
        if indexerID not in portfolio.withdraw_block_number.keys():
            portfolio.withdraw_block_number[indexerID] = []
            portfolio.withdraw_block_number[indexerID].append(event['blockNumber'])
        else:
            portfolio.delegate_block_number[indexerID].append(event['blockNumber'])
        investment_time = portfolio.withdraw_block_number[indexerID][-1] - portfolio.delegate_block_number[indexerID][0] 
        if indexerID not in portfolio.indexer_ROI_time.keys():
            portfolio.indexer_ROI_time[indexerID] = 1/Decimal(investment_time) * (portfolio.indexer_revenues[indexerID] / portfolio.indexer_in_tokens[indexerID]) + 1
        else:
            portfolio.indexer_ROI_time[indexerID] = 1/Decimal(investment_time) * (portfolio.indexer_revenues[indexerID] / portfolio.indexer_in_tokens[indexerID]) + 1
        portfolio.indexer_ROI[indexerID] = (portfolio.indexer_revenues[indexerID] / portfolio.indexer_in_tokens[indexerID]) + 1
        portfolio.indexer_realized_price[indexerID] = portfolio.indexer_shares[indexerID] / portfolio.indexer_revenues[indexerID]
        portfolio.ROI = sum(portfolio.indexer_ROI.values()) 
        portfolio.ROI_time = sum(portfolio.indexer_ROI_time.values())
        # value based on average of 2-3 most common gas costs from etherscan, still figuring out best source to obtain actual data
        portfolio.gas_spent += 52101
    key = 'delegator_portfolios'
    return key, s['delegator_portfolios']
        