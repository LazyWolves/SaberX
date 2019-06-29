import os
import socket
import ssl

class TCPHandler:

    @staticmethod
    def check_tcp(**kwargs):

        host = kwargs.get("host")
        port = kwargs.get("port", 80)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, int(port)))
            sock.shutdown(2)
            return True
        except socket.error:
            return False

    @staticmethod
    def check_tcp_ssl(**kwargs):

        host = kwargs.get("host")
        port = kwargs.get("port", 443)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
        ssl_sock = context.wrap_socket(sock, server_hostname=host)

        try:
            ssl_sock.connect((host, int(port)))
            ssl_sock.close()
            return True
        except:
            return False


    @staticmethod
    def  check_connection(**kwargs):
        pass
