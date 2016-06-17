import subprocess

from lib.parsers.DexParserInterface import DexParserInterface
from lib.parsers.File import File
from lib.signatures.URISignature import URISignature
from lib.signatures.ShellCommandSignature import ShellCommandSignature
from lib.signatures.Signature import Signature


##
# Parser implementation for Android classes.dex file.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#
class Dex(File, DexParserInterface):
    __FILE_NAME_CLASSES_DEX = "classes.dex"

    # Class constructor.
    #
    # @param filepath  The classes.dex file path.
    # @param string_processing  If True (default), the URLs and shell commands in the classes.dex will be extracted.
    #
    def __init__(self, filepath, string_processing=True):
        super(Dex, self).__init__(filepath, "classes.dex")

        self._strings = []
        self._urls = []
        self._shell_commands = []
        self._custom_signatures = []

        self._extract_and_set_strings()

        if string_processing:
            self._extract_and_set_substring_from()

    ##
    # Extract the strings from the classes.dex file and set the correspondent attributes. Empty strings will be removed.
    #
    def _extract_and_set_strings(self):
        process = subprocess.Popen("strings " + self.get_file_path(), stdout=subprocess.PIPE, stderr=None, shell=True)
        self._strings = process.communicate()[0].decode("utf-8").splitlines()
        self._strings.sort()
        while "" in self._strings:
            self._strings.remove("")

    ##
    # Extract the strings from the classes.dex file and set the correspondent attributes. Empty strings will be removed.
    #
    def _extract_and_set_substring_from(self):
        for string in self._strings:
            if string == "":
                continue

            self._extract_and_set_urls_from(string)
            self._extract_and_set_shell_commands_from(string)
            #self._extract_and_set_signatures_from(string)

        self._urls.sort()
        self._shell_commands.sort()
        #self._custom_signatures.sort()

    ##
    # Extract eventual URLs from a string and set the correspondent attribute.
    #
    # @param string  The string from which extracting the eventual URLs.
    #
    def _extract_and_set_urls_from(self, string):
        if not hasattr(self, "_uri"):
            self._uri_signature = URISignature()
        if len(string) > 6:
            url = self._uri_signature.get_matches_in_string(string)
            if url != "" and url not in self._urls:
                self._urls.append(url)

    ##
    # Extract eventual shell commands from a string and set the correspondent attribute.
    #
    # @param string  The string from which extracting the eventual shell commands.
    #
    def _extract_and_set_shell_commands_from(self, string):
        if not hasattr(self, "_shell"):
            self._shell_signature = ShellCommandSignature()
        command = self._shell_signature.get_matches_in_string(string)
        if command != "" and command not in self._shell_commands:
            self._shell_commands.append(command)

    ##
    # Extract eventual signatures from a string and set the correspondent attribute.
    #
    # @param string  The string from which extracting the eventual signatures.
    #
    def _extract_and_set_signatures_from(self, string):
        if not hasattr(self, "_shell"):
            self._generic_signature = Signature()
            match = self._generic_signature.get_matches_in_string(string)
            if match != "" and match not in self._custom_signatures:
                self._custom_signatures.append(match)

    @staticmethod
    def looks_like_a_dex(filename):
        return filename == Dex.__FILE_NAME_CLASSES_DEX

    def dump(self):
        dump = super(Dex, self).dump()
        dump["urls"] = self._urls
        dump["shell_commands"] = self._shell_commands
        #dump["custom_signatures"] = self._custom_signatures
        dump["strings"] = self._strings
        return dump

    def get_strings(self):
        return self._strings

    def get_urls(self):
        return self._urls

    def get_shell_commands(self):
        return self._shell_commands

    def get_custom_signatures(self):
        return self._custom_signatures
