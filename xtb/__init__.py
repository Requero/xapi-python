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

    def get_chart_last_request(self, period: int, start: int, symbol: str):
        """
        Returns chart info from start date to current time.
        Note that the streaming equivalent of this function is preferred.
        See http://developers.xstore.pro/documentation/#getChartLastRequest
        """
        arguments = {'info': {
            'period': period, 'start': start, 'symbol': symbol
        }}
        return self._handle_command(
            command='getChartLastRequest', arguments=arguments
        )

    def get_chart_range_request(self):
        pass

    def get_symbol(self, symbol: str) -> records.SymbolRecord:
        arguments = {'symbol': symbol}
        response = self._handle_command(command='getSymbol', arguments=arguments)
        return records.cast_to(records.SymbolRecord, response['returnData'])

    def _handle_command(
            self,
            *,
            command: str,
            arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self._connector.handle_command(
            command=command, arguments=arguments
        )
