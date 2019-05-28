from server.trade_data.order_history.models.transaction import Transaction
from server.user.models.balance import Balance
from server.utils.transactions.transaction_result import TransactionResult, TransactionStatusEnum


def make_virtual_transaction(currency_pair_object, stock_market_object, user, price, check_if_enough_money=False):
    transaction_result = TransactionResult()

    transaction = Transaction()
    transaction.currency_pair = currency_pair_object
    transaction.stock_market = stock_market_object
    transaction.user = user

    from_balance = Balance.query.filter_by(user=user, currency=currency_pair_object.from_currency,
                                           market=stock_market_object).first()
    if not from_balance:
        transaction_result.status = TransactionStatusEnum.USER_DOES_NOT_HAVE_FROM_BALANCE
        return transaction_result

    to_balance = Balance.query.filter_by(user=user, currency=currency_pair_object.to_currency,
                                         market=stock_market_object).first()
    if not to_balance:
        transaction_result.status = TransactionStatusEnum.USER_DOES_NOT_HAVE_TO_BALANCE
        return transaction_result

    sell_percentage = from_balance.sell_percentage

    if not sell_percentage:
        user_balance_sell = user.sell_percentage
        if not user_balance_sell:
            transaction_result.status = TransactionStatusEnum.SELL_PERCENTAGE_IS_UNKNOWN
            return transaction_result
        sell_percentage = user_balance_sell

    exchange_rate = min(sell_percentage, 1)

    transaction.price = price

    if from_balance.balance == 0:
        transaction_result.status = TransactionStatusEnum.NOT_ENOUGH_BALANCE
        return transaction_result

    transaction.previous_balance_from = from_balance.balance
    transaction.previous_balance_to = to_balance.balance

    transaction_fee = stock_market_object.transaction_fee
    if transaction_fee is None:
        transaction_fee = 0
    transaction.fee = transaction_fee

    sell_amount = exchange_rate * from_balance.balance
    sell_with_fee = sell_amount + sell_amount * transaction_fee

    if sell_with_fee > from_balance.balance:
        if check_if_enough_money:
            transaction_result.status = TransactionStatusEnum.NOT_ENOUGH_BALANCE
            return transaction_result
        sell_with_fee = from_balance.balance
        sell_amount = sell_with_fee / (1 + transaction_fee)

    from_balance.balance -= sell_with_fee

    transaction.sell_amount = sell_amount

    buy_amount = sell_amount * price
    transaction.buy_amount = buy_amount

    to_balance.balance += buy_amount

    transaction.after_balance_from = from_balance.balance
    transaction.after_balance_to = to_balance.balance

    transaction.save()
    transaction_result.transaction = transaction

    transaction_result.is_success = True
    transaction_result.status = TransactionStatusEnum.SUCCESS
    return transaction_result
