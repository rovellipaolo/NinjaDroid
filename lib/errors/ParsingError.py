##
# Generic file parsing error.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

class ParsingError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "Cannot parse the file!"
