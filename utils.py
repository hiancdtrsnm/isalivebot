import socket
import asyncio
from asyncio import Future
import time

def check_status(host: str, port: int, timeout=5):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    if result == 0:
        return 'alive'

    return 'dead'
