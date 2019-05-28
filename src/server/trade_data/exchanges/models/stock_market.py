from server.extensions import db
from server.trade_data.exceptions import NoMarketByNameException
from server.trade_data.models.currency import market_currencies
from server.utils.base_model import BaseModel



class StockMarket(db.Model, BaseModel):
    __tablename__ = 'stock_market'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    web_address = db.Column(db.String(200), unique=True, nullable=True)
    currencies = db.relationship('Currency', secondary=market_currencies, lazy='subquery',
                                 backref=db.backref('stock_markets', lazy=True))

    leverage = db.Column(db.Integer, default=1)
    max_leverage = db.Column(db.Integer, default=leverage)
    balance_percentage = db.Column(db.Integer, default=0)

    transaction_fee = db.Column(db.Float, nullable=True, default=0.001)

    is_available = db.Column(db.Boolean, nullable=True, default=True)

    is_trading_active = db.Column(db.Boolean, default=False)
    is_terminate_all_required = db.Column(db.Boolean, default=False)

    def to_json(self, currencies=False):
        result = {
            "id": self.id,
            "name": self.name,
            "web_address": self.web_address,
            "leverage": self.leverage,
            "balance_percentage": self.balance_percentage
        }

        if currencies:
            result["currencies"] = [currency.to_json() for currency in self.currencies]

        return result

    def __repr__(self):
        return "<id: {}>, <name: {}>".format(self.id, self.name)

    @staticmethod
    def get_by_name(market_name):
        market = StockMarket.query.filter_by(name=market_name).first()
        if not market:
            raise NoMarketByNameException("No market by name: {}".format(market_name))
        return market
