from enum import Enum


class TransactionStatusEnum(Enum):
    UNKNOWN = -1
    SUCCESS = 1
    FAIL = 2
    NOT_ENOUGH_BALANCE = 3
    USER_DOES_NOT_HAVE_FROM_BALANCE = 4
    USER_DOES_NOT_HAVE_TO_BALANCE = 5
    SELL_PERCENTAGE_IS_UNKNOWN = 6
    BUY_PERCENTAGE_IS_UNKNOWN = 7
    UNSUPPORTED_TYPE_OF_TRANSACTION = 8
    USER_DOES_NOT_HAVE_PERCENTAGE = 9
    USER_DOES_NOT_HAVE_BALANCE = 10
    USER_CHANGE_MARGIN_TRANSACTION = 11
    TRANSACTION_EXCEPTION = 12


class TransactionResult(object):
    def __init__(self):
        self.is_success = False
        self.status = TransactionStatusEnum.FAIL
        self.error = None
        self.transaction = None
