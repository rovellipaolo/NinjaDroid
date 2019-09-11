import logging
import re
import subprocess
from typing import Dict, List, Sequence

from ninjadroid.parsers.dex_interface import DexInterface
from ninjadroid.parsers.file import File
from ninjadroid.signatures.uri_signature import URISignature
from ninjadroid.signatures.shell_command_signature import ShellCommandSignature
from ninjadroid.signatures.signature import Signature

logger = logging.getLogger(__name__)


class Dex(File, DexInterface):
    """
    Parser implementation for Android DEX file.
    """

    __DEX_FILE_REGEX = ".*\\.dex$"

    def __init__(self, filepath: str, filename: str, string_processing: bool = True, logger=logger):
        super(Dex, self).__init__(filepath, filename)

        self.logger = logger
        self.logger.debug("Init Dex on %s, filename=%s, string_processing=%s", filepath, filename, string_processing)

        self._filename = filename

        self._strings = []  # type: List[str]
        self._urls = []  # type: List[str]
        self._shell_commands = []  # type: List[str]
        self._custom_signatures = []  # type: List[str]

        self._extract_and_set_strings()

        if string_processing:
            self._extract_and_set_urls()
            self._extract_and_set_shell_commands()
            # self. _extract_and_set_signatures()

    def _extract_and_set_strings(self):
        self.logger.debug("Extracting strings...")
        command = "strings " + self.get_file_path()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        strings = filter(
            lambda string: string != "",
            (string.strip() for string in process.communicate()[0].decode("utf-8").splitlines())
        )
        self._strings = sorted(strings)
        self.logger.debug("%d strings extracted", len(self._strings))

    def _extract_and_set_urls(self):
        self.logger.debug("Extracting URLs from strings...")
        urls = (url
                for string in self._strings
                for url in self._extract_urls_from(string))
        self._urls = sorted(urls)
        self.logger.debug("%s URLs extracted from strings", len(self._urls))

    def _extract_and_set_shell_commands(self):
        self.logger.debug("Extracting shell commands from strings...")
        shell_commands = (command
                          for string in self._strings
                          for command in self._extract_shell_commands_from(string))
        self._shell_commands = sorted(shell_commands)
        self.logger.debug("%s shell commands extracted from strings", len(self._shell_commands))

    def _extract_and_set_signatures(self):
        self.logger.debug("Extracting signatures from strings...")
        custom_signatures = (signature
                             for string in self._strings
                             for signature in self._extract_custom_signature_from(string))
        self._custom_signatures = sorted(custom_signatures)
        self.logger.debug("%s signatures extracted from strings", len(self._custom_signatures))

    def _extract_urls_from(self, string: str) -> Sequence[str]:
        if not hasattr(self, "_uri"):
            self._uri_signature = URISignature()
        if len(string) > 6:
            uri = self._uri_signature.get_matches_in_string(string)
            if uri != "":
                return [uri]
        return []

    def _extract_shell_commands_from(self, string: str) -> Sequence[str]:
        if not hasattr(self, "_shell"):
            self._shell_signature = ShellCommandSignature()
        command = self._shell_signature.get_matches_in_string(string)
        if command != "":
            return [command]
        return []

    def _extract_custom_signature_from(self, string: str) -> Sequence[str]:
        if not hasattr(self, "_signatures"):
            self._generic_signature = Signature()
        signature = self._generic_signature.get_matches_in_string(string)
        if signature != "":
            return [signature]
        return []

    @staticmethod
    def looks_like_a_dex(filename: str) -> bool:
        return bool(re.search(Dex.__DEX_FILE_REGEX, filename))

    def dump(self) -> Dict:
        dump = super(Dex, self).dump()
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
