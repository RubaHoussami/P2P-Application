from enum import Enum

class Currency(Enum):
    LBP = 422
    USD = 840

class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    TRANSFER = "TRANSFER"

currency_map = {currency.value: currency.name for currency in Currency}
