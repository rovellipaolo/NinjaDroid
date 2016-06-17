from abc import ABCMeta, abstractmethod


##
# Parser interface for Android CERT.RSA/DSA certificate file.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#
class CERTParserInterface(object):
    __metaclass__ = ABCMeta

    ##
    # Check whether a given file looks like a CERT.RSA/DSA certificate file.
    #
    @staticmethod
    @abstractmethod
    def looks_like_a_cert(filename):
        pass

    ##
    # Dump the CERT object into a Dictionary.
    #
    # @return A Dictionary representing the CERT object.
    #
    @abstractmethod
    def dump(self):
        pass

    ##
    # Retrieve the serial number of the certificate.
    #
    # @return The certificate serial number.
    #
    @abstractmethod
    def get_serial_number(self):
        pass

    ##
    # Retrieve the validity of the certificate.
    #
    # @return The certificate validity as a dictionary (i.e. {"from": "...", "until": "..."}).
    #
    @abstractmethod
    def get_validity(self):
        pass

    ##
    # Retrieve the certificate fingerprint MD5 checksum.
    #
    # @return The certificate fingerprint MD5 checksum.
    #
    @abstractmethod
    def get_fingerprint_md5(self):
        pass

    ##
    # Retrieve the certificate fingerprint SHA-1 checksum.
    #
    # @return The certificate fingerprint SHA-1 checksum.
    #
    @abstractmethod
    def get_fingerprint_sha1(self):
        pass

    ##
    # Retrieve the certificate fingerprint SHA-256 checksum.
    #
    # @return The certificate fingerprint SHA-256 checksum.
    #
    @abstractmethod
    def get_fingerprint_sha256(self):
        pass

    ##
    # Retrieve the certificate fingerprint signature algorithm name.
    #
    # @return The certificate fingerprint signature algorithm name.
    #
    @abstractmethod
    def get_fingerprint_signature(self):
        pass

    ##
    # Retrieve the certificate fingerprint version.
    #
    # @return The certificate fingerprint version.
    #
    @abstractmethod
    def get_fingerprint_version(self):
        pass

    ##
    # Retrieve the certificate owner.
    #
    # @return The certificate owner as a Dictionary (i.e. {"name": "...", "email": "...", "country": "..."}).
    #
    @abstractmethod
    def get_owner(self):
        pass

    ##
    # Retrieve the certificate issuer.
    #
    # @return The certificate issuer as a dictionary (i.e. {"name": "...", "email": "...", "country": "..."}).
    #
    @abstractmethod
    def get_issuer(self):
        pass
