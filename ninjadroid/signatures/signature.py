import re
import json


class Signature:
    """
    Parser for generic signature.
    """

    _CONFIG_FILE = "etc/signatures.json"
    _SIGNATURE_KEYS_LIST = ["signatures"]

    def __init__(self):
        signatures_regex = self._get_signature_regex_from_config()
        self._compile_regex(signatures_regex)

    def _get_signature_regex_from_config(self):
        signatures_regex = {}
        with open(self._CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)

            for signature_name in self._SIGNATURE_KEYS_LIST:
                signatures_list = config[signature_name]
                signatures_list.reverse()

                signatures_regex[signature_name] = ""

                for signature in signatures_list:
                    signatures_regex[signature_name] += r'' + signature + r'|'
                signatures_regex[signature_name] = signatures_regex[signature_name][:-1]
        return signatures_regex


    @classmethod
    def _compile_regex(cls, signatures):
        """
        Compile the Shell commands signature regex.

        :param signatures: Dictionary of the signature regex, whose keys are the ones declared in _SIGNATURE_KEYS_LIST.
        """
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

    def is_valid(self, signature):
        """
        Validate a given signature.

        :param signature: The signature to be validated.
        :return: True if it is a valid signature, False otherwise.
        """
        if signature is None or signature == "":
            return False

        return self._is_regex.search(signature)

    def get_matches_in_string(self, string):
        """
        Search whether a string matches at least a signature.

        :param string: The string to be searched.
        :return: The matched signature, if the string contains a signature, an empty string otherwise.
        """
        if string is None or string == "":
            return ""

        match = self._is_contained_regex.search(string)

        if match is not None and match.group(0) is not None:
            return str(match.group(0)).strip()

        return ""
