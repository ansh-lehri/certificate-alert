import socket
import ssl

from config.conf import config
from config.dataclasses import HTTPSPortSocketConnection, TLSHandshake, Certificate
from config.logger import logger

class SocketUtils:

    """
    Contains methods regarding default port checking and tls handshake.
    """

    def __init__(self):
        pass


    def check_socket_connection_on_port(self, hostname, port):
        
        """
        Checks if the hostname is running on DEFAULT_HTTPS_PORT

        :param hostname: Name of the subdomain present in cloudlfare.
        :type hostname: str
        :param port: Default HTTPS Port.
        :type port: int

        :return: Object containing information regarding result of port check. 
        :rtype: dataclass

        """
        socket_connection = ssl.socket()
        error = ""
        try:
            socket_connection = socket.create_connection((hostname, port),config.socket_connection_timeout_seconds)
            connection_established = True
        except Exception as e:
            error = f"Socket connection could not be established on default port {port}"
            connection_established = False

        print(hostname, "   ",port,"   ",connection_established)
        return HTTPSPortSocketConnection(connection_established, hostname, error, socket_connection)

    def check_tls(self, https_connection_object):
        
        """
        checks if TLS handshake is happeing successfully.

        :param https_connection_object: An object containing information regarding result of port check.
        :type https_connection_object: dataclass

        :returns: Object containing information regarding result of tls_handshake. 
        :rtype: dataclass

        """
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        tls_socket = context.wrap_socket(ssl.socket())
        error = ""
        hostname = getattr(https_connection_object,'hostname')

        try:
            tls_socket = context.wrap_socket(getattr(https_connection_object,'socket_connection'), server_hostname=hostname)
            handshake_successful = True
        except Exception as e:
            error = "%s%s%s" % (error,f"TLS handshake failed for {hostname} because ",str(e))
            handshake_successful = False

        print(hostname, "   ",handshake_successful)
        return TLSHandshake(handshake_successful,hostname,error,tls_socket)



class SSLSocket:

    """
    The class is concerned with ssl socket. Can conatin methods to perform different actions using ssl sockets.
    """

    def __init__(self):
        pass


    def get_ssl_certificate(self, tls_handshake_object):

        """
        Fetches ssl certificate using ssl socket connection established.

        :param tls_handshake_object: An object containing information regarding TLS handshake.
        :type tls_handshake_object: dataclass

        :return: Certificate object containing result of fetching ssl certificate.
        :rtype: dataclass
        """

        hostname = getattr(tls_handshake_object,'hostname')
        certificate = b''
        error = ""

        try:
            certificate = getattr(tls_handshake_object,'tls_socket').getpeercert(True)
            certificate_fetched = True
        except Exception as e:
            certificate_fetched = False
            error = "%s%s%s" % (error,f"Certificate for {hostname} could not be fetched because ",str(e))
        
        print(hostname, "     ", certificate,"     ",certificate_fetched)
        return Certificate(certificate_fetched,hostname,error,certificate)