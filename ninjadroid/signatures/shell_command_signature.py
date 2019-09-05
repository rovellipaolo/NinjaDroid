import os.path
import re
from typing import Dict

from ninjadroid.signatures.signature import Signature


class ShellCommandSignature(Signature):
    """
    Parser for shell commands.
    """

    _CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "shell.json")
    _SIGNATURE_KEYS_LIST = ["commands", "dirs"]

    def __init__(self):
        super(ShellCommandSignature, self).__init__()

    @staticmethod
    def _compile_regex(signatures: Dict):
        regex = r'('

        # Shell command:
        regex += r'(?:(?:^|\s|_|#)'
        if signatures["commands"] != "":
            regex += r'(' + signatures["commands"] + r')'
        else:
            regex += r'(am|cat|chmod|chown||exit|iptables|kill|ls|mount|pm|ps|pwd|rm|rmdir|su)'
        regex += r'((?:(?:\s|_)(?:\d|\S)+)*))'

        # Dirs:
        regex += r'|(?:\S*'
        if signatures["dirs"] != "":
            regex += r'(?:' + signatures["dirs"] + r')'
        else:
            regex += r'(?:\/data\/|\/system\/)'
        regex += r'\S*)'

        regex += r')'

        _is_regex = re.compile(regex, re.IGNORECASE)
        _is_contained_regex = re.compile(regex, re.IGNORECASE)

        return (_is_regex, _is_contained_regex)
