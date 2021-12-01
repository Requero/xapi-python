from typing import Any, Dict, List, Optional, Type

from xtb import records
from xtb.connector import SyncConnector
from xtb.exceptions import XtbApiError, XtbSocketError


class XtbApi:
    def __init__(
            self,
            host: str = 'xapi.xtb.com',
            port: int = 5124,
            connector: Type[SyncConnector] = SyncConnector
    ) -> None:
        self._host = host
        self._port = port
        self._is_logged_in = False
        self._connector = connector()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """
        Creates the connection
        Raises:
            XtbSocketError if connect() was called more than once before close()
        """
        self._connector.connect(self._host, self._port)

    def close(self):
        """
        Closes an existing connection.
        Logouts the user if login() was called.
        Raises:
            XtbSocketError if close() was called before connect()
        """
        if self.is_connected() and self._is_logged_in:
            self.logout()
        self._connector.close()

    def is_connected(self) -> bool:
        return self._connector.is_connected()

    def login(self, user: str, password: str,
              app_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Logins the user.
        See http://developers.xstore.pro/documentation/#login
        """
        arguments = {'userId': user, 'password': password}
        if app_name is not None:
            arguments['appName'] = app_name
        response = self._handle_command(command='login', arguments=arguments)
        self._is_logged_in = True
        return response

    def logout(self) -> Dict[str, bool]:
        """
        Logouts the user.
        See http://developers.xstore.pro/documentation/#logout
        """
        response = self._handle_command(command='logout')
        self._is_logged_in = False
        return response

    def get_all_symbols(self) -> List[records.SymbolRecord]:
        """
        Returns array of symbols available for the user.
        See http://developers.xstore.pro/documentation/#getAllSymbols
        """
        response = self._handle_command(command='getAllSymbols')
        return records.cast_to_collection_of(
            records.SymbolRecord, response['returnData']
        )

    def get_calendar(self) -> List[records.CalendarRecord]:
        """
        Returns calendar with market events
        See http://developers.xstore.pro/documentation/#getCalendar
        """
        response = self._handle_command(command='getCalendar')
        return records.cast_to_collection_of(
            records.CalendarRecord, response['returnData']
        )

    def get_chart_last_request(
            self,
            period: int,
            start: int,
            symbol: str
    ) -> records.ChartResponse:
        """
        Returns chart info from start date to current time.
        Note that the streaming equivalent of this function is preferred.
        See http://developers.xstore.pro/documentation/#getChartLastRequest
        """
        # TODO: Possible values for period field via enum
        arguments = {
            'info': {'period': period, 'start': start, 'symbol': symbol}
        }
        response = self._handle_command(
            command='getChartLastRequest', arguments=arguments
        )
        return records.ChartResponse.from_dict(response['returnData'])

    def get_chart_range_request(
            self,
            end: int,
            period: int,
            start: int,
            symbol: str,
            ticks: int
    ) -> records.ChartResponse:
        """
        Returns chart info with data between given start and end dates
        Note that the streaming equivalent of this function is preferred.
        See http://developers.xstore.pro/documentation/#getChartRangeRequest
        """
        arguments = {
            'info': {
                'end': end, 'period': period, 'start': start,
                'symbol': symbol, 'ticks': ticks
            }
        }
        response = self._handle_command(
            command='getChartRangeRequest', arguments=arguments
        )
        return records.ChartResponse.from_dict(response['returnData'])

    def get_commission_def(
            self,
            symbol: str,
            volume: float
    ) -> records.CommissionRecord:
        """
        Returns calculation of commission and rate of exchange.
        See http://developers.xstore.pro/documentation/#getCommissionDef
        """
        args = {'symbol': symbol, 'volume': volume}
        response = self._handle_command(
            command='getCommissionDef', arguments=args
        )
        return records.CommissionRecord.from_dict(response['returnData'])

    def get_current_user_data(self) -> records.UserRecord:
        """
        Returns information about account currency, and account leverage.
        See http://developers.xstore.pro/documentation/#getCurrentUserData
        """
        response = self._handle_command(command='getCurrentUserData')
        return records.UserRecord.from_dict(response['returnData'])

    def get_margin_level(self):
        """
        Returns various account indicators.
        Note that the streaming equivalent of this function is preferred.
        See http://developers.xstore.pro/documentation/#getMarginLevel
        """
        response = self._handle_command(command='getMarginLevel')
        return records.MarginLevelRecord.from_dict(response['returnData'])

    def get_symbol(self, symbol: str) -> records.SymbolRecord:
        """
        Returns information about symbol available for the user.
        See http://developers.xstore.pro/documentation/#getSymbol
        """
        arguments = {'symbol': symbol}
        response = self._handle_command(command='getSymbol', arguments=arguments)
        return records.SymbolRecord.from_dict(response['returnData'])

    def get_margin_trade(
            self,
            symbol: str,
            volume: float
    ) -> records.MarginTradeRecord:
        """
        Returns expected margin for given instrument and volume.
        See http://developers.xstore.pro/documentation/#getMarginTrade
        """
        args = {'symbol': symbol, 'volume': volume}
        resp = self._handle_command(command='getMarginTrade', arguments=args)
        return records.MarginTradeRecord.from_dict(resp['returnData'])

    def get_news(self, start: int, end: int) -> List[records.NewsRecord]:
        """
        Returns news from trading server which were sent within specified
        period of time.
        Note that the streaming equivalent of this function is preferred.
        See http://developers.xstore.pro/documentation/#getNews
        """
        args = {'end': end, 'start': start}
        resp = self._handle_command(command='getNews', arguments=args)
        return records.cast_to_collection_of(
            records.NewsRecord, resp['returnData']
        )

    def _handle_command(
            self,
            *,
            command: str,
            arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self._connector.handle_command(
            command=command, arguments=arguments
        )
