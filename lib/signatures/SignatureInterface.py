##
# Parser for generic signatures.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

from abc import ABCMeta, abstractmethod


class SignatureInterface(object):
    __metaclass__ = ABCMeta

    ##
    # Compile the given signature regex.
    #
    # @param signatures  Dictionary of the signature regex, whose keys are the ones declared in _SIGNATURE_KEYS_LIST.
    #
    @classmethod
    @abstractmethod
    def _compile_regex(cls, signatures):
        pass

    ##
    # Validate a given signature.
    #
    # @param uri  The signature to be validated.
    # @return True if it is a valid signature, False otherwise.
    #
    @abstractmethod
    def is_valid(self, signature):
        pass

    ##
    # Search whether a string matches at least a signature.
    #
    # @param string  The string to be searched.
    # @return The matched signature, if the string contains a signature, an empty string otherwise.
    #
    @abstractmethod
    def get_matches_in_string(self, string):
        pass
