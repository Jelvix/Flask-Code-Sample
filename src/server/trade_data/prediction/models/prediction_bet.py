from datetime import datetime

from server.extensions import db
from server.utils.abstract_models import BaseExchangeMixin
from server.utils.transactions.transaction_result import TransactionResult
from server.utils.transactions.transactions_utils import make_virtual_transaction
from server.trade_data.models.currency import CurrencyPair
from server.trade_data.prediction.models.remembered_points import RememberedPoints


class PredictionBet(BaseExchangeMixin, db.Model):
    __tablename__ = 'prediction_bets'

    bet_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    bet_price = db.Column(db.Float, nullable=True)
    coins_amount = db.Column(db.Float, nullable=False)
    strategy_name = db.Column(db.String(300), unique=False, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship("User", foreign_keys=[user_id], lazy='selectin')

    checker_record_id = db.Column(db.Integer, db.ForeignKey('checker_records.id'),
                                  nullable=True)
    checker_record = db.relationship("CheckerRecord", foreign_keys=[checker_record_id])

    open_transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'),
                                    nullable=True)
    open_transaction = db.relationship("Transaction", foreign_keys=[open_transaction_id], lazy='subquery')

    close_transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'),
                                     nullable=True)
    close_transaction = db.relationship("Transaction", foreign_keys=[close_transaction_id], lazy='subquery')

    is_buy = db.Column(db.Boolean, nullable=True, default=False)

    is_opened = db.Column(db.Boolean, nullable=False, default=False)
    is_closed = db.Column(db.Boolean, nullable=False, default=False)

    def to_dataframe_analysis_dict(self):
        return {
            "currency_pair_id": self.currency_pair_id,
            "stock_market_id": self.stock_market_id,
            "deal_time": self.deal_time,
            "prediction_time": self.prediction_time,
            "initial_price": self.initial_price,
            "predicted_price": self.predicted_price,
            "real_price": self.real_price,
            "is_checked": self.is_checked,
        }

    def save_empty_bet(self):
        self.coins_amount = 0
        self.is_opened = False
        self.is_buy = None
        self.save()

    def is_profitable(self, current_price):
        if not self.open_transaction:
            return False

        sell_amount = self.open_transaction.buy_amount * current_price
        sell_amount_with_fee = sell_amount - sell_amount * self.stock_market.transaction_fee

        if sell_amount_with_fee > self.open_transaction.sell_amount:
            return True
        return False

    def close_with_current_price(self, current_price):
        from_currency = self.currency_pair.from_currency
        to_currency = self.currency_pair.to_currency

        reverse_currency_pair = CurrencyPair.query.filter_by(from_currency=to_currency,
                                                             to_currency=from_currency).first()
        if not reverse_currency_pair:
            result = TransactionResult()
            return result

        return make_virtual_transaction(reverse_currency_pair, self.stock_market, self.user, current_price,
                                        check_if_enough_money=False)

    def open_with_current_price(self, current_price, quantity):
        from_currency = self.currency_pair.from_currency
        to_currency = self.currency_pair.to_currency

        reverse_currency_pair = CurrencyPair.query.filter_by(from_currency=from_currency,
                                                             to_currency=to_currency).first()
        if not reverse_currency_pair:
            result = TransactionResult()
            return result

        return make_virtual_transaction(reverse_currency_pair, self.stock_market, self.user, current_price,
                                        check_if_enough_money=False)

    def is_growth(self, current_price):
        remembered_points = RememberedPoints.query.filter_by(bet_id=self.id).order_by(RememberedPoints.timestamp).all()
        if not remembered_points:
            return True
        if current_price > remembered_points[-1].price:
            return True

        return False

    def save_point(self, price):
        point = RememberedPoints()
        point.bet = self
        point.price = price
        point.save()

