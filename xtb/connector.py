import itertools
import json
import socket
import ssl
import time
from typing import Any, Dict, List, Optional

from xtb.exceptions import XtbApiError, XtbSocketError


class SyncConnector:
    END_TOKEN = b'\n\n'
    SLEEP_INTERVAL = 0.2
    CHUNK_SIZE = 8192
    JSON_INDENT = 4
    ENCODING = 'utf-8'

    def __init__(self):
        self._socket: Optional[socket.socket] = None

    def connect(self, host: str, port: int) -> None:

        def get_host_address() -> str:
            return socket.getaddrinfo(host, port)[0][4][0]

        if self.is_connected():
            raise XtbSocketError('Tried to connect() without calling close()')

        host_address = get_host_address()
        s = socket.socket()
        s.connect((host_address, port))
        self._socket = ssl.wrap_socket(s)

    def close(self) -> None:
        if not self.is_connected():
            raise XtbSocketError('Tried to close() without calling connect()')

        self._socket.close()
        self._socket = None

    def is_connected(self) -> bool:
        return self._socket is not None

    def handle_command(
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
        return self._response_to_dict(content)

    def _response_to_dict(self, content: List[bytes]) -> Dict[str, Any]:
        # TODO: Raise
        mapped = map(
            lambda x: x.decode(self.ENCODING), itertools.chain(content)
        )
        return json.loads(''.join(mapped))

    @staticmethod
    def _raise_if_wrong_status(response: Dict[str, Any]) -> None:
        if response.get('status', True):
            return
        error_code = response.get('errorCode', 'Unknown Error')
        description = response.get('errorDescr', 'Unknown Description')
        raise XtbApiError(code=error_code, description=description)
