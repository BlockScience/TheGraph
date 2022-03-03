from .portfolio import Portfolio
from decimal import Decimal


def delegate_portfolio(params, step, sL, s, inputs):
    if params['portfolio_tracking']:
        portfolios = s['delegator_portfolios']
        event = inputs['event'][0] if inputs['event'] is not None else None
        delegation_tax_rate = params['delegation_tax_rate']
        print(event['delegator'])
        if event['delegator'] in params['delegator_list'] or len(params['delegator_list']) == 0:
            indexerID = event['indexer']
            delegatorID = event['delegator']
            indexer = s['indexers'][event['indexer']]
            pool_delegated_stake = indexer.pool_delegated_stake
            if delegatorID not in portfolios:
                portfolio = Portfolio(delegatorID)
                portfolios[delegatorID] = portfolio
            else:
                portfolio = portfolios[delegatorID]
            portfolio.holdings -= event['tokens'] / (1 - delegation_tax_rate)
            shares = sum([d.shares for d in indexer.delegators.values()])
            if indexerID not in portfolio.indexer_in_tokens:
                portfolio.indexer_in_tokens[indexerID] = event['tokens'] / (1 - delegation_tax_rate)
            else:
                portfolio.indexer_in_tokens[indexerID] = event['tokens'] / (1 - delegation_tax_rate) # to calculate ROI, won't sum to pool delegated stake 
            if indexerID not in portfolio.indexer_shares:
                portfolio.indexer_shares[indexerID] = event['tokens'] if pool_delegated_stake.is_zero() \
                                                     else (event['tokens'] / pool_delegated_stake) * shares
            else:
                portfolio.indexer_shares[indexerID] = event['tokens'] if pool_delegated_stake.is_zero() \
                                                     else (event['tokens'] / pool_delegated_stake) * shares
            portfolio.indexer_price[indexerID] = portfolio.indexer_shares[indexerID] / portfolio.indexer_in_tokens[indexerID]
            if indexerID not in portfolio.delegate_block_number and event.get('blockNumber') is not None:
                portfolio.delegate_block_number[indexerID] = []
                portfolio.delegate_block_number[indexerID].append(event['blockNumber'])
            elif event.get('blockNumber') is not None:
                portfolio.delegate_block_number[indexerID].append(event['blockNumber'])               
            portfolio.gas_spent += params['delegation_gas_cost']
        key = 'delegator_portfolios'
        return key, s['delegator_portfolios']
    else:
        return 'delegator_portfolios', s['delegator_portfolios']


def undelegate_portfolio(params, step, sL, s, inputs):
    if params['portfolio_tracking']:
        portfolios = s['delegator_portfolios']
        event = inputs['event'][0] if inputs['event'] is not None else None    
        if event['delegator'] in params['delegator_list'] or len(params['delegator_list']) == 0:
            indexerID = event['indexer']
            delegatorID = event['delegator']
            portfolio = portfolios[delegatorID]
            indexer = s['indexers'][event['indexer']]
            pool_delegated_stake = indexer.pool_delegated_stake
            pool_shares = indexer.shares
            
            # tokens are not of the event for undelegate so this will always go to the else case
            if indexerID not in portfolio.indexer_locked_tokens and event.get('shares') is not None:
                portfolio.indexer_locked_tokens[indexerID] = event['shares'] * pool_delegated_stake / pool_shares
            elif event.get('shares') is not None:
                portfolio.indexer_locked_tokens[indexerID] += event['shares'] * pool_delegated_stake / pool_shares
            # else:
            #     portfolio.indexer_locked_tokens[indexerID] = {}# portfolio.indexer_locked_tokens[indexerID] #CHANGE FROM indexer_in_tokens on right side
                
            # if indexerID not in portfolio.indexer_shares and event.get('shares') is not None:
            #     portfolio.indexer_shares[indexerID] -= event['shares']
            if event.get('shares') is not None:
                portfolio.indexer_shares[indexerID] -= event['shares']
            else:
                portfolio.indexer_shares[indexerID] = portfolio.indexer_shares[indexerID]
                
                
            portfolio.gas_spent += params['undelegate_gas_cost']
        key = 'delegator_portfolios'
        return key, s['delegator_portfolios']
    else:
        return 'delegator_portfolios', s['delegator_portfolios']
        
    
def withdraw_portfolio(params, step, sL, s, inputs):
    if params['portfolio_tracking']:
        portfolios = s['delegator_portfolios']
        event = inputs['event'][0] if inputs['event'] is not None else None    
        if event['delegator'] in params['delegator_list'] or len(params['delegator_list']) == 0:
            indexerID = event['indexer']
            delegatorID = event['delegator']
            portfolio = portfolios[delegatorID]
            portfolio.holdings += event['tokens']
            if indexerID not in portfolio.indexer_locked_tokens:
                portfolio.indexer_locked_tokens[indexerID] = event['tokens']
            else:
                portfolio.indexer_locked_tokens[indexerID] -= event['tokens']
            if indexerID not in portfolio.indexer_revenues:
                portfolio.indexer_revenues[indexerID] = event['tokens']
            else:
                portfolio.indexer_revenues[indexerID] += event['tokens']
            if indexerID not in portfolio.withdraw_block_number and event['blockNumber']:
                portfolio.withdraw_block_number[indexerID] = []
                portfolio.withdraw_block_number[indexerID].append(event['blockNumber'])
            elif event['blockNumber']:
                portfolio.delegate_block_number[indexerID].append(event['blockNumber'])
            investment_time = portfolio.withdraw_block_number[indexerID][-1] - portfolio.delegate_block_number[indexerID][0] 
            if indexerID not in portfolio.indexer_ROI_time:
                portfolio.indexer_ROI_time[indexerID] = 1/Decimal(investment_time) * (portfolio.indexer_revenues[indexerID] / portfolio.indexer_in_tokens[indexerID]) + 1
            else:
                portfolio.indexer_ROI_time[indexerID] = 1/Decimal(investment_time) * (portfolio.indexer_revenues[indexerID] / portfolio.indexer_in_tokens[indexerID]) + 1
            portfolio.indexer_ROI[indexerID] = (portfolio.indexer_revenues[indexerID] / portfolio.indexer_in_tokens[indexerID]) + 1
            portfolio.indexer_realized_price[indexerID] = portfolio.indexer_shares[indexerID] / portfolio.indexer_revenues[indexerID]
            portfolio.ROI = sum(portfolio.indexer_ROI.values()) 
            portfolio.ROI_time = sum(portfolio.indexer_ROI_time.values())
            portfolio.gas_spent += params['withdraw_gas_cost']
        key = 'delegator_portfolios'
        return key, s['delegator_portfolios']
    else:
        return 'delegator_portfolios', s['delegator_portfolios']
        