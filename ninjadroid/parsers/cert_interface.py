from abc import ABCMeta, abstractmethod


class CERTInterface(metaclass=ABCMeta):
    """
    Parser interface for Android CERT.RSA/DSA certificate file.
    """

    @staticmethod
    @abstractmethod
    def looks_like_a_cert(filename):
        """
        Check whether a given file looks like a CERT.RSA/DSA certificate file.

        :param filename: The name of the file to be checked.
        :return: True if the file looks like a CERT.RSA/DSA certificate file, False otherwise.
        """
        pass

    @abstractmethod
    def dump(self):
        """
        Dump the CERT object into a Dictionary.

        :return: A Dictionary representing the CERT object.
        """
        pass

    @abstractmethod
    def get_serial_number(self):
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
    def get_validity(self):
        pass

    @abstractmethod
    def get_fingerprint_md5(self):
        """
        Retrieve the certificate fingerprint MD5 checksum.

        :return: The certificate fingerprint MD5 checksum.
        """
        pass

    @abstractmethod
    def get_fingerprint_sha1(self):
        """
        Retrieve the certificate fingerprint SHA-1 checksum.

        :return: The certificate fingerprint SHA-1 checksum.
        """
        pass

    @abstractmethod
    def get_fingerprint_sha256(self):
        """
        Retrieve the certificate fingerprint SHA-256 checksum.

        :return: The certificate fingerprint SHA-256 checksum.
        """
        pass

    @abstractmethod
    def get_fingerprint_signature(self):
        """
        Retrieve the certificate fingerprint signature algorithm name.

        :return: The certificate fingerprint signature algorithm name.
        """
        pass

    @abstractmethod
    def get_fingerprint_version(self):
        """
        Retrieve the certificate fingerprint version.

        :return: The certificate fingerprint version.
        """
        pass

    @abstractmethod
    def get_owner(self):
        """
        Retrieve the certificate owner.

        :return: The certificate owner as a Dictionary (i.e. {"name": "...", "email": "...", "country": "..."}).
        """
        pass

    @abstractmethod
    def get_issuer(self):
        """
        Retrieve the certificate issuer.

        :return: The certificate issuer as a dictionary (i.e. {"name": "...", "email": "...", "country": "..."}).
        """
        pass
