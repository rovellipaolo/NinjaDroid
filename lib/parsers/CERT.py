##
# Parser implementation for Android CERT.RSA/DSA certificate file.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

from datetime import datetime
from fnmatch import fnmatch
import re
import subprocess

from lib.parsers.CERTParserInterface import CERTParserInterface
from lib.parsers.File import File
from lib.errors.CERTParsingError import CERTParsingError


class CERT(File, CERTParserInterface):
    __FILE_NAME_CERT_RSA = "META-INF/CERT.RSA"
    __FILE_NAME_CERT_DSA = "META-INF/CERT.DSA"
    __FILE_NAME_CERT_ALT_REGEX = "META-INF/*.RSA"

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
    # @param filepath  The path of the CERT.RSA/DSA.
    # @param filename  The name of the CERT file.
    # @throw CERTParsingError  If there is a keytool error.
    #
    def __init__(self, filepath, filename=""):
        super(CERT, self).__init__(filepath, filename)

        self._raw = self._extract_decoded_cert_file()
        self._serial_number = self._extract_string_pattern(self._raw, '^' + CERT.__LABEL_SERIAL_NUMBER + '(.*)$')
        self._extract_and_set_validity()
        self._extract_and_set_fingerprint()
        self._extract_and_set_owner()
        self._extract_and_set_issuer()

    ##
    # Retrieve decoded (PKCS7) certificate file, using keytool utility.
    #
    # @return The raw decoded file.
    # @throw CERTParsingError  If there is a keytool error.
    #
    def _extract_decoded_cert_file(self):
        process = subprocess.Popen("keytool -printcert -file " + self.get_file_path(), stdout=subprocess.PIPE, stderr=None, shell=True)
        raw = process.communicate()[0].decode("utf-8")
        if re.search("^keytool error", raw, re.IGNORECASE):
            raise CERTParsingError
        return raw

    ##
    # Extract the APK certificate validity.
    #
    def _extract_and_set_validity(self):
        self._validity = {"from": "", "until": ""}
        validity = self._extract_string_pattern(self._raw, '^' + CERT.__LABEL_VALIDITY['label'] + '(.*)$')
        if validity:
            self._validity['from'] = self._extract_string_pattern(validity, '^' + CERT.__LABEL_VALIDITY['from'] + '(.*)' + CERT.__LABEL_VALIDITY['until'])
            self._validity['until'] = self._extract_string_pattern(validity, CERT.__LABEL_VALIDITY['until'] + '(.*)$')

            try:
                dt_from = datetime.strptime(self._validity['from'], "%a %b %d %H:%M:%S %Z %Y")
                dt_until = datetime.strptime(self._validity['until'], "%a %b %d %H:%M:%S %Z %Y")
            except ValueError:
                pass
            else:
                self._validity['from'] = dt_from.strftime("%Y-%m-%d %H:%M:%S")
                self._validity['until'] = dt_until.strftime("%Y-%m-%d %H:%M:%S")

    ##
    # Extract APK certificate fingerprint data, such as MD5, SHA-1, SHA-256, signature and version.
    #
    def _extract_and_set_fingerprint(self):
        self._fingerprint_md5 = self._extract_fingerprint_info(CERT.__LABEL_FINGERPRINT_MD5)
        self._fingerprint_sha1 = self._extract_fingerprint_info(CERT.__LABEL_FINGERPRINT_SHA1)
        self._fingerprint_sha256 = self._extract_fingerprint_info(CERT.__LABEL_FINGERPRINT_SHA256)
        self._fingerprint_signature = self._extract_fingerprint_info(CERT.__LABEL_FINGERPRINT_SIGNATURE)
        self._fingerprint_version = self._extract_fingerprint_info(CERT.__LABEL_FINGERPRINT_VERSION)

    ##
    # Extract a given APK certificate fingerprint information (e.g. MD5, SHA-1, SHA-256, signature and version).
    #
    # @param info  The information to be extracted (e.g. CERT.__LABEL_FINGERPRINT_MD5, ...).
    # @return The extracted fingerprint information.
    #
    def _extract_fingerprint_info(self, info):
        return self._extract_string_pattern(self._raw, '^' + info + '(.*)$')

    ##
    # Extract the APK certificate owner details (e.g. name, email, ...).
    #
    def _extract_and_set_owner(self):
        self._owner = {}
        owner = self._extract_string_pattern(self._raw, '^' + CERT.__LABEL_OWNER['label'] + '(.*)$')
        if owner:
            owner = owner.replace(", ", "\n")
            for key in CERT.__LABEL_OWNER:
                self._owner[key] = self._extract_string_pattern(owner, '^' + CERT.__LABEL_OWNER[key] + '(.*)')

    ##
    # Extract the APK certificate issuer details (e.g. name, email, ...).
    #
    def _extract_and_set_issuer(self):
        self._issuer = {}
        issuer = self._extract_string_pattern(self._raw, '^' + CERT.__LABEL_ISSUER['label'] + '(.*)$')
        if issuer:
            issuer = issuer.replace(", ", "\n")
            for key in CERT.__LABEL_ISSUER:
                self._issuer[key] = self._extract_string_pattern(issuer, '^' + CERT.__LABEL_ISSUER[key] + '(.*)')

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

    @staticmethod
    def looks_like_a_cert(filename):
        return filename == CERT.__FILE_NAME_CERT_RSA or \
               filename == CERT.__FILE_NAME_CERT_DSA or \
               fnmatch(filename, CERT.__FILE_NAME_CERT_ALT_REGEX)

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

    def get_serial_number(self):
        return self._serial_number

    def get_validity(self):
        return self._validity

    def get_fingerprint_md5(self):
        return self._fingerprint_md5

    def get_fingerprint_sha1(self):
        return self._fingerprint_sha1

    def get_fingerprint_sha256(self):
        return self._fingerprint_sha256

    def get_fingerprint_signature(self):
        return self._fingerprint_signature

    def get_fingerprint_version(self):
        return self._fingerprint_version

    def get_owner(self):
        return self._owner

    def get_issuer(self):
        return self._issuer
