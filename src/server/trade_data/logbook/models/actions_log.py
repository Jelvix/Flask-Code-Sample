from datetime import datetime
import enum

from server.utils.base_model import BaseModel
from server.extensions import db


class Screen(enum.Enum):
    EXCHANGES = "Exchanges"
    NOTIFICATIONS = "Notifications"
    LOGBOOK = "Logbook"
    USER_MANAGEMENT = "UsersManagement"
    ORDER_HISTORY = "OrderHistory"

    def __str__(self):
        return self.value


class ActionLog(db.Model, BaseModel):
    __tablename__ = "action_logs"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship("User", foreign_keys=[user_id], lazy='selectin')

    action_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    action = db.Column(db.String(), nullable=False)
    screen = db.Column(db.Enum(Screen), nullable=False)

    def to_json(self):
        return {"action_date": str(self.action_date),
                "user_id": self.user_id,
                "full_name": str(self.user.full_name),
                "action": self.action,
                "screen": self.screen.value}
