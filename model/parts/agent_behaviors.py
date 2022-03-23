# from .delegate_front_runner import DelegateFrontRunner
def get_agent_actions_next_timestep(params, step, sL, s, inputs):
    # To generate an event, two methods would need to be called on an instantiation of an agent object 
    # (“agent”):
    # agent.inputs(Inputs), where Inputs contains the info the agent needs to update their state and set 
    # an action--in practice this could just be the previous state of the system + system parameters, 
    # as per usual
    # output = agent.getAction(), which triggers the agent workflow and stores the output of the agent 
    # in output; this would then be parsed to extract events according to the agent’s output schema.
        
    # indexers = s['indexers']

    # for indexer in indexers.values():

    # agent = indexer.delegators[1]  #NOTE: this is not the agent

    # NOTE: Agent has to be in the portfolio.
    delegator_portfolios = s['delegator_portfolios']
    agent = delegator_portfolios[1]

    inpt = {
                'available_indexers': s['indexers'],
                'current_period': s['epoch'],
                'dispute_channel_epochs': params['dispute_channel_epochs'],
                'allocation_days': params['allocation_days'],
                'delegation_unbonding_period_epochs': params['delegation_unbonding_period_epochs'],
                'account_balance': agent.holdings,
                'delegation_tax_rate': params['delegation_tax_rate'],
                'minimum_delegation_period_epochs': params['minimum_delegation_period_epochs'],
            }
    agent.inputs(inpt)
    # this populates an action into the agent object.
    agent.get_action()
    key = 'delegator_portfolios'
    return key, delegator_portfolios
