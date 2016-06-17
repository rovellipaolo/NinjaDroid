import re

from lib.signatures.Signature import Signature


##
# Parser for URIs.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#
class URISignature(Signature, object):
    _CONFIG_FILE = "etc/uri.json"
    _SIGNATURE_KEYS_LIST = ["tlds"]

    ##
    # Class constructor.
    #
    def __init__(self):
        super(URISignature, self).__init__()

    ##
    # Compile the URI signature regex.
    #
    # @param signatures  Dictinary of the signature regex, whose keys are the ones declared in _SIGNATURE_KEYS_LIST.
    #
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
