import os.path
import re
from typing import Dict, Pattern, Tuple

from ninjadroid.signatures.signature import Signature


class UriSignature(Signature):
    """
    Parser for URIs.
    """

    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "uri.json")
    SIGNATURE_KEYS_LIST = ["tlds"]

    @staticmethod
    def compile_regex(signatures: Dict) -> Tuple[Pattern, Pattern]:
        regex = r'('

        # Scheme (HTTP, HTTPS, FTP and SFTP):
        regex += r'(?:(https?|s?ftp):\/\/)?'

        # www:
        regex += r'(?:www\.)?'

        regex += r'('

        # Host and domain (including ccSLD):
        regex += r'(?:(?:[A-Z0-9][A-Z0-9-]{0,61}[A-Z0-9]\.)+)'

        # TLD:
        if signatures["tlds"] != "":
            regex += r'(' + signatures["tlds"] + r')'
        else:
            regex += r'([A-Z]{2,6})'

        # IP Address:
        regex += r'|(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'

        regex += r')'

        # Port:
        regex += r'(?::(\d{1,5}))?'

        # Query path:
        regex += r'(?:(\/\S+)*)'

        regex += r')'

        is_regex = re.compile(r'^' + regex + r'$', re.IGNORECASE)
        is_contained_regex = re.compile(regex, re.IGNORECASE)

        return is_regex, is_contained_regex
