from flask import request, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful_swagger import swagger
from werkzeug.exceptions import BadRequest

from server.user.permissions import roles_required
from server.utils.db_utils import create_action_log
from server.utils.view import check_0_max
from .models.stock_market import StockMarket


class Exchanges(Resource):
    @swagger.operation(
        responseClass=StockMarket.__name__,
        nickname='get',
        parameters=[
            {
                "name": "Authorization",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header",
                "description": "Bearer <token>"

            }
        ],
        responseMessages=[
            {
                "code": 403,
                "message": "For this endpoint your need one of these permissions: {0}, {1}".format('exchanges',
                                                                                                   'exchanges_only_read')
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required('exchanges', 'exchanges_only_read')
    def get(self):
        """
        List Stock market endpoint
        :return:
        """
        stock_markets = []
        for stock in StockMarket.query.all():
            stock_markets.append(stock.to_json())
        return stock_markets, 200

    @jwt_required
    @roles_required('exchanges')
    def post(self):
        """
        :return: status
        """
        return Response(status=201)

    @jwt_required
    @roles_required('exchanges')
    def delete(self):
        """
        Delete endpoint method
        Remove from db Stock Market object by it's name
        :data_example:{"id":"1"}
        :return: status
        """
        json_data = request.get_json()
        try:
            delete_sm = StockMarket.query.filter_by(id=json_data['id']).first()
            create_action_log("{0} was removed".format(delete_sm.name), "Exchanges")
            delete_sm.delete()
            return Response(status=204)
        except:
            BadRequest(description="Can't delete the object with current name or id")

    @swagger.operation(
        responseClass=StockMarket.__name__,
        parameters=[
            {
                "name": "body",
                "required": True,
                "allowMultiple": False,
                "dataType": "json",
                "paramType": "body",
                "description": '{"leverage": integer, "balance_percentage": integer, "id":string}'
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
                "message": "For this endpoint your need one of these permissions: {0}".format('exchanges')
            },
            {
                "code": 401,
                "message": "Token has expired"
            },
            {
                "message": 'ID is not in request',
                "code": 400
            },
            {
                "message": "Stock Market with current id is not found",
                "code": 204
            }
        ]
    )
    @jwt_required
    @roles_required('exchanges')
    def put(self):
        """
        The update Exchanges endpoint method
        :data_example:{"leverage": 11, "balance_percentage": 50, "id":"1"}
        :return: status code
        """
        json_data = request.get_json()
        if 'id' not in json_data:
            return 'ID is not in request', 400
        current_sm = StockMarket.query.filter_by(id=json_data['id']).first()
        if not current_sm:
            return "Stock Market with current id is not found", 204
        action = ""
        if 'balance_percentage' in json_data:
            balance_percentage = check_0_max(json_data['balance_percentage'], 100)
            if balance_percentage != current_sm.balance_percentage:
                action += "Balance percentage for {2} was changed from {0} to {1}.\n".format(
                    current_sm.balance_percentage, balance_percentage, current_sm.name)
                current_sm.balance_percentage = balance_percentage

        if 'leverage' in json_data:
            leverage = check_0_max(json_data['leverage'], current_sm.max_leverage)
            if leverage != current_sm.leverage:
                action += "Leverage for {2} was changed from {0} to {1}.".format(
                    current_sm.leverage, leverage, current_sm.name)
                current_sm.leverage = leverage

        current_sm.save()
        create_action_log(action, "Exchanges")
        return Response(status=200)

    swagger.add_model(StockMarket)
