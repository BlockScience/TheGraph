# from .delegate_front_runner import DelegateFrontRunner
def get_agent_actions_next_timestep(params, step, sL, s, inputs):
    # To generate an event, two methods would need to be called on an instantiation of an agent object 
    # (“agent”):
    # agent.inputs(Inputs), where Inputs contains the info the agent needs to update their state and set 
    # an action--in practice this could just be the previous state of the system + system parameters, 
    # as per usual
    # output = agent.getAction(), which triggers the agent workflow and stores the output of the agent 
    # in output; this would then be parsed to extract events according to the agent’s output schema.
        
    # agents = s['agents']    
    # agent = agents[0]
    indexers = s['indexers']
    for indexer in indexers.values():        
        # delegate_front_runner is delegate id 1.
        agent = indexer.delegators[1]

        inpt = {
                    'availableIndexers'         : s['indexers'],
                    'currentPeriod'             : s['epoch'],
                    'disputeChannelEpochs'      : params['dispute_channel_epochs'],
                    'allocationDays'            : params['allocation_days'],
                    'delegationUnbondingPeriod' : params['unbonding_days'],
                    'accountBalance'            : agent.holdings
                }
            
        
        agent.inputs(inpt)
        # action = agent.getAction()
        # this populates an action into the agent object.
        agent.getAction()
    key = 'indexers'
    return key, indexers