from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful_swagger import swagger
from werkzeug.exceptions import BadRequest

from server.config import BaseConfig
from server.user.models.user import User, UserRole
from server.user.permissions import roles_required
from server.utils.db_utils import create_action_log, get_by_id


class UserManagement(Resource):
    @swagger.operation(
        responseClass=User.__name__,
        parameters=[
            {
                "name": "active",
                "required": False,
                "allowMultiple": False,
                "paramType": "query",
                "dataType": "bool",
                "description": "bool"
            },
            {
                "name": "Authorization",
                "required": True,
                "allowMultiple": False,
                "paramType": "header",
                "dataType": "string",
                "description": "Bearer <token>"
            }
        ],
        responseMessages=[
            {
                "code": 403,
                "message": "For this endpoint your need one of these permissions: {0}".format("user management")
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required('users management')
    def get(self):
        """
        :parameter:
            active:True/False
        :return:list of actived or deactived users and status
        """
        users = []
        args = request.args
        if 'active' not in args:
            raise BadRequest("Wrong parameters in request")
        for user in User.query.filter_by(is_active=args['active']).all():
            users.append({
                "fullname": user.full_name,
                "email": user.email,
                "id": user.id
            })
        return users, 200

    @swagger.operation(
        responseClass=User.__name__,
        parameters=[
            {
                "name": "body",
                "required": True,
                "allowMultiple": False,
                "dataType": "json",
                "paramType": "body",
                "description": """{"email": string, 
                "first_name": string, 
                "last_name":string,
                "role": list}"""
            },
            {
                "name": "Authorization",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            }
        ],
        responseMessages=[
            {
                "code": 403,
                "message": "For this endpoint your need one of these permissions: {0}".format("user management")
            },
            {
                "code": 401,
                "message": "Token has expired"
            },
            {
                "message": "Email not in request",
                "code": 422
            },
            {
                "message": "Invalid email",
                "code": 422
            },
            {
                "message":  "User with this email already exists.",
                "code": 409
            }
        ]
    )
    @jwt_required
    @roles_required("user management")
    def post(self):
        data = request.json
        if "email" not in data:
            return "Email not in request", 422
        if BaseConfig.DEFAULT_EMAIL_DOMAIN not in data['email']:
            return "Invalid email", 422
        if User.query.filter_by(email=data['email']).first():
            return "User with this email already exists.", 409
        new_user = User(email=data['email'])
        if "first_name" in data:
            new_user.first_name = data['first_name']
        if "last_name" in data:
            new_user.last_name = data['last_name']
        if "owner" in data['role']:
            new_user.add_role("owner")
            action = "Added {0} as owner.".format(data['email'])
        else:
            for each in data['role']:
                if not bool(UserRole.query.filter_by(role_name=each).first()):
                    role = UserRole(role_name=each)
                    role.save()
                new_user.add_role(each)
            action = "Added {0} as admin with access to {1}.".format(data['email'],
                                                                     ", ".join(new_user.get_user_roles_names_list))
        new_user.save()
        create_action_log(action, "UsersManagement")
        return 200

    @swagger.operation(
        responseClass=User.__name__,
        parameters=[
            {
                "name": "body",
                "required": True,
                "allowMultiple": False,
                "dataType": "json",
                "paramType": "body",
                "description": """{"email": string, 
                    "first_name": string, 
                    "last_name":string,
                    "id": integer,
                    "roles": list}"""
            },
            {
                "name": "Authorization",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            }
        ],
        responseMessages=[
            {
                "code": 403,
                "message": "For this endpoint your need one of these permissions: {0}".format("user management")
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required("user management")
    def put(self):
        """
        Method for updating info about user
        :return:
        """
        data = request.json
        try:
            edit_user = get_by_id(User, data['id'])
        except:
            BadRequest("ID not found in request")
        action = ""
        if "email" in data:
            action = "Updated email from {0} to {1} for {2}.".format(edit_user.email, data['email'],
                                                                     edit_user.full_name)
            edit_user.email = data['email']

        if "first_name" in data:
            action = "Updated first name from {0} to {1} for {2}.".format(edit_user.first_name, data['first_name'],
                                                                          edit_user.email)
            edit_user.first_name = data['first_name']
        if "last_name" in data:
            action = "Updated last name from {0} to {1} for {2}.".format(edit_user.last_name, data['last_name'],
                                                                         edit_user.email)
            edit_user.last_name = data['last_name']
        if "first_name" in data or "last_name" in data:
            edit_user.full_name = edit_user.get_full_name()
        edit_user.save()

        if "roles" in data:
            action = "Updated rights from {0} to {1} for {2}.".format(", ".join(edit_user.get_user_roles_names_list),
                                                                      ", ".join(data['roles']),
                                                                      edit_user.full_name)
            for role in data['roles']:
                edit_user.add_role(role)
        create_action_log(action, "UsersManagement")
        return 200

    @swagger.operation(
        responseClass=User.__name__,
        parameters=[
            {
                "name": "body",
                "required": True,
                "allowMultiple": False,
                "dataType": "json",
                "paramType": "body",
                "description": """{"id": integer}"""
            },
            {
                "name": "Authorization",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            }
        ],
        responseMessages=[
            {
                "code": 403,
                "message": "For this endpoint your need one of these permissions: {0}".format("user management")
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required("user management")
    def patch(self):
        """
        Method to activete or deactivate user
        :return:
        """
        data = request.json
        user = User.query.filter_by(id=data['id']).first()
        if user.is_active:
            user.is_active = False
            "Deactivated {0}.".format(user.email)
        else:
            user.is_active = True
            "Activated {0}.".format(user.email)
        return 200


class GetOneUser(Resource):
    @swagger.operation(
        responseClass=User.__name__,
        parameters=[
            {
                "name": "user_id",
                "required": False,
                "allowMultiple": False,
                "paramType": "path",
                "dataType": "bool",
                "description": "bool"
            },
            {
                "name": "Authorization",
                "required": True,
                "allowMultiple": False,
                "paramType": "header",
                "dataType": "string",
                "description": "Bearer <token>"
            }
        ],
        responseMessages=[
            {
                "code": 403,
                "message": "For this endpoint your need one of these permissions: {0}".format("user management")
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required("user management")
    def get(self, user_id):
        """
        Method return info about one user
        :return: info about user with this id and status
        """
        user_data = get_by_id(User, user_id)
        user = {
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "id": user_data.id
        }
        return user, 200
