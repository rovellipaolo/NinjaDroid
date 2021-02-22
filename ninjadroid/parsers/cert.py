import re
from subprocess import PIPE, Popen
from datetime import datetime
from fnmatch import fnmatch
from typing import Dict
from dateutil.tz import tzutc
from tzlocal import get_localzone

from ninjadroid.parsers.file import File
from ninjadroid.errors.cert_parsing_error import CertParsingError


# pylint: disable=too-many-instance-attributes
class Cert(File):
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
    __LABEL_OWNER = "Owner: "
    __LABEL_OWNER_FIELDS = {
        "name": "CN=",
        "email": "EMAILADDRESS=",
        "unit": "OU=",
        "organization": "O=",
        "city": "L=",
        "state": "ST=",
        "country": "C=",
        "domain": "DC=",
    }
    __LABEL_ISSUER = "Issuer: "
    __LABEL_ISSUER_FIELDS = {
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
        super().__init__(filepath, filename)
        self._raw = self._extract_cert_info(self.get_file_path())
        self._serial_number = self._extract_string_pattern(
            self._raw,
            pattern="^" + Cert.__LABEL_SERIAL_NUMBER + "(.*)$"
        )
        self._extract_and_set_fingerprint()
        self._validity = self._extract_validity(self._raw)
        self._owner = self._extract_owner(self._raw)
        self._issuer = self._extract_issuer(self._raw)

    def _extract_and_set_fingerprint(self):
        self._fingerprint_md5 = self._extract_string_pattern(
            self._raw,
            pattern="^" + Cert.__LABEL_FINGERPRINT_MD5 + "(.*)$"
        )
        self._fingerprint_sha1 = self._extract_string_pattern(
            self._raw,
            pattern="^" + Cert.__LABEL_FINGERPRINT_SHA1 + "(.*)$"
        )
        self._fingerprint_sha256 = self._extract_string_pattern(
            self._raw,
            pattern="^" + Cert.__LABEL_FINGERPRINT_SHA256 + "(.*)$"
        )
        self._fingerprint_signature = self._extract_string_pattern(
            self._raw,
            pattern="^" + Cert.__LABEL_FINGERPRINT_SIGNATURE + "(.*)$"
        )
        self._fingerprint_version = self._extract_string_pattern(
            self._raw,
            pattern="^" + Cert.__LABEL_FINGERPRINT_VERSION + "(.*)$"
        )

    @staticmethod
    def _extract_cert_info(file_path) -> str:
        """
        Retrieve decoded (PKCS7) certificate file, using keytool utility.
        """
        command = "keytool -printcert -file " + file_path
        process = Popen(command, stdout=PIPE, stderr=None, shell=True)
        raw = process.communicate()[0].decode("utf-8")
        if re.search("^keytool error", raw, re.IGNORECASE):
            raise CertParsingError
        return raw

    @staticmethod
    def _extract_validity(raw: str) -> Dict:
        validity = {
            "from": "",
            "until": ""
        }

        validity_pattern = Cert._extract_string_pattern(raw, pattern="^" + Cert.__LABEL_VALIDITY["label"] + "(.*)$")
        if validity_pattern:
            validity["from"] = Cert._extract_string_pattern(
                validity_pattern,
                pattern="^" + Cert.__LABEL_VALIDITY["from"] + "(.*)" + Cert.__LABEL_VALIDITY["until"]
            )
            validity["until"] = Cert._extract_string_pattern(
                validity_pattern,
                pattern=Cert.__LABEL_VALIDITY["until"] + "(.*)$"
            )

            try:
                time_zone = get_localzone()

                local_dt_from = time_zone.localize(
                    dt=datetime.strptime(validity["from"], "%a %b %d %H:%M:%S %Z %Y")
                )
                utc_dt_from = local_dt_from.astimezone(tzutc())

                local_dt_until = time_zone.localize(
                    dt=datetime.strptime(validity["until"], "%a %b %d %H:%M:%S %Z %Y")
                )
                utc_dt_until = local_dt_until.astimezone(tzutc())
            except ValueError:
                pass
            else:
                validity["from"] = utc_dt_from.strftime("%Y-%m-%d %H:%M:%SZ")
                validity["until"] = utc_dt_until.strftime("%Y-%m-%d %H:%M:%SZ")

        return validity

    @staticmethod
    def _extract_owner(raw: str) -> Dict:
        owner = {}  # type: Dict[str, str]
        owner_pattern = Cert._extract_string_pattern(raw, pattern="^" + Cert.__LABEL_OWNER + "(.*)$")
        if owner_pattern:
            owner_pattern = owner_pattern.replace(", ", "\n")
            for key in Cert.__LABEL_OWNER_FIELDS:
                owner[key] = Cert._extract_string_pattern(
                    owner_pattern,
                    pattern="^" + Cert.__LABEL_OWNER_FIELDS[key] + "(.*)"
                )
        return owner

    @staticmethod
    def _extract_issuer(raw: str) -> Dict:
        issuer = {}  # type: Dict[str, str]
        issuer_pattern = Cert._extract_string_pattern(raw, pattern="^" + Cert.__LABEL_ISSUER + "(.*)$")
        if issuer_pattern:
            issuer_pattern = issuer_pattern.replace(", ", "\n")
            for key in Cert.__LABEL_ISSUER_FIELDS:
                issuer[key] = Cert._extract_string_pattern(
                    issuer_pattern,
                    pattern="^" + Cert.__LABEL_ISSUER_FIELDS[key] + "(.*)"
                )
        return issuer

    @staticmethod
    def _extract_string_pattern(string: str, pattern: str) -> str:
        """
        Extract the value of a given pattern from a given string.
        """
        match = re.search(pattern, string, re.MULTILINE | re.IGNORECASE)
        if match and match.group(1):
            return match.group(1).strip()
        return ""

    @staticmethod
    def looks_like_a_cert(filename: str) -> bool:
        return filename == Cert.__FILE_NAME_CERT_RSA or \
            filename == Cert.__FILE_NAME_CERT_DSA or \
            fnmatch(filename, Cert.__FILE_NAME_CERT_ALT_REGEX)

    def dump(self) -> Dict:
        dump = super().dump()
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
