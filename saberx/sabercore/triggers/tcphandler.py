"""
.. module:: tcphandler
   :synopsis: Module for evaluating tcptrigger trigger.
"""

import os
import socket
import ssl
import traceback


class TCPHandler:

    """
        **Class containing TCP handler methods**
    """

    @staticmethod
    def check_tcp(**kwargs):
        """
            **Check tcp connection to a host**

            This method tries to open a tcp connection to a host.

            Args:
                kwargs (dict): dict containing host, port and timeout

            Returns:
                bool: Whether the tcp connection could be established or not.
        """

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

        """
            **Check tcp connection with ssl to a host**

            This method tries to open a ssl tcp connection to a host.

            Args:
                kwargs (dict): dict containing host, port and timeout

            Returns:
                bool: Whether the tcp connection could be established or not.
        """

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
    def check_connection(**kwargs):

        """
            **Method to evaluate the TCP trigger**

            This method evaulates the TCP trigger. Calls the
            desired methods to check tcp (normal or ssl) to a
            host.

            Args:
                kwargs (dict): dict containing host, port, ssl, timeout, attempts, threshold, check_type

            Returns:
                bool, error: status, error if any
        """
        host = kwargs.get("host")
        port = kwargs.get("port")
        ssl = kwargs.get("ssl")
        timeout = kwargs.get("timeout")
        attemps = kwargs.get("attempts")
        threshold = kwargs.get("threshold")
        check_type = kwargs.get("check_type")

        if ssl:
            check = TCPHandler.check_tcp_ssl
        else:
            check = TCPHandler.check_tcp

        count = 0

        for attempt in range(attemps):
            check_result = check(host=host, port=port, timeout=timeout)

            if check_result:
                if check_type == "tcp_connect":
                    count += 1
            else:
                if check_type == "tcp_fail":
                    count += 1

        if count >= threshold:
            return True, None

        return False, None

if __name__ == "__main__":
    print(TCPHandler.check_connection(host="www.media.net", port=1111, check_type="tcp_connect", attempts=2))
