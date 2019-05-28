from server.trade_data.exchanges.view import Exchanges
from server.trade_data.logbook.view import LogBook
from server.trade_data.order_history.view import OrderHistory
from server.trade_data.trading_view import TerminateAllOrders, StartStopTrading
from server.user.notifications.view import Notifications
from server.user.user_manager.view import UserManagement, GetOneUser


def api_urls(api):
    api.add_resource(Exchanges,  '/exchanges/')
    api.add_resource(OrderHistory,  '/order_history/')
    api.add_resource(LogBook, '/logbook/')
    api.add_resource(TerminateAllOrders, '/terminate_all_orders/')
    api.add_resource(StartStopTrading, '/start_stop_trading/')
    api.add_resource(UserManagement, '/user_management/')
    api.add_resource(GetOneUser, '/user_management/<user_id>')
    api.add_resource(Notifications, '/notifications/')
