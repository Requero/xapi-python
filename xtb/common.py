import socket
from typing import Any, Dict


class FromDictMixin:

    @classmethod
    def from_dict(cls, dictionary: Dict[Any, Any]):
        return cls(**dictionary)  # noqa


def get_host_address(host: str, port: int) -> str:
    return socket.getaddrinfo(host, port)[0][4][0]
