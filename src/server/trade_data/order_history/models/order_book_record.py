from server.extensions import db
from server.utils.abstract_models import BaseExchangeMixin


class OrderBookRecord(BaseExchangeMixin, db.Model):
    # ask if true else bid
    is_ask = db.Column(db.Boolean, nullable=False, default=True)

    # additional id field. For example 'lastUpdateId' in Binance
    original_source_id = db.Column(db.Integer, nullable=True)

    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    def __init__(self):
        pass

    def __repr__(self):
        return '<id: {}>, <timestamp: {}>, <from: {}>, <to: {}>, <price: {}>, <quantity: {}>'.format(
            self.id,
            self.timestamp,
            self.from_currency_id,
            self.to_currency_id,
            self.price,
            self.quantity)
