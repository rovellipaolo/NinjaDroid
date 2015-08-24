##
# @file Signature.py
# @brief Parser for generic signatures.
# @version 1.0
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

import re
import json


##
# Shell class.
#
class Signature(object):
    _CONFIG_FILE = "etc/signatures.json"
    _SIGNATURE_KEYS_LIST = ["signatures"]

    ##
    # Class constructor.
    #
    def __init__(self):
        signatures_regex = {}

        # Load the config file:
        with open(self._CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)

            # Load all the different signatures:
            for signature_name in self._SIGNATURE_KEYS_LIST:
                signatures_list = config[signature_name]
                signatures_list.reverse()

                signatures_regex[signature_name] = ""

                for signature in signatures_list:
                    signatures_regex[signature_name] += r'' + signature + r'|'
                signatures_regex[signature_name] = signatures_regex[signature_name][:-1]

        self._compile_regex(signatures_regex)

    ##
    # Compile the given signature regex.
    #
    # @param signatures  Signature regex in an hash, whose keys are the ones declared in _SIGNATURE_KEYS_LIST (i.e. {"signatures": [...]}).
    #
    @classmethod
    def _compile_regex(cls, signatures):
        regex = r'('

        # Custom Signatures:
        regex += r'(?:^|(?:\S|\s|_|#)*)(?:'
        if signatures["signatures"] != "":
            regex += signatures["signatures"]
        else:
            regex += r'apk'
        regex += r')((?:(?:\s|_)?(?:\d|\S)+)*)'

        regex += r')'

        cls._is_regex = re.compile(r'^' + regex + r'$', re.IGNORECASE)
        cls._is_contained_regex = re.compile(regex, re.IGNORECASE)

    ##
    # Validate a given signature.
    #
    # @param uri  The signature to be validated.
    # @return True if it is a valid signature, False otherwise.
    #
    def is_valid(self, signature):
        if signature is None or signature == "":
            return False

        return self._is_regex.search(signature)

    ##
    # Search whether a string matches at least a signature.
    #
    # @param string  The string to be searched.
    # @return The matched signature, if the string contains a signature, an empty string otherwise.
    #
    def get_matches_in_string(self, string):
        if string is None or string == "":
            return ""

        match = self._is_contained_regex.search(string)

        if match is not None and match.group(0) is not None:
            return str(match.group(0)).strip()

        return ""
