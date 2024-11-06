import OpenSSL
import ssl

from config.conf import config
from config.constants import Constants
from config.dataclasses import CertificateDetails
from datetime import datetime
from dateutil.parser import parse


class ConvertSSlCertificate:

    """
    Class focusing on converting ssl certificate format.
    """

    def __init__(self, certificate): 

        """
        :param certificate: Certificate object.
        :type certificate: dataclass
        """      
        self.certificate = certificate


    def der_to_pem(self):
        """
        Converts certificate from bytes to PEM format.

        :return: Certificate object with additional information on PEM format of certificate.
        :rtype: dataclass

        """
        self.certificate.certificate_pem = ssl.DER_cert_to_PEM_cert(self.certificate.certificate_byte)
        print()
        print(self.certificate)
        return self.certificate


class CertificateSubjectInfo:

    """
    Class focused on retrieving different parameters present in subject section of a ssl certificate.
    """
    def __init__(self,certificate):

        """
        Fetches X509 object of certificate using its PEM format and OpenSSl and then retrieves subject information in 
        certificate.

        :param certificate: Certificate object.
        :type certificate: dataclass
        """
        try:
            self.x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, getattr(certificate,'certificate_pem'))
        except Exception as e:
            raise ValueError("SSL certificate not in proper formate. It should be in PEM format.")

        self.x509subjectinfo = self.x509.get_subject()


    def get_common_name(self):

        """
        Fetches common name of certificate.
       
        :return: common name
        :rtype: str
        """
        return self.x509subjectinfo.commonName

    def get_organization_name(self):

        """
        Fetches organization name of certificate.
       
        :return: organization name
        :rtype: str
        """
        return str(self.x509subjectinfo.organizationName)


class CertificateDates:

    """
    Class focused on retrieving dates present on a ssl certificate.
    """

    def __init__(self,certificate):

        """
        Fetches X509 object of certificate using its PEM format and OpenSSl.

        :param certificate: Certificate object.
        :type certificate: dataclass
        """

        try:
            self.x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, getattr(certificate,'certificate_pem'))
        except Exception as e:
            raise ValueError("SSL certificate not in proper formate. It should be in PEM format.")


    def get_expiry_date(self):

        """
        Fetches expiry date of a certificate.

        :return: expiry date.
        :rtype: str
        """

        x509dateinfo = self.x509.get_notAfter()
        exp_day = x509dateinfo[6:8].decode("utf-8")
        exp_month = x509dateinfo[4:6].decode("utf-8")
        exp_year = x509dateinfo[:4].decode("utf-8")
        expiry_date = str(exp_day) + "-" + str(exp_month) + "-" + str(exp_year)

        return expiry_date


class CertificateProperties(CertificateDates, CertificateSubjectInfo):

    """
    Class which inherits from mentioned classes and can inherit from more base classes which deals with Certificate 
    proeprties to get all details at one interface.
    """

    def __init__(self,certificate):

        """
        Initiates init method of base classes and retrieves hostname from certificate object.

        :param certificate: Certificate object.
        :type certificate: dataclass
        """
        CertificateDates.__init__(self,certificate)
        CertificateSubjectInfo.__init__(self,certificate)
        self.hostname = getattr(certificate,'hostname')


    def get_properties(self):

        """
        Method calls different methods of base classes. Methods called depends on information needed from different Classes.
        
        :return: CertificateDetails object which contain certificate properties.
        :rtype: dataclass
        """

        expiry_date = self.get_expiry_date()
        common_name = self.get_common_name()
        organization_name = self.get_organization_name()

        return CertificateDetails(hostname=self.hostname,expiry_date=expiry_date, common_name=common_name, organization_name=organization_name)


class CertificateValidations:

    """
    Class to deal with different validations which can be put on certificate and its properties.
    """
    today_date = datetime.now(Constants.IST).date()

    def __init__(self, certificate_details):
        """
        :param certificate_details: CertificateDetails object.
        :type certificate_details: dataclass
        """     
        self.certificate_details = certificate_details

    def check_expiry(self):
        
        """
        checks if the expiry of a hostname's certificate is about to breach threshold.

        :return: CertificateDetails object with additional information on if certificate is to expire.
        :rtype: dataclass
        """
        expiry_date = parse(getattr(self.certificate_details,'expiry_date')).date()
        if (expiry_date - CertificateValidations.today_date).days < config.warn_if_days_less_than:
            self.certificate_details.expired = True

        return self.certificate_details

        
