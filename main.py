from config.constants import Constants
from config.logger import logger
from utils.dataclass_unwrap import DEFAULT_PORT_ERROR, EXPIRING_CERTIFICATES, TLS_PEERCERT_ERROR
from utils.notifier import SlackNotification
from utils.socket_utils import SocketUtils, SSLSocket
from utils.ssl_certificate import CertificateProperties,ConvertSSlCertificate,CertificateValidations


def check_ssl_expiry(hostname_ports):

    https_connection_objects = []
    tls_handshake_objects = []
    cert_detail_objects = []
    ssl_certificate_objects = []

    for hostname_port in hostname_ports:
        https_connection_object = SocketUtils().check_socket_connection_on_port(
            hostname = hostname_port.get("hostname"),
            port = hostname_port.get("port",Constants.DEFAULT_HTTPS_PORT)
        )
        
        https_connection_objects.append(https_connection_object)

        if getattr(https_connection_object,'connection_established'):
            tls_handshake_object = SocketUtils().check_tls(https_connection_object)
            tls_handshake_objects.append(tls_handshake_object)

            if getattr(tls_handshake_object,'handshake_successful'):
                ssl_certificate_object = SSLSocket().get_ssl_certificate(tls_handshake_object)
                ssl_certificate_objects.append(ssl_certificate_object)

                if getattr(ssl_certificate_object, 'certificate_fetched'):
                    pem_cert_object = ConvertSSlCertificate(ssl_certificate_object).der_to_pem()
                    cert_detail_object = CertificateProperties(pem_cert_object).get_properties()
                    cert_detail_object = CertificateValidations(cert_detail_object).check_expiry()
                    cert_detail_objects.append(cert_detail_object)

    return https_connection_objects, tls_handshake_objects, ssl_certificate_objects, cert_detail_objects


def unwrap_cert_objects(https_connection_objects, tls_handshake_objects, ssl_certificate_objects, cert_detail_objects):

    default_port_error = DEFAULT_PORT_ERROR().get_port_error_hostnames(https_connection_objects)
    tls_or_peercert_issue = TLS_PEERCERT_ERROR().get_tls_or_peercert_error_hostnames(tls_handshake_objects, ssl_certificate_objects)
    expiring_certificates = EXPIRING_CERTIFICATES().get_expiring_certificates(cert_detail_objects)

    return default_port_error, tls_or_peercert_issue, expiring_certificates


if __name__ == "__main__":
    https_connection_objects, tls_handshake_objects, ssl_certificate_objects, cert_detail_objects = check_ssl_expiry(
        [
            {
                'hostname':"google.com",
                'port':443
            },
            {
                'hostname':"meta.com",
                'port':443
            },
            {
                'hostname':"googles.com",
                'port':443
            }
        ]
    )
    default_port_error, tls_or_peercert_issue, expiring_certificates = unwrap_cert_objects(
        https_connection_objects, 
        tls_handshake_objects, 
        ssl_certificate_objects, 
        cert_detail_objects
    )


    SlackNotification().send_notification(expiring_certificates, default_port_error, tls_or_peercert_issue)