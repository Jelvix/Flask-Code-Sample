from server.extensions import db
from server.utils.base_model import BaseModel


class Balance(db.Model, BaseModel):
    __tablename__ = 'balances'

    balance = db.Column(db.Float, nullable=True, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship("User", foreign_keys=[user_id])

    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'),
                            nullable=False)
    currency = db.relationship("Currency", foreign_keys=[currency_id])

    market_id = db.Column(db.Integer, db.ForeignKey('stock_market.id'),
                          nullable=False)
    market = db.relationship("StockMarket", foreign_keys=[market_id])

    buy_percentage = db.Column(db.Float, nullable=True, default=0.5)
    sell_percentage = db.Column(db.Float, nullable=True, default=0.5)

    is_active = db.Column(db.Boolean, nullable=False, default=False)

    def to_json(self):
        return {
            "user": self.user.id,
            "balance": self.balance,
            "currency": self.currency.id,
            "market": self.market.id,
            "is_active": self.is_active,
        }

    def __repr__(self):
        return "{}\n{}\n{}".format(self.user.email, self.balance, self.currency.name)

    @property
    def sell_exchange_part(self):
        if self.sell_percentage is not None:
            return self.sell_percentage
        if self.user.sell_percentage is not None:
            return self.user.sell_percentage
        return 0.5

    @property
    def buy_exchange_part(self):
        if self.buy_percentage is not None:
            return self.buy_percentage
        if self.user.buy_percentage is not None:
            return self.user.buy_percentage
        return 0.5

    @staticmethod
    def get_by_user_and_market(user, stock_market_object, currency_pair_object, currency_attr="from_currency"):
        return Balance.query.filter_by(user=user, currency=getattr(currency_pair_object, currency_attr),
                                       market=stock_market_object).first()
