from datetime import datetime

from server.extensions import db
from server.utils.base_model import BaseModel


class RememberedPoints(BaseModel, db.Model):
    __tablename__ = 'remembered_points'

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    price = db.Column(db.Float, nullable=False)
    bet_id = db.Column(db.Integer, db.ForeignKey('prediction_bets.id'),
                       nullable=False, index=True)
    bet = db.relationship("PredictionBet", foreign_keys=[bet_id], lazy='subquery')
