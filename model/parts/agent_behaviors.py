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
    subgraphs = {}
    for indexer_id, indexer in indexers.items():        
        # delegate_front_runner is delegate id 1.
        # try:
        for subgraph_id, subgraph in indexer.subgraphs.items():
            subgraphs[subgraph_id] = subgraph
        # except AttributeError:
        #     subgraphs = subgraphs
    agent = indexers[1]
    inpt = {
                'available_subgraphs': subgraphs,
                'currentPeriod': s['epoch'],
                'delegation_unbonding_period': params['unbonding_days'],
                'account_balance': agent.holdings,
                'change_cut': params['change_cut']
            }
    agent.inputs(inpt)
        # this populates an action into the agent object.
    agent.get_action()
    key = 'indexers'
    return key, indexers
