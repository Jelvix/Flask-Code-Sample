from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr

from server.extensions import db
from server.trade_data.exceptions import NoCurrencyPairBySymbolException, NoMarketByNameException
from server.trade_data.exchanges.models.stock_market import StockMarket
from server.trade_data.models.currency import CurrencyPair
from server.utils.base_model import BaseModel


class BaseExchangeMixin(BaseModel):
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    @declared_attr
    def currency_pair_id(self):
        return db.Column(db.Integer, db.ForeignKey('currency_pair.id'), nullable=False)

    @declared_attr
    def currency_pair(self):
        return db.relationship("CurrencyPair", foreign_keys=[self.currency_pair_id], lazy='subquery')

    @declared_attr
    def stock_market_id(self):
        return db.Column(db.Integer, db.ForeignKey('stock_market.id'), nullable=True)

    @declared_attr
    def stock_market(self):
        return db.relationship("StockMarket", foreign_keys=[self.stock_market_id], lazy='subquery')

    @classmethod
    def from_mapped_object(cls, mapped_object):
        new_object = cls()
        for prop in mapped_object.__dict__:
            if hasattr(new_object, prop):
                setattr(new_object, prop, mapped_object.__dict__[prop])
        return new_object

    def set_currency_pair_by_symbol(self, symbol):
        currency_pair = CurrencyPair.query.filter_by(symbol=symbol).first()
        if not currency_pair:
            raise NoCurrencyPairBySymbolException("Symbol: {}".format(symbol))
        self.currency_pair = currency_pair

    def set_market_by_name(self, market_name):
        market = StockMarket.query.filter_by(name=market_name).first()
        if not market:
            raise NoMarketByNameException("No market by name: {}".format(market_name))
        self.stock_market = market
