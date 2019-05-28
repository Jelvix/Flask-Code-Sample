from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from .models.user import User


def roles_required(*roles_needed):
    def required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            email = get_jwt_identity()
            user = User.query.filter_by(email=email).first()
            roles = user.get_user_roles_names_list
            if 'owner' in roles:
                return fn(*args, **kwargs)
            for role_needed in roles_needed:
                if role_needed in roles:
                    return fn(*args, **kwargs)
            return "For this endpoint your need one of these permissions: {0}".format(roles_needed), 403
        return wrapper
    return required
