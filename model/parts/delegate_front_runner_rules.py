from heuristic_agent import HeuristicAgent
from rules import Rules

class DelegateFrontRunnerRules(Rules):
    
    def __init__(self, G):
        self._rules = {
            'delegate' : {
                'event'    : "delegate",
                'target'   : None,
                'amount'   : G,
                'status'   : "have delegated"
            },
            'claim' : {
                'event'    : "claim",
                'target'   : None,
                'status'   : "have sent claim()"
            },
            'undelegate' : {
                'event'    : "undelegate",
                'target'   : None,
                'status'   : "have sent undelegate()"
            },
            'withdraw' : {
                'event'    : "withdraw",
                'target'   : None,
                'status'   : "have sent withdrawDelegation()"
            },
            'checkBalance' : {
                'event'    : "checkAccountBalance",
                'target'   : '<account address>',
                'status'   : "have sent checkAccountBalance"
            },
            'clear' : {
                'event'    : None,
                'target'   : None,
                'status'   : "have cleared delegation"
            }  
        }
