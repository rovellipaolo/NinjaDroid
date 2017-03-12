import re

from ninjadroid.signatures.signature import Signature


class URISignature(Signature):
    """
    Parser for URIs.
    """

    _CONFIG_FILE = "ninjadroid/config/uri.json"
    _SIGNATURE_KEYS_LIST = ["tlds"]

    def __init__(self):
        super(URISignature, self).__init__()

    @classmethod
    def _compile_regex(cls, signatures):
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

        cls._is_regex = re.compile(r'^' + regex + r'$', re.IGNORECASE)
        cls._is_contained_regex = re.compile(regex, re.IGNORECASE)
