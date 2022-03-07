from .rules import Rules

class IndexSpoofingRules(Rules):
    def __init__(self, tokens, indexingRewardCut,
                waitingPeriod):
        super().__init__()
        self._rules = {
            'stake' : {
                'event'    : "stake",
                'type'     : "stakeDepositeds",
                'target'   : None,
                'tokens'   : tokens,
                'status'   : "have staked to self"
            },
            'delegate': {
                'event': "delegate",
                'type': 'stakeDelegateds',
                'indexer': None,
                'tokens': tokens,
                'status': "have delegated to self",
            },
            'open' : {
                'event'    : "open",
                'type'     : "allocationCreateds",
                'target'   : None,
                'tokens'   : tokens,
                'status'   : "have opened an allocation"
            },
            'set_cut'  : {
                'event'    : "set indexingRewardCut",
                'type'     : "delegationParametersUpdateds",
                'target'   : None,
                'amount'   : indexingRewardCut,
                'status'   : "have set indexingRewardCut"
            },
            'wait' : {
                'event'    : None,
                'target'   : None,
                'amount'   : waitingPeriod,
                'status'   : "am waiting"
            },
            'close' : {
                'event'    : "close",
                'type'     : "allocationCloseds",
                'target'   : None,
                'status'   : "have closed an allocation"
            },
            'undelegate': {
                'event': "undelegate",
                'type': 'stakeDelegatedLockeds',
                'indexer': None,
                'status': "have sent undelegate()",
            },
            'withdraw': {
                'event': "withdraw",
                'type': 'stakeDelegatedWithdrawns',
                'indexer': None,
                'status': "have sent withdrawDelegation()"
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