import os
import socket

class TCPHandler:

    @staticmethod
    def check_tcp(**kwargs):

        host = kwargs.get("host")
        port = kwargs.get("port")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, int(port)))
            sock.shutdown(2)
            return True
        except socket.error as err:
            return False


    def check_tcp_ssl(**kwargs):
        pass

    def  check_connection(**kwargs):
        pass
