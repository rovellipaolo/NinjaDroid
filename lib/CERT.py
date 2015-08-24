##
# @file CERT.py
# @brief Parser for Android CERT.RSA/DSA certificate file.
# @version 1.5
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

from datetime import datetime
import re
import subprocess

from lib.File import File


##
# ErrorCERTParsing class.
#
class ErrorCERTParsing(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an Android CERT!"


##
# CERT class.
#
class CERT(File, object):
    __LABEL_SERIAL_NUMBER = "Serial number: "
    __LABEL_VALIDITY = {
        "label": "Valid ",
        "from": "from: ",
        "until": "until: ",
    }
    __LABEL_FINGERPRINT_MD5 = "\t MD5: "
    __LABEL_FINGERPRINT_SHA1 = "\t SHA1: "
    __LABEL_FINGERPRINT_SHA256 = "\t SHA256: "
    __LABEL_FINGERPRINT_SIGNATURE = "\t Signature algorithm name: "
    __LABEL_FINGERPRINT_VERSION = "\t Version: "
    __LABEL_OWNER = {
        "label": "Owner: ",
        "name": "CN=",
        "email": "EMAILADDRESS=",
        "unit": "OU=",
        "organization": "O=",
        "city": "L=",
        "state": "ST=",
        "country": "C=",
        "domain": "DC=",
    }
    __LABEL_ISSUER = {
        "label": "Issuer: ",
        "name": "CN=",
        "email": "EMAILADDRESS=",
        "unit": "OU=",
        "organization": "O=",
        "city": "L=",
        "state": "ST=",
        "country": "C=",
        "domain": "DC=",
    }

    ##
    # Class constructor.
    #
    # @param filepath  The CERT.RSA/DSA file path.
    # @param filename  the name of the CERT file.
    #
    def __init__(self, filepath, filename=""):
        super(CERT, self).__init__(filepath, filename)

        # Decode the CERT.RSA/DSA file (PKCS7):
        process = subprocess.Popen("keytool -printcert -file " + filepath, stdout=subprocess.PIPE, stderr=None, shell=True)
        self._raw = process.communicate()[0].decode("utf-8")

        if re.search("^keytool error", self._raw, re.IGNORECASE):
            raise ErrorCERTParsing

        self._serial_number = CERT._extract_string_pattern(self._raw, '^' + CERT.__LABEL_SERIAL_NUMBER + '(.*)$')

        # Extract the certificate validity
        self._validity = {"from": "", "until": ""}
        validity = CERT._extract_string_pattern(self._raw, '^' + CERT.__LABEL_VALIDITY['label'] + '(.*)$')
        if validity:
            self._validity['from'] = CERT._extract_string_pattern(validity, '^' + CERT.__LABEL_VALIDITY['from'] + '(.*)' + CERT.__LABEL_VALIDITY['until'])
            self._validity['until'] = CERT._extract_string_pattern(validity, CERT.__LABEL_VALIDITY['until'] + '(.*)$')

            try:
                dt_from = datetime.strptime(self._validity['from'], "%a %b %d %H:%M:%S %Z %Y")
                dt_until = datetime.strptime(self._validity['until'], "%a %b %d %H:%M:%S %Z %Y")
            except ValueError:
                pass
            else:
                self._validity['from'] = dt_from.strftime("%Y-%m-%d %H:%M:%S")
                self._validity['until'] = dt_until.strftime("%Y-%m-%d %H:%M:%S")

        # Extract certificate fingerprint:
        self._fingerprint_md5 = CERT._extract_string_pattern(self._raw, '^' + CERT.__LABEL_FINGERPRINT_MD5 + '(.*)$')
        self._fingerprint_sha1 = CERT._extract_string_pattern(self._raw, '^' + CERT.__LABEL_FINGERPRINT_SHA1 + '(.*)$')
        self._fingerprint_sha256 = CERT._extract_string_pattern(self._raw, '^' + CERT.__LABEL_FINGERPRINT_SHA256 + '(.*)$')
        self._fingerprint_signature = CERT._extract_string_pattern(self._raw, '^' + CERT.__LABEL_FINGERPRINT_SIGNATURE + '(.*)$')
        self._fingerprint_version = CERT._extract_string_pattern(self._raw, '^' + CERT.__LABEL_FINGERPRINT_VERSION + '(.*)$')

        # Extract owner details:
        self._owner = {}
        owner = CERT._extract_string_pattern(self._raw, '^' + CERT.__LABEL_OWNER['label'] + '(.*)$')
        if owner:
            owner = owner.replace(", ", "\n")
            for key in CERT.__LABEL_OWNER:
                self._owner[key] = CERT._extract_string_pattern(owner, '^' + CERT.__LABEL_OWNER[key] + '(.*)')

        # Extract issuer details:
        self._issuer = {}
        issuer = CERT._extract_string_pattern(self._raw, '^' + CERT.__LABEL_ISSUER['label'] + '(.*)$')
        if issuer:
            issuer = issuer.replace(", ", "\n")
            for key in CERT.__LABEL_ISSUER:
                self._issuer[key] = CERT._extract_string_pattern(issuer, '^' + CERT.__LABEL_ISSUER[key] + '(.*)')

    ##
    # Extract the value of a given pattern from a given string.
    #
    # @param string  The string to be searched.
    # @param pattern  The pattern to extract.
    # @return The extracted pattern if any is found, an empty string otherwise.
    #
    @staticmethod
    def _extract_string_pattern(string, pattern):
        match = re.search(pattern, string, re.MULTILINE | re.IGNORECASE)
        if match and match.group(1):
            return match.group(1).strip()
        else:
            return ""

    ##
    # Dump the CERT object.
    #
    # @return A Dictionary representing the CERT object.
    #
    def dump(self):
        dump = super(CERT, self).dump()
        dump["serial_number"] = self._serial_number
        dump["validity"] = self._validity
        dump["fingerprint"] = {}
        dump["fingerprint"]["md5"] = self._fingerprint_md5
        dump["fingerprint"]["sha1"] = self._fingerprint_sha1
        dump["fingerprint"]["sha256"] = self._fingerprint_sha256
        dump["fingerprint"]["signature"] = self._fingerprint_signature
        dump["fingerprint"]["version"] = self._fingerprint_version
        dump["owner"] = self._owner
        dump["issuer"] = self._issuer
        return dump

    ##
    # Retrieve the serial number of the certificate.
    #
    # @return the certificate serial number.
    #
    def get_serial_number(self):
        return self._serial_number

    ##
    # Retrieve the validity of the certificate.
    #
    # @return The certificate validity as a dictionary (i.e. {"from": "...", "until": "..."}).
    #
    def get_validity(self):
        return self._validity

    ##
    # Retrieve the certificate fingerprint MD5 checksum.
    #
    # @return The certificate fingerprint MD5 checksum.
    #
    def get_fingerprint_md5(self):
        return self._fingerprint_md5

    ##
    # Retrieve the certificate fingerprint SHA-1 checksum.
    #
    # @return The certificate fingerprint SHA-1 checksum.
    #
    def get_fingerprint_sha1(self):
        return self._fingerprint_sha1

    ##
    # Retrieve the certificate fingerprint SHA-256 checksum.
    #
    # @return The certificate fingerprint SHA-256 checksum.
    #
    def get_fingerprint_sha256(self):
        return self._fingerprint_sha256

    ##
    # Retrieve the certificate fingerprint signature algorithm name.
    #
    # @return The certificate fingerprint signature algorithm name.
    ##
    def get_fingerprint_signature(self):
        return self._fingerprint_signature

    ##
    # Retrieve the certificate fingerprint version.
    #
    # @return The certificate fingerprint version.
    ##
    def get_fingerprint_version(self):
        return self._fingerprint_version

    ##
    # Retrieve the certificate owner.
    #
    # @return The certificate owner as a dictionary (i.e. {"name": "...", "email": "...", "unit": "...", "organization": "...", "city": "...", "state": "...", "country": "...", "domain": "..."}).
    ##
    def get_owner(self):
        return self._owner

    ##
    # Retrieve the certificate issuer.
    #
    # @return The certificate issuer as a dictionary (i.e. {"name": "...", "email": "...", "unit": "...", "organization": "...", "city": "...", "state": "...", "country": "...", "domain": "..."}).
    ##
    def get_issuer(self):
        return self._issuer
