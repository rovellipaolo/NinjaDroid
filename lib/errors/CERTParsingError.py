##
# Android CERT.RSA/DSA certificate file parsing error.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

from lib.errors.ParsingError import ParsingError


class CERTParsingError(ParsingError):
    def __init__(self):
        ParsingError.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an Android CERT!"
