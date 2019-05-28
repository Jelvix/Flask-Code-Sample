from server.extensions import db
from server.utils.abstract_models import BaseExchangeMixin
from server.utils.base_model import BaseModel


class Transaction(BaseExchangeMixin, db.Model, BaseModel):
    __tablename__ = 'transactions'

    price = db.Column(db.Float, nullable=False)

    sell_amount = db.Column(db.Float, nullable=False)
    buy_amount = db.Column(db.Float, nullable=False)

    fee = db.Column(db.Float, nullable=False)

    previous_balance_from = db.Column(db.Float, nullable=False)
    previous_balance_to = db.Column(db.Float, nullable=False)

    after_balance_from = db.Column(db.Float, nullable=False)
    after_balance_to = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship("User", foreign_keys=[user_id])

    is_completed = db.Column(db.Boolean, unique=False, default=False)

    # average price buy/sell
    avg_buy_price = db.Column(db.Float, nullable=True, unique=False)
    avg_sell_price = db.Column(db.Float, nullable=True, unique=False)

    def __init__(self):
        pass

    def __repr__(self):
        return '<pair: {}>, <buy amount: {}>, <price: {}>, <fee: {}>, complete: {}'.format(self.currency_pair.symbol,
                                                                                           self.buy_amount, self.price,
                                                                                           self.fee,
                                                                                           self.is_completed)
