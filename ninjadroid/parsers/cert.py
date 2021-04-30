from logging import getLogger, Logger
import re
from subprocess import PIPE, Popen
from datetime import datetime
from fnmatch import fnmatch
from typing import Any, Dict
from dateutil.tz import tzutc
from tzlocal import get_localzone

from ninjadroid.parsers.file import File, FileParser, FileParsingError


default_logger = getLogger(__name__)


class CertValidity:
    """
   CERT validity information.
   """

    def __init__(self, valid_from: str, valid_to: str):
        self.__from = valid_from
        self.__to = valid_to

    def __eq__(self, other: Any):
        return isinstance(other, CertValidity) and \
               self.__from == other.get_from() and \
               self.__to == other.get_to()

    def get_from(self) -> str:
        return self.__from

    def get_to(self) -> str:
        return self.__to

    def as_dict(self) -> Dict:
        return {
            "from": self.__from,
            "until": self.__to
        }


class CertFingerprint:
    """
   CERT fingerprint information.
   """

    # pylint: disable=too-many-arguments
    def __init__(self, md5: str, sha1: str, sha256: str, signature: str, version: str):
        self.__md5 = md5
        self.__sha1 = sha1
        self.__sha256 = sha256
        self.__signature = signature
        self.__version = version

    def __eq__(self, other: Any):
        return isinstance(other, CertFingerprint) and \
               self.__md5 == other.get_md5() and \
               self.__sha1 == other.get_sha1() and \
               self.__sha256 == other.get_sha256() and \
               self.__signature == other.get_signature() and \
               self.__version == other.get_version()

    def get_md5(self) -> str:
        return self.__md5

    def get_sha1(self) -> str:
        return self.__sha1

    def get_sha256(self) -> str:
        return self.__sha256

    def get_signature(self) -> str:
        return self.__signature

    def get_version(self) -> str:
        return self.__version

    def as_dict(self) -> Dict:
        return {
            "md5": self.__md5,
            "sha1": self.__sha1,
            "sha256": self.__sha256,
            "signature": self.__signature,
            "version": self.__version
        }


# pylint: disable=too-many-instance-attributes
class CertParticipant:
    """
   CERT owner/issuer information.
   """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            name: str,
            email: str,
            unit: str,
            organization: str,
            city: str,
            state: str,
            country: str,
            domain: str
    ):
        self.__name = name
        self.__email = email
        self.__unit = unit
        self.__organization = organization
        self.__city = city
        self.__state = state
        self.__country = country
        self.__domain = domain

    def __eq__(self, other: Any):
        return isinstance(other, CertParticipant) and \
               self.__name == other.get_name() and \
               self.__email == other.get_email() and \
               self.__unit == other.get_unit() and \
               self.__organization == other.get_organization() and \
               self.__city == other.get_city() and \
               self.__state == other.get_state() and \
               self.__country == other.get_country() and \
               self.__domain == other.get_domain()

    def get_name(self) -> str:
        return self.__name

    def get_email(self) -> str:
        return self.__email

    def get_unit(self) -> str:
        return self.__unit

    def get_organization(self) -> str:
        return self.__organization

    def get_city(self) -> str:
        return self.__city

    def get_state(self) -> str:
        return self.__state

    def get_country(self) -> str:
        return self.__country

    def get_domain(self) -> str:
        return self.__domain

    def as_dict(self) -> Dict:
        return {
            "name": self.__name,
            "email": self.__email,
            "unit": self.__unit,
            "organization": self.__organization,
            "city": self.__city,
            "state": self.__state,
            "country": self.__country,
            "domain": self.__domain,
        }


class Cert(File):
    """
   Android CERT.RSA/DSA certificate file information.
   """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            filename: str,
            size: str,
            md5hash: str,
            sha1hash: str,
            sha256hash: str,
            sha512hash: str,
            serial_number: str,
            validity: CertValidity,
            fingerprint: CertFingerprint,
            owner: CertParticipant,
            issuer: CertParticipant
    ):
        super().__init__(filename, size, md5hash, sha1hash, sha256hash, sha512hash)
        self.__serial_number = serial_number
        self.__validity = validity
        self.__fingerprint = fingerprint
        self.__owner = owner
        self.__issuer = issuer

    def get_serial_number(self) -> str:
        return self.__serial_number

    def get_validity(self) -> CertValidity:
        return self.__validity

    def get_fingerprint(self) -> CertFingerprint:
        return self.__fingerprint

    def get_owner(self) -> CertParticipant:
        return self.__owner

    def get_issuer(self) -> CertParticipant:
        return self.__issuer

    def as_dict(self) -> Dict:
        dump = super().as_dict()
        dump["serial_number"] = self.__serial_number
        dump["validity"] = self.__validity.as_dict()
        dump["fingerprint"] = self.__fingerprint.as_dict()
        dump["owner"] = self.__owner.as_dict()
        dump["issuer"] = self.__issuer.as_dict()
        return dump


class CertParsingError(FileParsingError):
    """
   Android CERT.RSA/DSA certificate file parsing error.
   """

    def __init__(self):
        FileParsingError.__init__(self)

    def __str__(self):
        return "Cannot parse the file as ad CERT!"


class CertParser:
    """
    Parser implementation for Android CERT.RSA/DSA certificate file.
    """

    def __init__(self, logger: Logger = default_logger):
        self.logger = logger

    def parse(self, filepath: str, filename: str = "") -> Cert:
        """
        :param filepath: path of the CERT file
        :param filename: name of the CERT file
        :return: the parsed CERT file
        :raise: FileParsingError if cannot parse the file
        :raise: CertParsingError if cannot parse the file as a CERT
        """
        self.logger.debug("Parsing CERT file: filepath=\"%s\", filename=\"%s\"", filepath, filename)
        file = FileParser(self.logger).parse(filepath, filename)
        raw = self.parse_cert(filepath)

        return Cert(
            filename=file.get_file_name(),
            size=file.get_size(),
            md5hash=file.get_md5(),
            sha1hash=file.get_sha1(),
            sha256hash=file.get_sha256(),
            sha512hash=file.get_sha512(),
            serial_number=self.__parse_string(raw, pattern=r"^Serial number: (.*)$"),
            validity=self.parse_validity(raw),
            fingerprint=self.parse_fingerprint(raw),
            owner=self.parse_participant(raw, pattern=r"^Owner: (.*)$"),
            issuer=self.parse_participant(raw, pattern=r"^Issuer: (.*)$")
        )

    @staticmethod
    def parse_cert(filepath: str) -> str:
        raw = ""
        command = "keytool -printcert -file " + filepath
        with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
            raw = process.communicate()[0].decode("utf-8")
        if re.search("^keytool error", raw, re.IGNORECASE):
            raise CertParsingError
        return raw

    @staticmethod
    def parse_validity(raw: str) -> CertValidity:
        valid_from = ""
        valid_to = ""

        raw_validity = CertParser.__parse_string(raw, pattern=r"^Valid (.*)$")
        if raw_validity:
            valid_from = CertParser.__parse_string(raw_validity, pattern=r"^from: (.*)until: ")
            valid_to = CertParser.__parse_string(raw_validity, pattern=r"until: (.*)$")

            try:
                time_zone = get_localzone()

                local_dt_from = time_zone.localize(
                    dt=datetime.strptime(valid_from, "%a %b %d %H:%M:%S %Z %Y")
                )
                utc_dt_from = local_dt_from.astimezone(tzutc())

                local_dt_until = time_zone.localize(
                    dt=datetime.strptime(valid_to, "%a %b %d %H:%M:%S %Z %Y")
                )
                utc_dt_until = local_dt_until.astimezone(tzutc())
            except ValueError:
                pass
            else:
                valid_from = utc_dt_from.strftime("%Y-%m-%d %H:%M:%SZ")
                valid_to = utc_dt_until.strftime("%Y-%m-%d %H:%M:%SZ")

        return CertValidity(
            valid_from=valid_from,
            valid_to=valid_to
        )

    @staticmethod
    def parse_fingerprint(raw: str) -> CertFingerprint:
        return CertFingerprint(
            md5=CertParser.__parse_string(raw, pattern=r"^\t MD5: (.*)$"),
            sha1=CertParser.__parse_string(raw, pattern=r"^\t SHA1: (.*)$"),
            sha256=CertParser.__parse_string(raw, pattern=r"^\t SHA256: (.*)$"),
            signature=CertParser.__parse_string(raw, pattern=r"^\t?\s?Signature algorithm name: (.*)$"),
            version=CertParser.__parse_string(raw, pattern=r"^\t?\s?Version: (.*)$")
        )

    @staticmethod
    def parse_participant(raw: str, pattern: str) -> CertParticipant:
        raw_owner = CertParser.__parse_string(raw, pattern=pattern)
        if raw_owner:
            raw_owner = raw_owner.replace(", ", "\n")
        return CertParticipant(
            name=CertParser.__parse_string(raw_owner, pattern=r"^CN=(.*)"),
            email=CertParser.__parse_string(raw_owner, pattern=r"^EMAILADDRESS=(.*)"),
            unit=CertParser.__parse_string(raw_owner, pattern=r"^OU=(.*)"),
            organization=CertParser.__parse_string(raw_owner, pattern=r"^O=(.*)"),
            city=CertParser.__parse_string(raw_owner, pattern=r"^L=(.*)"),
            state=CertParser.__parse_string(raw_owner, pattern=r"^ST=(.*)"),
            country=CertParser.__parse_string(raw_owner, pattern=r"^C=(.*)"),
            domain=CertParser.__parse_string(raw_owner, pattern=r"^DC=(.*)")
        )

    @staticmethod
    def __parse_string(string: str, pattern: str) -> str:
        match = re.search(pattern, string, re.MULTILINE | re.IGNORECASE)
        if match and match.group(1):
            return match.group(1).strip()
        return ""

    @staticmethod
    def looks_like_cert(filename: str) -> bool:
        return filename == "META-INF/CERT.RSA" or \
            filename == "META-INF/CERT.DSA" or \
            fnmatch(filename, "META-INF/*.RSA")
