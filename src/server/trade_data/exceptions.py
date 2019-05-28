from server.trade_data.exception_handlers import no_currency_in_db_by_short_name_exception_handler


class NoMarketByNameException(Exception):
    pass


class NoCurrencyPairBySymbolException(Exception):
    pass


class NoCurrencyByShortNameException(Exception):
    pass


def register_errors(app):
    app.register_error_handler(NoCurrencyByShortNameException, no_currency_in_db_by_short_name_exception_handler)
