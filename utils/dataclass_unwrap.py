# contain classes to unwrap dataclass objects into forms needed.

from collections import defaultdict

class DEFAULT_PORT_ERROR:

    def __init__(self):
        pass

    def get_port_error_hostnames(self, https_connection_objects):

        """
        Open https_connection_objects to fetch hostname and error occured if any while checking default https port.

        :param https_connection_objects: Objects containing information regarding result of port check.
        :type https_connection_objects: dataclass

        :return: collection of hostnames and error occured while checking default https port.
        :rtype: defaultdict(list)
        """
        port_not_deafult_https = defaultdict(list)

        for https_connection_object in https_connection_objects:
            if https_connection_object.connection_established == False:
                port_not_deafult_https['Hostname'].append(https_connection_object.hostname)
                port_not_deafult_https['Error'].append(https_connection_object.error)

        return port_not_deafult_https


class EXPIRING_CERTIFICATES:

    def __init__(self):
        pass

    def get_expiring_certificates(self, cert_detail_objects):

        """
        Open cert_detail_objects to fetch deatils of expiring certificates.

        :param cert_detail_objects: Objects containing certificate properties.
        :type cert_detail_objects: dataclass

        :return: collection of hostnames and other suitable information, certificate of which is about to expire.
        :rtype: defaultdict(list)
        """
        expiring_certificates = defaultdict(list)

        for cert_detail_objects in cert_detail_objects:
            if cert_detail_objects.expired == True:
                expiring_certificates['Hostname'].append(cert_detail_objects.hostname)
                expiring_certificates['Expiry Date'].append(cert_detail_objects.expiry_date)
                expiring_certificates['Common Name'].append(cert_detail_objects.common_name)
                expiring_certificates['organization Name'].append(cert_detail_objects.organization_name)

        return expiring_certificates


class TLS_PEERCERT_ERROR:

    def __init__(self):
        pass

    def get_tls_or_peercert_error_hostnames(self, tls_handshake_objects, ssl_certificate_objects):

        """
        Open tls_handshake_objects and ssl_certificate_objects to fetch hostname and error occured if any while 
        checking TLS Handshake or fetching ssl certificate respectively.

        :param tls_handshake_objects: Objects containing information regarding result of tls_handshake.
        :type tls_handshake_objects: dataclass

        :param ssl_certificate_objects: Objects containing outcome of the attempt to fetch a host's ssl certificate.
        :type ssl_certificate_objects: dataclass

        :return: collection of hostnames and error occured while doing TLS Handshake or fetching certificate.
        :rtype: defaultdict(list)
        """

        tls_or_peercert_issue = defaultdict(list)

        for tls_handshake_object in tls_handshake_objects:
            if tls_handshake_object.handshake_successful == False:
                tls_or_peercert_issue['Hostname'].append(tls_handshake_object.hostname)
                tls_or_peercert_issue['Error'].append(tls_handshake_object.error)

        for ssl_certificate_object in ssl_certificate_objects:
            if ssl_certificate_object.certificate_fetched == False:
                tls_or_peercert_issue['Hostname'].append(ssl_certificate_object.hostname)
                tls_or_peercert_issue['Error'].append(ssl_certificate_object.error)

        return tls_or_peercert_issue