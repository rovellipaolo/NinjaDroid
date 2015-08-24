##
# @file File.py
# @brief Class representing a file.
# @version 1.0
# @date 2015-07-06 19:59:00
# @author Paolo Rovelli
# @copyright GNU Lesser General Public License v3.0 (https://www.gnu.org/licenses/lgpl.html).
#

from hashlib import md5, sha1, sha256, sha512
from os import access, R_OK
from os.path import getsize, isfile


##
# ErrorAPKParsing class.
#
class ErrorFileParsing(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "Cannot parse the file!"


##
# File class.
# 
# @author Paolo Rovelli
#
class File(object):
    ##
    # Class constructor.
    #
    # @param filepath  The absolute path to the file.
    # @param filename  the name of the file.
    #
    def __init__(self, filepath, filename=""):
        if filename != "":
            self._name = filename
        else:
            self._name = filepath
        if filepath == "" or not isfile(filepath) or not access(filepath, R_OK):
            raise ErrorFileParsing

        # Attributes initialization:
        self._raw = ""
        self._size = 0
        self._md5 = ""
        self._sha1 = ""
        self._sha256 = ""
        self._sha512 = ""

        # Retrieve the size of the file:
        self._size = getsize(filepath)

        with open(filepath, 'rb') as fp:
            self._raw = fp.read()

            # Retrieve the hashes of the file:
            self._md5 = md5(self._raw).hexdigest()
            self._sha1 = sha1(self._raw).hexdigest()
            self._sha256 = sha256(self._raw).hexdigest()
            self._sha512 = sha512(self._raw).hexdigest()

    ##
    # Dump the File object.
    #
    # @return A Dictionary representing the File object.
    #
    def dump(self):
        return {
            "file": self._name,
            "size": self._size,
            "md5": self._md5,
            "sha1": self._sha1,
            "sha256": self._sha256,
            "sha512": self._sha512,
        }

    ##
    # Retrieve the raw file.
    #
    # @return The raw file.
    #
    def get_raw_file(self):
        return self._raw

    ##
    # Retrieve the file path.
    #
    # @return The file path.
    #
    def get_file_name(self):
        return self._name

    ##
    # Retrieve the size (in Bytes) of the file.
    #
    # @return The size (in Bytes).
    #
    def get_size(self):
        return self._size

    ##
    # Retrieve the MD5 checksum of the file.
    #
    # @return The MD5 checksum.
    #
    def get_md5(self):
        return self._md5

    ##
    # Retrieve the SHA-1 checksum of the file.
    #
    # @return The SHA-1 checksum.
    #
    def get_sha1(self):
        return self._sha1

    ##
    # Retrieve the SHA-256 checksum of the file.
    #
    # @return The SHA-256 checksum.
    #
    def get_sha256(self):
        return self._sha256

    ##
    # Retrieve the SHA-512 checksum of the file.
    #
    # @return The SHA-512 checksum.
    #
    def get_sha512(self):
        return self._sha512
