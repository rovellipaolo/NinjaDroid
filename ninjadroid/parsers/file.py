from logging import getLogger, Logger
from hashlib import md5, sha1, sha256, sha512
from os import access, R_OK
from os.path import getsize, isfile, isdir
from typing import Dict
from zipfile import is_zipfile


default_logger = getLogger(__name__)


class File:
    """
    Generic file information.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, filename: str, size: str, md5hash: str, sha1hash: str, sha256hash: str, sha512hash: str):
        self.__name = filename
        self.__size = size
        self.__md5 = md5hash
        self.__sha1 = sha1hash
        self.__sha256 = sha256hash
        self.__sha512 = sha512hash

    def get_file_name(self) -> str:
        return self.__name

    def get_size(self) -> int:
        return self.__size

    def get_md5(self) -> str:
        return self.__md5

    def get_sha1(self) -> str:
        return self.__sha1

    def get_sha256(self) -> str:
        return self.__sha256

    def get_sha512(self) -> str:
        return self.__sha512

    def as_dict(self) -> Dict:
        return {
            "file": self.__name,
            "size": self.__size,
            "md5": self.__md5,
            "sha1": self.__sha1,
            "sha256": self.__sha256,
            "sha512": self.__sha512,
        }


class FileParsingError(Exception):
    """
    Generic file parsing error.
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "Cannot parse the file!"


class FileParser:
    """
    Parser implementation for generic files.
    """

    def __init__(self, logger: Logger = default_logger):
        self.logger = logger

    def parse(self, filepath: str, filename: str = "") -> File:
        """
        :param filepath: path of the file
        :param filename: name of the file
        :return: the parsed file
        :raise: FileParsingError if cannot parse the file
        """
        if not self.is_readable_file(filepath):
            raise FileParsingError

        with open(filepath, "rb") as file:
            self.logger.debug("Reading file: filepath=\"%s\"", filepath)
            raw = file.read()

        return File(
            filename=filename if filename != "" else filepath,
            size=getsize(filepath),
            md5hash=md5(raw).hexdigest(),
            sha1hash=sha1(raw).hexdigest(),
            sha256hash=sha256(raw).hexdigest(),
            sha512hash=sha512(raw).hexdigest()
        )

    @staticmethod
    def is_file(path: str) -> bool:
        return path != "" and isfile(path)

    @staticmethod
    def is_readable_file(path: str) -> bool:
        return FileParser.is_file(path) and access(path, R_OK)

    @staticmethod
    def is_zip_file(path: str) -> bool:
        return FileParser.is_file(path) and is_zipfile(path)

    @staticmethod
    def is_directory(path: str) -> bool:
        return path != "" and isdir(path)
