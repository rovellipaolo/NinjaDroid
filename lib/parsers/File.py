from hashlib import md5, sha1, sha256, sha512
from os import access, R_OK
from os.path import getsize, isfile

from lib.errors.ParsingError import ParsingError
from lib.parsers.FileParserInterface import FileParserInterface


##
# Parser implementation for a file.
#
# @author Paolo Rovelli
# @copyright GNU Lesser General Public License v3.0 (https://www.gnu.org/licenses/lgpl.html).
#
class File(FileParserInterface):
    ##
    # Class constructor.
    #
    # @param filepath  The absolute path to the file.
    # @param filename  the name of the file.
    # @throw ParsingError  If it is not a valid file.
    #
    def __init__(self, filepath, filename=""):
        self._path = filepath
        if filename != "":
            self._name = filename
        else:
            self._name = filepath

        if not self.is_a_readable_file(filepath):
            raise ParsingError

        self._raw = ""
        self._size = 0
        self._md5 = ""
        self._sha1 = ""
        self._sha256 = ""
        self._sha512 = ""

        self._size = getsize(filepath)

        with open(filepath, 'rb') as fp:
            self._raw = fp.read()
            self._extract_and_set_file_hashes()

    ##
    # Extract the file hashes and set the correspondent attributes.
    #
    def _extract_and_set_file_hashes(self):
        self._md5 = md5(self._raw).hexdigest()
        self._sha1 = sha1(self._raw).hexdigest()
        self._sha256 = sha256(self._raw).hexdigest()
        self._sha512 = sha512(self._raw).hexdigest()

    @staticmethod
    def is_a_file(filepath):
        return filepath != "" and isfile(filepath)

    @staticmethod
    def is_a_readable_file(filepath):
        return File.is_a_file(filepath) and access(filepath, R_OK)

    def dump(self):
        return {
            "file": self._name,
            "size": self._size,
            "md5": self._md5,
            "sha1": self._sha1,
            "sha256": self._sha256,
            "sha512": self._sha512,
        }

    def get_raw_file(self):
        return self._raw

    def get_file_name(self):
        return self._name

    def get_file_path(self):
        return self._path

    def get_size(self):
        return self._size

    def get_md5(self):
        return self._md5

    def get_sha1(self):
        return self._sha1

    def get_sha256(self):
        return self._sha256

    def get_sha512(self):
        return self._sha512
