from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful_swagger import swagger

from server.config import BaseConfig
from server.user.notifications.models.notifications import NotificationEmail
from server.user.permissions import roles_required
from server.utils.db_utils import create_action_log


class Notifications(Resource):
    @swagger.operation(
        responseClass=NotificationEmail.__name__,
        parameters=[
            {
                "name": "page",
                "required": False,
                "allowMultiple": False,
                "paramType": "query",
                "dataType": "integer",
                "description": "integer"
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
                "message": "For this endpoint your need one of these permissions: {0}, {1}".format('notifications',
                                                                                                   'notifications only read')
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required('notifications', 'notifications only read')
    def get(self):
        args = request.args
        page = int(args.get("page", 1))
        emails = []
        for em in NotificationEmail.query.paginate(page=page, per_page=10, error_out=True).items:
            emails.append({"email": em.email,
                           "id": em.id})
        return emails, 200

    @swagger.operation(
        responseClass=NotificationEmail.__name__,
        parameters=[
            {
                "name": "body",
                "required": True,
                "allowMultiple": False,
                "dataType": "json",
                "paramType": "body",
                "description": '{"email": string}'
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
                "message": "For this endpoint your need one of these permissions: {0}".format('notifications')
            },
            {
                "code": 401,
                "message": "Token has expired"
            },
            {
                "code": 422,
                "message": "Email not in request"
            },
            {
                "code": 422,
                "message": "Invalid email"
            },
            {
                "code": 409,
                "message": "User with this email already exists."
            }


        ]
    )
    @jwt_required
    @roles_required('notifications')
    def post(self):
        data = request.json
        if "email" not in data:
            return "Email not in request", 422
        if BaseConfig.DEFAULT_EMAIL_DOMAIN not in data['email']:
            return "Invalid email", 422
        if NotificationEmail.query.filter_by(email=data['email']).first():
            return "User with this email already exists.", 409
        notif_email = NotificationEmail(email=data['email'])
        notif_email.save()
        create_action_log("Added {0}.".format(data['email']), "Notifications")
        return 200

    @swagger.operation(
        responseClass=NotificationEmail.__name__,
        parameters=[
            {
                "name": "ids",
                "required": False,
                "allowMultiple": False,
                "paramType": "query",
                "dataType": "list",
                "description": "list of integers"
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
                "message": "For this endpoint your need one of these permissions: {0}".format('notifications')
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required('notifications')
    def delete(self):
        args = request.args
        if "ids" not in args:
            return "ID not in request", 422
        for each in args.getlist("ids"):
            del_email = NotificationEmail.query.filter_by(id=each).first()
            del_email.delete()
            create_action_log("Removed {0}.".format(args['email']), "Notifications")
        return 200
