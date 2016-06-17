from abc import ABCMeta, abstractmethod


##
# Parser interface for Android classes.dex file.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#
class DexParserInterface(object):
    __metaclass__ = ABCMeta

    ##
    # Check whether a given file looks like a classes.dex file.
    #
    @staticmethod
    @abstractmethod
    def looks_like_a_dex(filename):
        pass

    ##
    # Dump the Dex object into a Dictionary.
    #
    # @return A Dictionary representing the Dex object.
    #
    @abstractmethod
    def dump(self):
        pass

    ##
    # Retrieve the strings in the classes.dex file.
    #
    # @return The list of strings.
    #
    @abstractmethod
    def get_strings(self):
        pass

    ##
    # Retrieve the URLs in the classes.dex file.
    #
    # @return The list of URLs.
    #
    @abstractmethod
    def get_urls(self):
        pass

    ##
    # Retrieve the shell commands in the classes.dex file.
    #
    # @return The list of shell commands.
    #
    @abstractmethod
    def get_shell_commands(self):
        pass

    ##
    # Retrieve the custom signatures in the classes.dex file.
    #
    # @return The list of custom signatures.
    #
    def get_custom_signatures(self):
        pass
