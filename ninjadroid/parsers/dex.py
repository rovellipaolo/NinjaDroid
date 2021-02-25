import logging
import re
from subprocess import PIPE, Popen
from typing import Dict, Optional, List

from ninjadroid.parsers.file import File
from ninjadroid.signatures.uri_signature import UriSignature
from ninjadroid.signatures.shell_signature import ShellSignature
from ninjadroid.signatures.signature import Signature


global_logger = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class Dex(File):
    """
    Parser implementation for Android DEX file.
    """

    __DEX_FILE_REGEX = ".*\\.dex$"

    def __init__(self, filepath: str, filename: str, logger=global_logger):
        super().__init__(filepath, filename)
        self.logger = logger
        self.logger.debug("Dex: %filepath=s, filename=%s", filepath, filename)

        self._filename = filename
        self._strings = []  # type: List[str]
        self._urls = []  # type: List[str]
        self._shell_commands = []  # type: List[str]
        self._custom_signatures = []  # type: List[str]

        self.logger.debug("Extracting strings...")
        self._strings = self._extract_strings(self.get_file_path())
        self.logger.debug("%d strings extracted", len(self._strings))

        self.logger.debug("Extracting URLs from strings...")
        self._urls = self._extract_signatures(signature=UriSignature(), strings=self._strings, min_string_len=6)
        self.logger.debug("%s URLs extracted from strings", len(self._urls))

        self.logger.debug("Extracting shell commands from strings...")
        self._shell_commands = self._extract_signatures(signature=ShellSignature(), strings=self._strings)
        self.logger.debug("%s shell commands extracted from strings", len(self._shell_commands))

        # TODO: improve custom signatures parsing performance (commented in the meanwhile because far too slow)
        # self.logger.debug("Extracting custom signatures from strings...")
        self._custom_signatures = []
        # self._custom_signatures = self._extract_signatures(signature=Signature(), strings=self._strings)
        # self.logger.debug("%s custom signatures extracted from strings", len(self._custom_signatures))

    @staticmethod
    def _extract_strings(filepath: str) -> List:
        process = Popen("strings " + filepath, stdout=PIPE, stderr=None, shell=True)
        strings = filter(
            lambda string: string != "",
            (string.strip() for string in process.communicate()[0].decode("utf-8").splitlines())
        )
        return sorted(strings)

    @staticmethod
    def _extract_signatures(signature: Signature, strings: List, min_string_len: Optional[bool] = None) -> List:
        signatures = []
        for string in strings:
            if min_string_len is None or len(string) > min_string_len:
                match = signature.search(string)
                if match is not None and match != "":
                    signatures.append(match)
        return sorted(signatures)

    @staticmethod
    def looks_like_a_dex(filename: str) -> bool:
        return bool(re.search(Dex.__DEX_FILE_REGEX, filename))

    def dump(self) -> Dict:
        dump = super().dump()
        dump["urls"] = self._urls
        dump["shell_commands"] = self._shell_commands
        # TODO: improve custom signatures parsing performance (commented in the meanwhile because far too slow)
        # dump["custom_signatures"] = self._custom_signatures
        dump["strings"] = self.get_strings()
        return dump

    def get_strings(self) -> List:
        return self._strings

    def get_urls(self) -> List:
        return self._urls

    def get_shell_commands(self) -> List:
        return self._shell_commands

    def get_custom_signatures(self) -> List:
        return self._custom_signatures
