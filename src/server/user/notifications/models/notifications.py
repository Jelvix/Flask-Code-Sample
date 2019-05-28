from server.extensions import db
from server.utils.base_model import BaseModel


class NotificationEmail(BaseModel, db.Model):
    email = db.Column(db.String, nullable=False)

    def __str__(self):
        return self.email
