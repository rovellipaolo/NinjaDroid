import os.path
import re
from typing import Dict, Pattern, Tuple

from ninjadroid.signatures.signature import Signature


class ShellSignature(Signature):
    """
    Parser for shell commands.
    """

    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "shell.json")
    SIGNATURE_KEYS_LIST = ["commands", "dirs"]

    @staticmethod
    def compile_regex(signatures: Dict) -> Tuple[Pattern, Pattern]:
        regex = r'('

        # Shell command:
        regex += r'(?:(?:^|\s|_|#)'
        if signatures["commands"] != "":
            regex += r'(' + signatures["commands"] + r')'
        else:
            regex += r'(am|cat|chmod|chown||exit|iptables|kill|ls|mount|pm|ps|pwd|rm|rmdir|su)'
        regex += r'((?:(?:\s|_)(?:\d|\S)+)*))'

        # Directories:
        regex += r'|(?:\S*'
        if signatures["dirs"] != "":
            regex += r'(?:' + signatures["dirs"] + r')'
        else:
            regex += r'(?:\/data\/|\/system\/)'
        regex += r'\S*)'

        regex += r')'

        is_regex = re.compile(regex, re.IGNORECASE)
        is_contained_regex = re.compile(regex, re.IGNORECASE)

        return is_regex, is_contained_regex
