"""
utils functions for simplifying work with database and flask sqlalchemy
"""
from datetime import datetime

from flask_jwt_extended import get_jwt_identity

from server.trade_data.logbook.models.actions_log import ActionLog, Screen
from server.user.models.user import User


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_or_abort(model, object_id):
    result = model.query.get(object_id)
    return result


def get_flat_list(entities_list):
    return [x[0] for x in entities_list]


def get_by_id(cls, object_id):
    obj = cls.query.filter_by(id=object_id).first()
    return obj


def create_action_log(action, screen):
    if action != "":
        user = User.query.filter_by(email=get_jwt_identity()).first()
        action_log = ActionLog(user_id=user.id, user=user, action_date=datetime.now(),
                               action=action, screen=Screen(value=screen))
        action_log.save()
        return 200
    return "Action not found"


