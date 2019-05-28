from datetime import datetime

from server.extensions import db
from server.utils.abstract_models import BaseExchangeMixin


class CheckerRecord(BaseExchangeMixin, db.Model):
    __tablename__ = 'checker_records'

    deal_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    prediction_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    initial_price = db.Column(db.Float, nullable=True)
    predicted_price = db.Column(db.Float, nullable=False)
    real_price = db.Column(db.Float, nullable=True)
    is_checked = db.Column(db.Boolean, nullable=False, default=False)

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
