import itertools
import json
import socket
import ssl
import time
from typing import Any, Dict, List, Optional

from xtb import records
from xtb.common import get_host_address
from xtb.exceptions import XtbApiError, XtbSocketError


class XtbApi:
    END_TOKEN = b'\n\n'
    SLEEP_INTERVAL = 0.2
    CHUNK_SIZE = 8192
    JSON_INDENT = 4
    ENCODING = 'utf-8'

    def __init__(self, host: str = 'xapi.xtb.com', port: int = 5124):
        self._port = port
        self._host_address = get_host_address(host, port)
        self._is_logged_in = False
        self._socket: Optional[socket.socket] = None

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
        if self._socket is not None:
            raise XtbSocketError('Tried to connect() without calling close()')

        s = socket.socket()
        s.connect((self._host_address, self._port))
        self._socket = ssl.wrap_socket(s)

    def close(self):
        """
        Closes an existing connection and logouts the user
        if login() was called before
        Raises:
            XtbSocketError if close() was called before connect()
        """
        if self._socket is None:
            raise XtbSocketError('Tried to close() without calling connect()')
        if self._is_logged_in:
            self.logout()

        self._socket.close()
        self._socket = None

    def login(self, user: str, password: str,
              app_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Logins the user.
        See http://developers.xstore.pro/documentation/#login for more.
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
        return list(map(records.SymbolRecord.from_dict, response['returnData']))

    def get_calendar(self) -> List[records.CalendarRecord]:
        """
        Returns calendar with market events
        See http://developers.xstore.pro/documentation/#getCalendar
        """
        response = self._handle_command(command='getCalendar')
        return list(map(records.CalendarRecord.from_dict, response['returnData']))

    def get_symbol(self, symbol: str) -> records.SymbolRecord:
        arguments = {'symbol': symbol}
        response = self._handle_command(command='getSymbol', arguments=arguments)
        return records.SymbolRecord.from_dict(response['returnData'])

    def _handle_command(
            self,
            *,
            command: str,
            arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        if self._socket is None:
            raise XtbSocketError(
                'Tried to use the API without calling connect() first'
            )

        data = {'command': command}
        if arguments:
            data['arguments'] = arguments

        self._send_packet(data)
        response = self._get_response()
        self._raise_if_wrong_status(response)
        return response

    def _send_packet(self, data: Dict[str, Any]) -> None:
        packet = json.dumps(data, indent=self.JSON_INDENT)
        self._socket.send(packet.encode(self.ENCODING))
        time.sleep(self.SLEEP_INTERVAL)

    def _get_response(self) -> Dict[str, Any]:
        content = []
        while True:
            response = self._socket.recv(self.CHUNK_SIZE)
            end_idx = response.find(self.END_TOKEN)
            if end_idx != -1:
                content.append(response[:end_idx])
                break
            content.append(response)
        mapped = map(
            lambda x: x.decode(self.ENCODING),
            list(itertools.chain(content))
        )
        return json.loads(''.join(mapped))

    @staticmethod
    def _raise_if_wrong_status(response: Dict[str, Any]) -> None:
        if response.get('status', True):
            return
        error_code = response.get('errorCode', 'Unknown Error')
        description = response.get('errorDescr', 'Unknown Description')
        raise XtbApiError(code=error_code, description=description)
