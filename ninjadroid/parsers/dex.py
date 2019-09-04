import logging
import os.path
import re
import subprocess
from typing import Dict, List, Sequence

from ninjadroid.parsers.dex_interface import DexInterface
from ninjadroid.parsers.file import File
from ninjadroid.signatures.uri_signature import URISignature
from ninjadroid.signatures.shell_command_signature import ShellCommandSignature
# from ninjadroid.signatures.signature import Signature

logger = logging.getLogger(__name__)


class Dex(File, DexInterface):
    """
    Parser implementation for Android DEX file.
    """

    __DEX_FILE_REGEX = ".*\\.dex$"

    def __init__(self, filepath: str, string_processing: bool = True, logger=logger):
        super(Dex, self).__init__(filepath, os.path.split(filepath)[1])

        logger.debug("Init Dex on %s, string_processing=%s", filepath, string_processing)

        self._strings = []  # type: List[str]
        self._urls = []  # type: List[str]
        self._shell_commands = []  # type: List[str]
        self._custom_signatures = []  # type: List[str]

        self.logger = logger

        self._extract_and_set_strings()

        if string_processing:
            self._extract_and_set_substring_from()

    def _extract_and_set_strings(self):
        """
        Extract the strings from the DEX file and set the corresponding attributes.
        Empty strings will be removed.
        """
        self.logger.debug("Extracting strings...")
        command = "strings " + self.get_file_path()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        strings = filter(lambda s: s != "",
                         (s.strip() for s in process.communicate()[0].decode("utf-8").splitlines()))
        self._strings = sorted(strings)
        self.logger.debug("%d strings extracted", len(self._strings))

    def _extract_and_set_substring_from(self):
        """
        Extract the strings from the DEX file and set the corresponding attributes.
        Empty strings will be removed.
        """
        self.logger.debug("Extracting URLs from strings...")
        urls = (url
                for s in self._strings
                for url in self._extract_urls_from(s))
        self._urls = sorted(urls)
        self.logger.debug("%s URLs extracted from strings", len(self._urls))

        self.logger.debug("Extracting shell commands from strings...")
        shell_commands = (command
                          for s in self._strings
                          for command in self._extract_shell_commands_from(s))

        self._shell_commands = sorted(shell_commands)
        self.logger.debug("%s shell commands extracted from strings", len(self._shell_commands))
        # self._custom_signatures.sort()

    def _extract_urls_from(self, string: str) -> Sequence[str]:
        """
        Extract URLs from a string.

        Currently at most one URL is extracted from a string. This may change.

        :param string: The string from which to extract the URLs.
        """
        if not hasattr(self, "_uri"):
            self._uri_signature = URISignature()
        if len(string) > 6:
            match = self._uri_signature.get_matches_in_string(string)
            if match != "":
                return [match]
        return []

    def _extract_shell_commands_from(self, string: str) -> Sequence[str]:
        """
        Extract shell commands from a string.

        Currently at most one shell command is extracted from a string. This may change.

        :param string: The string from which to extract the shell commands.
        """
        if not hasattr(self, "_shell"):
            self._shell_signature = ShellCommandSignature()
        command = self._shell_signature.get_matches_in_string(string)
        if command != "":
            return [command]
        return []

    # def _extract_and_set_signatures_from(self, string: str):
    #     """
    #     Extract eventual signatures from a string and set the corresponding attribute.
    #
    #     :param string: The string from which extracting the eventual signatures.
    #     """
    #     if not hasattr(self, "_shell"):
    #         self._generic_signature = Signature()
    #         match = self._generic_signature.get_matches_in_string(string)
    #         if match != "" and match not in self._custom_signatures:
    #             self._custom_signatures.append(match)

    @staticmethod
    def looks_like_a_dex(filename: str) -> bool:
        return bool(re.search(Dex.__DEX_FILE_REGEX, filename))

    def dump(self) -> Dict:
        dump = super(Dex, self).dump()
        dump["urls"] = self._urls
        dump["shell_commands"] = self._shell_commands
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
