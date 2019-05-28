from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

from server.extensions import db


class StockHistory(db.Model):
    __tablename__ = 'stocks_history'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    stock_info = db.Column(JSON)

    def __init__(self, timestamp, stock_info):
        self.timestamp = timestamp
        self.stock_info = stock_info

    def __repr__(self):
        return '<id {}>'.format(self.id)
