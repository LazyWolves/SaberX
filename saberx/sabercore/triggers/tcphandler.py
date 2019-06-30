import os
import socket
import ssl
import traceback

class TCPHandler:

    @staticmethod
    def check_tcp(**kwargs):

        host = kwargs.get("host")
        port = kwargs.get("port", 80)
        timeout = kwargs.get("timeout", 5)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
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
        timeout = kwargs.get("timeout", 5)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
        ssl_sock = context.wrap_socket(sock, server_hostname=host)

        try:
            ssl_sock.connect((host, int(port)))
            ssl_sock.close()
            return True
        except socket.error:
            return False


    @staticmethod
    def  check_connection(**kwargs):

        host = kwargs.get("host")
        port = kwargs.get("port", 80)
        ssl = kwargs.get("ssl", False)
        timeout = kwargs.get("timeout", 5)
        attemps = kwargs.get("attempts", 1)
        threshold = kwargs.get("threshold", 1)
        check_type = kwargs.get("check_type", "tcp_fail")


        if ssl:
            check = TCPHandler.check_tcp_ssl
        else:
            check = TCPHandler.check_tcp

        count = 0

        for attempt in range(attemps):
            print ("checking...")
            check_result = check(host=host, port=port, timeout=timeout)

            if check_result:
                if check_type == "tcp_connect":
                    count += 1
            else:
                if check_result == "tcp_fail":
                    count += 1

        if count >= threshold:
            return True

        return False

if __name__ == "__main__":
    print (TCPHandler.check_connection(host="www.media.net", port=1111, check_type="tcp_connect", attempts=2))
