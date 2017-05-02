from abc import ABCMeta, abstractmethod
from typing import Dict


class CertInterface(metaclass=ABCMeta):
    """
    Parser interface for Android CERT.RSA/DSA certificate file.
    """

    @staticmethod
    @abstractmethod
    def looks_like_a_cert(filename: str) -> bool:
        """
        Check whether a given file looks like a CERT.RSA/DSA certificate file.

        :param filename: The name of the file to be checked.
        :return: True if the file looks like a CERT.RSA/DSA certificate file, False otherwise.
        """
        pass

    @abstractmethod
    def dump(self) -> Dict:
        """
        Dump the Cert object into a Dictionary.

        :return: A Dictionary representing the Cert object.
        """
        pass

    @abstractmethod
    def get_serial_number(self) -> str:
        """
        Retrieve the serial number of the certificate.

        :return: The certificate serial number.
        """
        pass

    ##
    # Retrieve the validity of the certificate.
    #
    # @return The certificate validity as a dictionary (i.e. {"from": "...", "until": "..."}).
    #
    @abstractmethod
    def get_validity(self) -> Dict:
        pass

    @abstractmethod
    def get_fingerprint_md5(self) -> str:
        """
        Retrieve the certificate fingerprint MD5 checksum.

        :return: The certificate fingerprint MD5 checksum.
        """
        pass

    @abstractmethod
    def get_fingerprint_sha1(self) -> str:
        """
        Retrieve the certificate fingerprint SHA-1 checksum.

        :return: The certificate fingerprint SHA-1 checksum.
        """
        pass

    @abstractmethod
    def get_fingerprint_sha256(self) -> str:
        """
        Retrieve the certificate fingerprint SHA-256 checksum.

        :return: The certificate fingerprint SHA-256 checksum.
        """
        pass

    @abstractmethod
    def get_fingerprint_signature(self) -> str:
        """
        Retrieve the certificate fingerprint signature algorithm name.

        :return: The certificate fingerprint signature algorithm name.
        """
        pass

    @abstractmethod
    def get_fingerprint_version(self) -> str:
        """
        Retrieve the certificate fingerprint version.

        :return: The certificate fingerprint version.
        """
        pass

    @abstractmethod
    def get_owner(self) -> Dict:
        """
        Retrieve the certificate owner.

        :return: The certificate owner as a Dictionary (i.e. {"name": "...", "email": "...", "country": "..."}).
        """
        pass

    @abstractmethod
    def get_issuer(self) -> Dict:
        """
        Retrieve the certificate issuer.

        :return: The certificate issuer as a dictionary (i.e. {"name": "...", "email": "...", "country": "..."}).
        """
        pass
