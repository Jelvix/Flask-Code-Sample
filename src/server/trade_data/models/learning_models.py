from datetime import datetime

from server.extensions import db


class LearningModel(db.Model):
    __tablename__ = 'learning_model'

    id = db.Column(db.Integer, primary_key=True)

    model_name = db.Column(db.String(400), nullable=False)
    specification = db.Column(db.String(400), nullable=True)
    uuid = db.Column(db.String(400), unique=True, nullable=False, index=True)

    created = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)
    last_update = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)

    is_learning = db.Column(db.Boolean, nullable=False, default=False)

    weights = db.relationship('LearningModelWeights', backref='learning_model', lazy=True)

    @classmethod
    def get_by_uuid(cls, uuid):
        instance = cls.query.filter_by(uuid=uuid).first()
        return instance


class LearningModelWeights(db.Model):
    __tablename__ = 'learning_model_weights'

    id = db.Column(db.Integer, primary_key=True)

    model_id = db.Column(db.Integer, db.ForeignKey('learning_model.id'),
                         nullable=False)

    version = db.Column(db.Integer, primary_key=False)

    created = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)

    learning_result = db.Column(db.Float, nullable=True)

    s3_url = db.Column(db.String(400), nullable=False)
