from abc import ABCMeta, abstractmethod


##
# Parser interface for a file.
#
# @author Paolo Rovelli
# @copyright GNU Lesser General Public License v3.0 (https://www.gnu.org/licenses/lgpl.html).
#
class FileParserInterface(object):
    __metaclass__ = ABCMeta

    ##
    # Check whether a given path is a file.
    #
    @staticmethod
    @abstractmethod
    def is_a_file(filepath):
        pass

    ##
    # Check whether a given path is a readable file.
    #
    @staticmethod
    @abstractmethod
    def is_a_readable_file(filepath):
        pass

    ##
    # Dump the File object into a Dictionary.
    #
    # @return A Dictionary representing the File object.
    #
    @abstractmethod
    def dump(self):
        pass

    ##
    # Retrieve the raw file.
    #
    # @return The raw file.
    #
    @abstractmethod
    def get_raw_file(self):
        pass

    ##
    # Retrieve the file name.
    #
    # @return The file name.
    #
    @abstractmethod
    def get_file_name(self):
        pass

    ##
    # Retrieve the file path.
    #
    # @return The file path.
    #
    @abstractmethod
    def get_file_path(self):
        pass

    ##
    # Retrieve the size (in Bytes) of the file.
    #
    # @return The size (in Bytes).
    #
    @abstractmethod
    def get_size(self):
        pass

    ##
    # Retrieve the MD5 checksum of the file.
    #
    # @return The MD5 checksum.
    #
    @abstractmethod
    def get_md5(self):
        pass

    ##
    # Retrieve the SHA-1 checksum of the file.
    #
    # @return The SHA-1 checksum.
    #
    @abstractmethod
    def get_sha1(self):
        pass

    ##
    # Retrieve the SHA-256 checksum of the file.
    #
    # @return The SHA-256 checksum.
    #
    @abstractmethod
    def get_sha256(self):
        pass

    ##
    # Retrieve the SHA-512 checksum of the file.
    #
    # @return The SHA-512 checksum.
    #
    @abstractmethod
    def get_sha512(self):
        pass
