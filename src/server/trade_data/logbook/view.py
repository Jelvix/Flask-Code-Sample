from datetime import datetime, timedelta

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful_swagger import swagger
from sqlalchemy import and_

from server.user.permissions import roles_required
from .models.actions_log import ActionLog, Screen


class LogBook(Resource):
    @swagger.operation(
        responseClass=ActionLog.__name__,
        parameters=[
            {
                "name": "page",
                "required": False,
                "allowMultiple": False,
                "paramType": "query",
                "dataType": "integer",
                "in": "path"
            },
            {
                "name": "filter_screen",
                "required": False,
                "allowMultiple": False,
                "paramType": "query",
                "dataType": "integer",
                "description": "string"
            },
            {
                "name": "filter_users",
                "required": False,
                "allowMultiple": False,
                "paramType": "query",
                "dataType": "integer",
                "description": "integer"
            },
            {
                "name": "start_date",
                "required": False,
                "allowMultiple": False,
                "paramType": "query",
                "description": "2019-03-27",
                "dataType": "string"
            },
            {
                "name": "end_date",
                "required": False,
                "allowMultiple": False,
                "paramType": "query",
                "dataType": "string",
                "description": "2019-03-27"
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
                "message": "For this endpoint your need one of these permissions: {0}".format('logbook')
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required('logbook')
    def get(self):
        """
        List of logs endpoint
        :return: list, status
        """
        args = request.args
        page = int(args.get("page", 1))
        filters = []
        if "filter_screen" in args:
            filter_screen = [screen for screen in Screen if screen.value in args.getlist('filter_screen')]
            filters.append(ActionLog.screen.in_(filter_screen))
        if "filter_users" in args:
            filter_users = args.getlist("filter_users")
            filters.append(ActionLog.user_id.in_(filter_users))
        if 'start_date' in args:
            start_date = datetime.strptime(args['start_date'], '%Y-%m-%d')
            filters.append(ActionLog.action_date >= start_date)
            if 'end_date' in request.args:
                end_date = datetime.strptime(args['end_date'], '%Y-%m-%d')
                end_date += timedelta(days=1)
            else:
                end_date = start_date + timedelta(days=1)
            filters.append(ActionLog.action_date < end_date)

        query_action_logs = ActionLog.query.filter(and_(*filters)).paginate(page=page, per_page=10, error_out=True)

        logs_book = []
        for logs in query_action_logs.items:
            logs_book.append(logs.to_json())

        logs_book.append({'number_of_pages': query_action_logs.pages,
                          "current_page": query_action_logs.page,
                          "has_next_page": query_action_logs.has_next,
                          "has_prev_page": query_action_logs.has_prev})

        return logs_book, 200
