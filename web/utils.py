import socket

def get_host_ip():
    return socket.gethostbyname(socket.gethostname())
