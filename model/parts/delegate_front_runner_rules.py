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
                'status': "have delegated",
                'blockNumber': 11522107
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
                'status': "have sent undelegate()",
                'blockNumber': 11522303
            },
            'withdraw': {
                'event': "withdraw",
                'type': 'stakeDelegatedWithdrawns',
                'indexer': None,
                'status': "have sent withdrawDelegation()"
            },
            'checkBalance': {
                'event': "checkaccount_balance",
                'indexer': '<account address>',
                'status': "have sent checkaccount_balance"
            },
            'clear': {
                'event': None,
                'indexer': None,
                'status': "have cleared delegation"
            }  
        }
