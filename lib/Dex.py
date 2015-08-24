##
# @file Dex.py
# @brief Parser for Android classes.dex file.
# @version 1.0
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

import subprocess

from lib.File import File
from lib.URI import URI
from lib.Shell import Shell
#from lib.Signature import Signature


##
# Dex class.
#
class Dex(File, object):
    # Class constructor.
    #
    # @param filepath  The classes.dex file path.
    # @param string_processing  If set to True (dafault), the URLs and shell commands in the classes.dex will be extracted.
    #
    def __init__(self, filepath, string_processing=True):
        super(Dex, self).__init__(filepath, "classes.dex")

        self._strings = []
        self._urls = []
        self._shell_commands = []
        #self._custom_signatures = []

        # Extract the strings from the classes.dex file:
        process = subprocess.Popen("strings " + filepath, stdout=subprocess.PIPE, stderr=None, shell=True)
        self._strings = process.communicate()[0].decode("utf-8").splitlines()
        self._strings.sort()
        while "" in self._strings: self._strings.remove("")

        if string_processing:
            uri = URI()
            shell = Shell()
            #signature = Signature()

            for string in self._strings:
                if string == "":
                    continue

                # Extract eventual URLs:
                if len(string) > 6:
                    url = uri.get_matches_in_string(string)
                    if url != "" and url not in self._urls:
                        self._urls.append(url)

                # Extract eventual shell commands:
                command = shell.get_matches_in_string(string)
                if command != "" and command not in self._shell_commands:
                    self._shell_commands.append(command)

                # Extract eventual custom signatures:
                #match = signature.get_matches_in_string(string)
                #if match != "" and match not in self._custom_signatures:
                #    self._custom_signatures.append(match)

            self._urls.sort()
            self._shell_commands.sort()
            #self._custom_signatures.sort()

    ##
    # Dump the Dex object.
    #
    # @return A Dictionary representing the Dex object.
    #
    def dump(self):
        dump = super(Dex, self).dump()
        dump["urls"] = self._urls
        dump["shell_commands"] = self._shell_commands
        #dump["custom_signatures"] = self._custom_signatures
        dump["strings"] = self._strings
        return dump

    ##
    # Retrieve the strings in the classes.dex file.
    #
    # @return the list of strings.
    #
    def get_strings(self):
        return self._strings

    ##
    # Retrieve the URLs in the classes.dex file.
    #
    # @return the list of URLs.
    #
    def get_urls(self):
        return self._urls

    ##
    # Retrieve the shell commands in the classes.dex file.
    #
    # @return the list of shell commands.
    #
    def get_shell_commands(self):
        return self._shell_commands

    ##
    # Retrieve the custom signatures in the classes.dex file.
    #
    # @return the list of custom signatures.
    #
    #def get_custom_signatures(self):
    #    return self._custom_signatures
