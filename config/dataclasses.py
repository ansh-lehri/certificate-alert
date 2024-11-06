import ssl

from dataclasses import dataclass, field


class Attributes:
    """
    Class which focus on putting different checks on parameters of different dataclasses created
    """

    def check_attribute_datatype(self, Dataclass: dataclass):
        """
        Check if values assigned to fields of a dataclass are of defined data type.

        :param Dataclass: dataclass object
        :type Dataclass: dataclass

        Raises:
            ValueError: mentions the foeld which violates datatype of its respective dataclass.
        """
        for field_name, field_def in Dataclass.__dataclass_fields__.items():
            if type(getattr(Dataclass,field_name)) != field_def.type:
                raise ValueError(f"Attribute '{field_name}' of '{Dataclass.__class__.__name__}' should be of type {field_def.type}")



@dataclass
class Certificate:

    """
    Stores data regarding the process of fetching ssl certificate.
    """
    certificate_fetched: bool
    hostname: str
    error: str
    certificate_byte: bytes
    certificate_pem: str = field(default="")

    def __post_init__(self):
        Attributes().check_attribute_datatype(self)


@dataclass
class CertificateDetails:

    """
    Stores properties of a ssl certificate.
    """
    hostname: str
    expiry_date: str
    common_name: str
    organization_name: str
    expired: bool = field(default=False)
    
    def __post_init__(self):
        Attributes().check_attribute_datatype(self)


@dataclass
class HTTPSPortSocketConnection:

    """
    Stores data regarding the process of checking https port connection.
    """
    connection_established: bool
    hostname: str
    error: str
    socket_connection: ssl.socket

    def __post_init__(self):
        Attributes().check_attribute_datatype(self)


@dataclass
class TLSHandshake:

    """
    Stores data regarding the process of doing TLS Handshake.
    """
    handshake_successful: bool
    hostname: str
    error: str
    tls_socket: ssl.SSLSocket  # wrong datattype. will have to change
    
    def __post_init__(self):
        Attributes().check_attribute_datatype(self)

