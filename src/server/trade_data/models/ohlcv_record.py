from datetime import datetime

from server.extensions import db
from server.utils.abstract_models import BaseExchangeMixin


class OHLCVRecord(BaseExchangeMixin, db.Model):
    __tablename__ = 'ohlcv_records'

    open_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)

    def to_dataframe_analysis_dict(self):
        return {
            "open_time": self.open_time,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
        }

    def to_python_types(self):
        self.open = float(self.open)
        self.high = float(self.high)
        self.low = float(self.low)
        self.close = float(self.close)
        self.volume = float(self.volume)

    def __str__(self):
        return str(self.to_dataframe_analysis_dict())
