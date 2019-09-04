import subprocess
from typing import Dict, List

from ninjadroid.parsers.dex_interface import DexInterface
from ninjadroid.parsers.file import File
from ninjadroid.signatures.uri_signature import URISignature
from ninjadroid.signatures.shell_command_signature import ShellCommandSignature
from ninjadroid.signatures.signature import Signature


class Dex(File, DexInterface):
    """
    Parser implementation for Android classes.dex file.
    """

    __FILE_NAME_CLASSES_DEX = "classes.dex"

    def __init__(self, filepath: str, string_processing: bool = True):
        super(Dex, self).__init__(filepath, "classes.dex")

        self._strings = []  # type: List[str]
        self._urls = []  # type: List[str]
        self._shell_commands = []  # type: List[str]
        self._custom_signatures = []  # type: List[str]

        self._extract_and_set_strings()

        if string_processing:
            self._extract_and_set_substring_from()

    def _extract_and_set_strings(self):
        """
        Extract the strings from the classes.dex file and set the correspondent attributes.
        Empty strings will be removed.
        """
        command = "strings " + self.get_file_path()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        self._strings = process.communicate()[0].decode("utf-8").splitlines()
        self._strings.sort()
        while "" in self._strings:
            self._strings.remove("")
        self._strings = [s.strip() for s in self._strings]

    def _extract_and_set_substring_from(self):
        """
        Extract the strings from the classes.dex file and set the correspondent attributes.
        Empty strings will be removed.
        """
        for string in self._strings:
            if string == "":
                continue

            self._extract_and_set_urls_from(string)
            self._extract_and_set_shell_commands_from(string)
            #self._extract_and_set_signatures_from(string)

        self._urls.sort()
        self._shell_commands.sort()
        #self._custom_signatures.sort()

    def _extract_and_set_urls_from(self, string: str):
        """
        Extract eventual URLs from a string and set the correspondent attribute.

        :param string: The string from which extracting the eventual URLs.
        """
        if not hasattr(self, "_uri"):
            self._uri_signature = URISignature()
        if len(string) > 6:
            url = self._uri_signature.get_matches_in_string(string)
            if url != "" and url not in self._urls:
                self._urls.append(url)

    def _extract_and_set_shell_commands_from(self, string: str):
        """
        Extract eventual shell commands from a string and set the correspondent attribute.

        :param string: The string from which extracting the eventual shell commands.
        """
        if not hasattr(self, "_shell"):
            self._shell_signature = ShellCommandSignature()
        command = self._shell_signature.get_matches_in_string(string)
        if command != "" and command not in self._shell_commands:
            self._shell_commands.append(command)

    def _extract_and_set_signatures_from(self, string: str):
        """
        Extract eventual signatures from a string and set the correspondent attribute.

        :param string: The string from which extracting the eventual signatures.
        """
        if not hasattr(self, "_shell"):
            self._generic_signature = Signature()
            match = self._generic_signature.get_matches_in_string(string)
            if match != "" and match not in self._custom_signatures:
                self._custom_signatures.append(match)

    @staticmethod
    def looks_like_a_dex(filename: str) -> bool:
        return filename == Dex.__FILE_NAME_CLASSES_DEX

    def dump(self) -> Dict:
        dump = super(Dex, self).dump()
        dump["urls"] = self._urls
        dump["shell_commands"] = self._shell_commands
        #dump["custom_signatures"] = self._custom_signatures
        dump["strings"] = self._strings
        return dump

    def get_strings(self) -> List:
        return self._strings

    def get_urls(self) -> List:
        return self._urls

    def get_shell_commands(self) -> List:
        return self._shell_commands

    def get_custom_signatures(self) -> List:
        return self._custom_signatures
