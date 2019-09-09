from datetime import datetime
from dateutil.tz import tzutc
from fnmatch import fnmatch
import re
import subprocess
from typing import Dict
import tzlocal

from ninjadroid.parsers.cert_interface import CertInterface
from ninjadroid.parsers.file import File
from ninjadroid.errors.cert_parsing_error import CertParsingError


class Cert(File, CertInterface):
    """
    Parser implementation for Android CERT.RSA/DSA certificate file.
    """

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
    __LABEL_FINGERPRINT_SIGNATURE = r"\t?\s?Signature algorithm name: "
    __LABEL_FINGERPRINT_VERSION = r"\t?\s?Version: "
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

    def __init__(self, filepath: str, filename: str = ""):
        super(Cert, self).__init__(filepath, filename)

        self._raw = self._extract_decoded_cert_file()
        self._serial_number = self._extract_string_pattern(self._raw, "^" + Cert.__LABEL_SERIAL_NUMBER + "(.*)$")
        self._extract_and_set_validity()
        self._extract_and_set_fingerprint()
        self._extract_and_set_owner()
        self._extract_and_set_issuer()

    def _extract_decoded_cert_file(self) -> str:
        """
        Retrieve decoded (PKCS7) certificate file, using keytool utility.

        :return: The raw decoded file.
        :raise CertParsingError: If there is a keytool error.
        """
        command = "keytool -printcert -file " + self.get_file_path()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        raw = process.communicate()[0].decode("utf-8")
        if re.search("^keytool error", raw, re.IGNORECASE):
            raise CertParsingError
        return raw

    def _extract_and_set_validity(self):
        """
        Extract the APK certificate validity.
        """
        self._validity = {"from": "", "until": ""}

        cert_validity_pattern = "^" + Cert.__LABEL_VALIDITY["label"] + "(.*)$"
        validity = self._extract_string_pattern(self._raw, cert_validity_pattern)
        if validity:
            cert_validity_from_pattern = "^" + Cert.__LABEL_VALIDITY["from"] + "(.*)" + Cert.__LABEL_VALIDITY["until"]
            self._validity["from"] = self._extract_string_pattern(validity, cert_validity_from_pattern)
            cert_validity_until_pattern = Cert.__LABEL_VALIDITY["until"] + "(.*)$"
            self._validity["until"] = self._extract_string_pattern(validity, cert_validity_until_pattern)

            tz = tzlocal.get_localzone()

            try:
                dt_from = datetime.strptime(self._validity["from"], "%a %b %d %H:%M:%S %Z %Y")
                local_dt_from = tz.localize(dt_from)
                utc_dt_from = local_dt_from.astimezone(tzutc())

                dt_until = datetime.strptime(self._validity["until"], "%a %b %d %H:%M:%S %Z %Y")
                local_dt_until = tz.localize(dt_until)
                utc_dt_until = local_dt_until.astimezone(tzutc())

            except ValueError:
                pass
            else:
                self._validity["from"] = utc_dt_from.strftime("%Y-%m-%d %H:%M:%SZ")
                self._validity["until"] = utc_dt_until.strftime("%Y-%m-%d %H:%M:%SZ")

    def _extract_and_set_fingerprint(self):
        """
        Extract APK certificate fingerprint data, such as MD5, SHA-1, SHA-256, signature and version.
        """
        self._fingerprint_md5 = self._extract_fingerprint_info(Cert.__LABEL_FINGERPRINT_MD5)
        self._fingerprint_sha1 = self._extract_fingerprint_info(Cert.__LABEL_FINGERPRINT_SHA1)
        self._fingerprint_sha256 = self._extract_fingerprint_info(Cert.__LABEL_FINGERPRINT_SHA256)
        self._fingerprint_signature = self._extract_fingerprint_info(Cert.__LABEL_FINGERPRINT_SIGNATURE)
        self._fingerprint_version = self._extract_fingerprint_info(Cert.__LABEL_FINGERPRINT_VERSION)

    def _extract_fingerprint_info(self, info: str) -> str:
        """
        Extract a given APK certificate fingerprint information (e.g. MD5, SHA-1, SHA-256, signature and version).

        :param info: The information to be extracted (e.g. Cert.__LABEL_FINGERPRINT_MD5, ...).
        :return: The extracted fingerprint information.
        """
        cert_fingerprint_pattern = "^" + info + "(.*)$"
        return self._extract_string_pattern(self._raw, cert_fingerprint_pattern)

    def _extract_and_set_owner(self):
        """
        Extract the APK certificate owner details (e.g. name, email, ...).
        """
        self._owner = {}  # type: Dict[str, str]

        cert_owner_pattern = "^" + Cert.__LABEL_OWNER["label"] + "(.*)$"
        owner = self._extract_string_pattern(self._raw, cert_owner_pattern)
        if owner:
            owner = owner.replace(", ", "\n")
            for key in Cert.__LABEL_OWNER:
                cert_owner_key_pattern = "^" + Cert.__LABEL_OWNER[key] + "(.*)"
                self._owner[key] = self._extract_string_pattern(owner, cert_owner_key_pattern)

    def _extract_and_set_issuer(self):
        """
        Extract the APK certificate issuer details (e.g. name, email, ...).
        """
        self._issuer = {}  # type: Dict[str, str]
        cert_issuer_pattern = "^" + Cert.__LABEL_ISSUER["label"] + "(.*)$"
        issuer = self._extract_string_pattern(self._raw, cert_issuer_pattern)
        if issuer:
            issuer = issuer.replace(", ", "\n")
            for key in Cert.__LABEL_ISSUER:
                cert_issuer_key_pattern = "^" + Cert.__LABEL_ISSUER[key] + "(.*)"
                self._issuer[key] = self._extract_string_pattern(issuer, cert_issuer_key_pattern)

    @staticmethod
    def _extract_string_pattern(string: str, pattern: str) -> str:
        """
        Extract the value of a given pattern from a given string.

        :param string: The string to be searched.
        :param pattern: The pattern to extract.
        :return: The extracted pattern if any is found, an empty string otherwise.
        """
        match = re.search(pattern, string, re.MULTILINE | re.IGNORECASE)
        if match and match.group(1):
            return match.group(1).strip()
        else:
            return ""

    @staticmethod
    def looks_like_a_cert(filename: str) -> bool:
        return filename == Cert.__FILE_NAME_CERT_RSA or \
            filename == Cert.__FILE_NAME_CERT_DSA or \
            fnmatch(filename, Cert.__FILE_NAME_CERT_ALT_REGEX)

    def dump(self) -> Dict:
        dump = super(Cert, self).dump()
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

    def get_serial_number(self) -> str:
        return self._serial_number

    def get_validity(self) -> str:
        return self._validity

    def get_fingerprint_md5(self) -> str:
        return self._fingerprint_md5

    def get_fingerprint_sha1(self) -> str:
        return self._fingerprint_sha1

    def get_fingerprint_sha256(self) -> str:
        return self._fingerprint_sha256

    def get_fingerprint_signature(self) -> str:
        return self._fingerprint_signature

    def get_fingerprint_version(self) -> str:
        return self._fingerprint_version

    def get_owner(self) -> Dict:
        return self._owner

    def get_issuer(self) -> Dict:
        return self._issuer
