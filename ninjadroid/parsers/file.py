from hashlib import md5, sha1, sha256, sha512
from os import access, R_OK
from os.path import getsize, isfile
from typing import Dict

from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.file_interface import FileInterface


class File(FileInterface):
    """
    Parser implementation for a file.
    """

    def __init__(self, filepath: str, filename: str = ""):
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

        with open(filepath, "rb") as fp:
            self._raw = fp.read()
            self._extract_and_set_file_hashes()

    def _extract_and_set_file_hashes(self):
        """
        Extract the file hashes and set the corresponding attributes.
        """
        self._md5 = md5(self._raw).hexdigest()
        self._sha1 = sha1(self._raw).hexdigest()
        self._sha256 = sha256(self._raw).hexdigest()
        self._sha512 = sha512(self._raw).hexdigest()

    @staticmethod
    def is_a_file(filepath: str) -> bool:
        return filepath != "" and isfile(filepath)

    @staticmethod
    def is_a_readable_file(filepath: str) -> bool:
        return File.is_a_file(filepath) and access(filepath, R_OK)

    def dump(self) -> Dict:
        return {
            "file": self._name,
            "size": self._size,
            "md5": self._md5,
            "sha1": self._sha1,
            "sha256": self._sha256,
            "sha512": self._sha512,
        }

    def get_raw_file(self) -> str:
        return self._raw

    def get_file_name(self) -> str:
        return self._name

    def get_file_path(self) -> str:
        return self._path

    def get_size(self) -> int:
        return self._size

    def get_md5(self) -> str:
        return self._md5

    def get_sha1(self) -> str:
        return self._sha1

    def get_sha256(self) -> str:
        return self._sha256

    def get_sha512(self) -> str:
        return self._sha512
