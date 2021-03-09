import os.path
import json
import re
from typing import Dict, Optional, Pattern, Tuple


class Signature:
    """
    Parser for generic signature.
    """

    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "signatures.json")
    SIGNATURE_KEYS_LIST = ["signatures"]
    IS_REGEX = None
    IS_CONTAINED_REGEX = None

    def __init__(self):
        # NOTE: IS_REGEX and IS_CONTAINED_REGEX are time-consuming to compile.
        # Since they don't change at runtime we can do this just once.
        if self.IS_REGEX is None or self.IS_CONTAINED_REGEX is None:
            signatures_regex = self.get_signature_regex_from_config()
            (self.IS_REGEX, self.IS_CONTAINED_REGEX) = self.compile_regex(signatures_regex)  # pylint: disable=invalid-name

    @classmethod
    def get_signature_regex_from_config(cls) -> Dict:
        signatures_regex = {}
        with open(cls.CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
            for signature_name in cls.SIGNATURE_KEYS_LIST:
                signatures_list = config[signature_name]
                signatures_list.reverse()

                signatures_regex[signature_name] = ""

                for signature in signatures_list:
                    signatures_regex[signature_name] += r'' + signature + r'|'
                signatures_regex[signature_name] = signatures_regex[signature_name][:-1]
        return signatures_regex

    @staticmethod
    def compile_regex(signatures: Dict) -> Tuple[Pattern, Pattern]:
        """
        :param signatures: Dictionary of the signature regex, whose keys are the ones declared in SIGNATURE_KEYS_LIST.
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

        is_regex = re.compile(r'^' + regex + r'$', re.IGNORECASE)
        is_contained_regex = re.compile(regex, re.IGNORECASE)

        return is_regex, is_contained_regex

    def is_valid(self, pattern: str) -> bool:
        """
        :param pattern: The pattern to validate
        :returns: true if the pattern matches
        """
        if pattern is None or pattern == "":
            return False
        return self.IS_REGEX.search(pattern) is not None

    def search(self, pattern: str) -> Tuple[Optional[str], bool]:
        """
        :param pattern: The pattern to search
        :returns: a tuple containing the optional match and a boolean "ok" status (true if the pattern matches)
        """
        if pattern is None or pattern == "":
            return None, False
        match = self.IS_CONTAINED_REGEX.search(pattern)
        if match is None or match.group(0) is None:
            return None, False
        return str(match.group(0)).strip(), True
