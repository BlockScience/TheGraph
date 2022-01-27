from .rules import Rules


class DelegateFrontRunnerRules(Rules):
    def __init__(self, tokens):
        super().__init__()
        self._rules = {
            'delegate': {
                'event': "delegate",
                'type': 'stakeDelegateds',
                'indexer': None,
                'tokens': tokens,
                'status': "have delegated"
            },
            'claim': {
                'event': "claim",
                'indexer': None,
                'status': "have sent claim()"
            },
            'undelegate': {
                'event': "undelegate",
                'type': 'stakeDelegatedLockeds',
                'indexer': None,
                'status': "have sent undelegate()"
            },
            'withdraw': {
                'event': "withdraw",
                'type': 'stakeDelegatedWithdrawns',
                'indexer': None,
                'status': "have sent withdrawDelegation()"
            },
            'checkBalance': {
                'event': "checkAccountBalance",
                'indexer': '<account address>',
                'status': "have sent checkAccountBalance"
            },
            'clear': {
                'event': None,
                'indexer': None,
                'status': "have cleared delegation"
            }  
        }
