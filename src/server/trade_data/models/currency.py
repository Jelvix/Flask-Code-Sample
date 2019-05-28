from server.trade_data.exceptions import NoCurrencyPairBySymbolException
from server.extensions import db

from server.utils.base_model import BaseModel


class Currency(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    short_name = db.Column(db.String(10), unique=True, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "short_name": self.short_name,
        }


    def __repr__(self):
        return '<id: {}>, <name: {}>, <short_name: {}>'.format(self.id, self.name, self.short_name)


class CurrencyPair(db.Model, BaseModel):
    __tablename__ = 'currency_pair'

    symbol = db.Column(db.String(15), unique=True, nullable=False)

    from_currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    from_currency = db.relationship("Currency", foreign_keys=[from_currency_id], lazy='subquery')

    to_currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    to_currency = db.relationship("Currency", foreign_keys=[to_currency_id], lazy='subquery')

    @classmethod
    def get_by_symbol(cls, symbol):
        currency_pair = cls.query.filter_by(symbol=symbol).first()
        if not currency_pair:
            raise NoCurrencyPairBySymbolException(symbol)

        return currency_pair

    def __repr__(self):
        return self.symbol

    def get_market_repr(self, market_name):
        if market_name == "Binance":
            return self.binance_repr
        elif market_name == "Bitmex":
            return self.bitmex_repr
        return self.symbol

    def get_market_order_repr(self, market_name):
        if market_name == "Binance":
            return self.binance_order_repr
        elif market_name == "Bitmex":
            return self.bitmex_repr
        return self.symbol

    @property
    def bitmex_repr(self):
        return "{}/{}".format(self.to_currency.short_name.upper(), self.from_currency.short_name.upper())

    @property
    def binance_repr(self):
        return "{}{}".format(self.to_currency.short_name.upper(), self.from_currency.short_name.upper())

    @property
    def binance_order_repr(self):
        return "{}/{}".format(self.to_currency.short_name.upper(), self.from_currency.short_name.upper())


market_currencies = db.Table('market_currencies',
                             db.Column('currency_id', db.Integer, db.ForeignKey('currency.id'), primary_key=True),
                             db.Column('stock_market_id', db.Integer, db.ForeignKey('stock_market.id'),
                                       primary_key=True)
                             )
