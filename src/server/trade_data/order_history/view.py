from flask_jwt_extended import jwt_required
from flask_restful_swagger import swagger

from server.user.permissions import roles_required
from .models.currency_purchase_transactions import CurrencyPurchaseTransactions

from flask_restful import Resource
from flask import request
from sqlalchemy import and_
from datetime import datetime, timedelta


class OrderHistory(Resource):
    @swagger.operation(
        responseClass=CurrencyPurchaseTransactions.__name__,
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
                "name": "filter_trade_market",
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
                "message": "For this endpoint your need one of these permissions: {0}".format('order history')
            },
            {
                "code": 401,
                "message": "Token has expired"
            }
        ]
    )
    @jwt_required
    @roles_required('order history')
    def get(self):
        """
        Lists of transactions endpoint
        :return:list, status 200
        """
        args = request.args
        page = int(args.get('page', 1))
        filters = []
        if "filter_trade_market" in args:
            filter_trade_market = request.args.getlist('filter_trade_market')
            filters.append(CurrencyPurchaseTransactions.stock_market_id.in_(filter_trade_market))
        if 'start_date' in request.args:
            start_date = datetime.strptime(args['start_date'], '%Y-%m-%d')
            filters.append(CurrencyPurchaseTransactions.timestamp >= start_date)
            if 'end_date' in request.args:
                end_date = datetime.strptime(args['end_date'], '%Y-%m-%d')
                end_date += timedelta(days=1)
            else:
                end_date = start_date + timedelta(days=1)
            filters.append(CurrencyPurchaseTransactions.timestamp < end_date)

        query_current = CurrencyPurchaseTransactions.query.filter(and_(*filters)).paginate(page=page,
                                                                                           per_page=10,
                                                                                           error_out=True)

        transactions = []
        for transaction in query_current.items:
            data = transaction.to_json()
            data.update(transaction.get_purchase_status())
            transactions.append(data)

        transactions.append({'number_of_pages': query_current.pages,
                             "current_page": query_current.page,
                             "has_next_page": query_current.has_next,
                             "has_prev_page": query_current.has_prev})

        return transactions, 200
