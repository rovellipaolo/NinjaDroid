import os.path
import json
import re
from typing import Dict


class Signature:
    """
    Parser for generic signature.
    """
    _CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "signatures.json")
    _SIGNATURE_KEYS_LIST = ["signatures"]
    _IS_REGEX = None
    _IS_CONTAINED_REGEX = None

    def __init__(self):
        # Note: _IS_REGEX and _IS_CONTAINED_REGEX are time-consuming to compile. Since
        # they don't change at runtime we can do this just once.
        if self._IS_REGEX is None or self._IS_CONTAINED_REGEX is None:
            signatures_regex = self._get_signature_regex_from_config()
            (self._IS_REGEX, self._IS_CONTAINED_REGEX) = self._compile_regex(signatures_regex)

    @classmethod
    def _get_signature_regex_from_config(cls):
        signatures_regex = {}
        with open(cls._CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)

            for signature_name in cls._SIGNATURE_KEYS_LIST:
                signatures_list = config[signature_name]
                signatures_list.reverse()

                signatures_regex[signature_name] = ""

                for signature in signatures_list:
                    signatures_regex[signature_name] += r'' + signature + r'|'
                signatures_regex[signature_name] = signatures_regex[signature_name][:-1]
        return signatures_regex

    @staticmethod
    def _compile_regex(signatures: Dict):
        """
        Compile the Shell commands signature regexes.

        :param signatures: Dictionary of the signature regex, whose keys are the ones declared in
          _SIGNATURE_KEYS_LIST.
        :returns: tuple of compiled regexes
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

        _is_regex = re.compile(r'^' + regex + r'$', re.IGNORECASE)
        _is_contained_regex = re.compile(regex, re.IGNORECASE)

        return (_is_regex, _is_contained_regex)

    def is_valid(self, signature: str) -> bool:
        if signature is None or signature == "":
            return False

        return self._IS_REGEX.search(signature)

    def get_matches_in_string(self, string: str) -> str:
        if string is None or string == "":
            return ""

        match = self._IS_CONTAINED_REGEX.search(string)

        if match is not None and match.group(0) is not None:
            return str(match.group(0)).strip()

        return ""
