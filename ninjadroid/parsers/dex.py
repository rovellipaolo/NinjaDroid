from logging import getLogger, Logger
import re
from subprocess import PIPE, Popen
from typing import Dict, Optional, List

from ninjadroid.parsers.file import File, FileParser
from ninjadroid.signatures.uri_signature import UriSignature
from ninjadroid.signatures.shell_signature import ShellSignature
from ninjadroid.signatures.signature import Signature


default_logger = getLogger(__name__)


class Dex(File):
    """
    Android dex file information.
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
            strings: List[str],
            urls: List[str],
            shell_commands: List[str],
            custom_signatures: List[str]
    ):
        super().__init__(filename, size, md5hash, sha1hash, sha256hash, sha512hash)
        self.__strings = strings
        self.__urls = urls
        self.__commands = shell_commands
        self.__signatures = custom_signatures

    def get_strings(self) -> List[str]:
        return self.__strings

    def get_urls(self) -> List[str]:
        return self.__urls

    def get_shell_commands(self) -> List[str]:
        return self.__commands

    def get_custom_signatures(self) -> List[str]:
        return self.__signatures

    def as_dict(self) -> Dict:
        dump = super().as_dict()
        dump["strings"] = self.__strings
        dump["urls"] = self.__urls
        dump["shell_commands"] = self.__commands
        # TODO: improve custom signatures parsing performance (commented in the meanwhile because far too slow)
        # dump["custom_signatures"] = self.__signatures
        return dump


class DexParser:
    """
    Parser implementation for Android dex files.
    """

    def __init__(self, logger: Logger = default_logger):
        self.logger = logger

    def parse(self, filepath: str, filename: str) -> Dex:
        """
        :param filepath: path of the dex file
        :param filename: name of the dex file
        :return: the parsed dex file
        :raise: FileParsingError if cannot parse the file
        """
        self.logger.debug("Parsing dex file: filepath=\"%s\", filename=\"%s\"", filepath, filename)
        file = FileParser(self.logger).parse(filepath, filename)

        self.logger.debug("Extracting strings...")
        strings = self.parse_strings(filepath)
        self.logger.debug("Strings extracted: %d", len(strings))

        self.logger.debug("Extracting URLs...")
        urls = self.parse_signatures(signature=UriSignature(), strings=strings, min_string_len=6)
        self.logger.debug("URLs extracted: %s ", len(urls))

        self.logger.debug("Extracting shell commands...")
        shell_commands = self.parse_signatures(signature=ShellSignature(), strings=strings)
        self.logger.debug("Shell commands extracted: %s", len(shell_commands))

        # TODO: improve custom signatures parsing performance (commented in the meanwhile because far too slow)
        # self.logger.debug("Extracting custom signatures...")
        custom_signatures = []  # self.extract_signatures(signature=Signature(), strings=self._strings)
        # self.logger.debug("Custom signatures extracted: %s", len(custom_signatures))

        return Dex(
            filename=file.get_file_name(),
            size=file.get_size(),
            md5hash=file.get_md5(),
            sha1hash=file.get_sha1(),
            sha256hash=file.get_sha256(),
            sha512hash=file.get_sha512(),
            strings=strings,
            urls=urls,
            shell_commands=shell_commands,
            custom_signatures=custom_signatures,
        )

    @staticmethod
    def parse_strings(filepath: str) -> List:
        with Popen("strings " + filepath, stdout=PIPE, stderr=None, shell=True) as process:
            strings = filter(
                lambda string: string != "",
                (string.strip() for string in process.communicate()[0].decode("utf-8").splitlines())
            )
            return sorted(strings)

    @staticmethod
    def parse_signatures(signature: Signature, strings: List, min_string_len: Optional[bool] = None) -> List:
        signatures = []
        for string in strings:
            if min_string_len is None or len(string) > min_string_len:
                match, is_valid = signature.search(string)
                if is_valid and match is not None and match != "":
                    signatures.append(match)
        return sorted(signatures)

    @staticmethod
    def looks_like_dex(filename: str) -> bool:
        return bool(re.search(".*\\.dex$", filename))
