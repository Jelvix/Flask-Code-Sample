from server.extensions import db
from server.utils.abstract_models import BaseExchangeMixin


class CurrencyPurchaseTransactions(db.Model, BaseExchangeMixin):
    # transaction_open_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=True)
    # transaction_open = db.relationship("Transaction", foreign_keys=[transaction_open_id], lazy="subquery")

    # transaction_close_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=True)
    # transaction_close = db.relationship("Transaction", foreign_keys=[transaction_close_id], lazy="subquery")

    pnl = db.Column(db.Float, nullable=True, unique=False)
    initial_margin = db.Column(db.Float, nullable=True, unique=False)

    leverage = db.Column(db.Integer, default=1)
    liquidation_price = db.Column(db.Float, nullable=True, unique=False)

    def get_purchase_status(self):
        if self.transaction_close_id is None:
            return {"status": "active", "status-color": "#ff7400"}
        else:
            difference = self.transaction_open.previous_balance_from - self.transaction_close.after_balance_to
            if difference >= 0:
                return {"status": "profitable", "status-color": "#c10b0b"}
            elif difference < 0:
                return {"status": "unprofitable", "status-color": "#1b911b"}

    def to_json(self):
        item = {
            "date": str(self.timestamp),
            "pnl": self.pnl,
            "initial_margin": self.initial_margin,
            "currency_pair": str(self.currency_pair),
            "exchange": str(self.stock_market.name),
            "exchange_id": self.id,
            "leverage": self.leverage,
            "liquidation_price": self.liquidation_price
        }
        if self.transaction_close:
            item.update({"avr_sell_price": self.transaction_close.avg_sell_price})

        return item
