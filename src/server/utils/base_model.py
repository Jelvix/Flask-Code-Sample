from sqlalchemy.exc import InvalidRequestError

from server.extensions import db


class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except InvalidRequestError:
            self.merge_save()

    def merge_save(self):
        db.session.expunge(self)
        local_object = db.session.merge(self)
        db.session.add(local_object)
        db.session.commit()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except InvalidRequestError:
            self.merge_save()
