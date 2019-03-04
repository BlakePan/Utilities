# -*- coding: utf-8 -*-
import socket
import json


def recv_from_socket(_socket: socket, buf_size:int = 4096)->(str, None):
    """
    Receive msg from a socket

    :param _socket:
    :param buf_size:
    :return:
    """
    data, addr = _socket.recvfrom(buf_size)
    if not data:
        return None
    data = json.loads(data.decode("utf-8"))
    return data
