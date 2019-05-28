from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful_swagger import swagger

from server.trade_data.exchanges.models.stock_market import StockMarket
from server.user.permissions import roles_required
from server.utils.db_utils import get_by_id, create_action_log


class StartStopTrading(Resource):
    @swagger.operation(
        responseClass=StockMarket.__name__,
        parameters=[
            {
                "name": "body",
                "required": False,
                "allowMultiple": False,
                "paramType": "body",
                "dataType": "body",
                "description": """{
                    "stock_market_id":integer,
                    "screen": string
                    }"""
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
                "message": "For this endpoint your need one of these permissions: {0}".format('stop/start trading')
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required('stop/start trading')
    def post(self):
        """
        Method to start trading
        :return:
        """
        data = request.json
        stock_market = get_by_id(StockMarket, data['stock_market_id'])
        stock_market.is_trading_active = True
        stock_market.save()
        create_action_log("Started Trading", data['screen'])
        return 200

    @swagger.operation(
        responseClass=StockMarket.__name__,
        parameters=[
            {
                "name": "body",
                "required": False,
                "allowMultiple": False,
                "paramType": "body",
                "dataType": "body",
                "description": """{
                    "stock_market_id":integer,
                    "screen": string
                    }"""
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
                "message": "For this endpoint your need one of these permissions: {0}".format('stop/start trading')
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required('stop/start trading')
    def delete(self):
        """
        Method to stop trading
        :return:
        """
        data = request.json
        stock_market = get_by_id(StockMarket, data['stock_market_id'])
        stock_market.is_trading_active = False
        stock_market.save()
        create_action_log("Stopped Trading", data['screen'])
        return 200


class TerminateAllOrders(Resource):
    @swagger.operation(
        responseClass=StockMarket.__name__,
        parameters=[
            {
                "name": "body",
                "required": False,
                "allowMultiple": False,
                "paramType": "body",
                "dataType": "body",
                "description": """{
                "stock_market_id":integer,
                "screen": string
                }"""
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
                "message": "For this endpoint your need one of these permissions: {0}".format('terminate all orders')
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required('terminate all orders')
    def delete(self):
        data = request.json
        stock_market = get_by_id(cls=StockMarket, object_id=data['stock_market_id'])
        stock_market.is_terminate_all_required = True
        stock_market.save()
        create_action_log("Terminated all orders", data['screen'])
        return 200



