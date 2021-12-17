from delegate_front_runner import DelegateFrontRunner
def agent_actions(params, step, sL, s, inputs):
    agent = s['agents'][0]
    inpt = {
                'availableIndexers'         : newInput['availableIndexers'],
                'currentPeriod'             : newInput['currentPeriod'],
                'disputeChannelEpochs'      : newInput['disputeChannelEpochs'],
                'delegationUnbondingPeriod' : newInput['delegationUnbondingPeriod'],
                'accountBalance'            : newInput['accountBalance']
            }
        
    
    agent.inputs(inpt)