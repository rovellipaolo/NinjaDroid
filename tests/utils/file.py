import unittest
from unittest.mock import Mock

from ninjadroid.parsers.file import File, FileParsingError


# pylint: disable=too-many-arguments
def any_file(
        filename: str = "any-file-name",
        size: str = 10,
        md5: str = "any-file-md5",
        sha1: str = "any-file-sha1",
        sha256: str = "any-file-sha256",
        sha512: str = "any-file-sha512",
) -> File:
    return File(
        filename=filename,
        size=size,
        md5hash=md5,
        sha1hash=sha1,
        sha256hash=sha256,
        sha512hash=sha512
    )

def any_file_parser(file: File = any_file()) -> Mock:
    parser = Mock()
    parser.parse.return_value = file
    return parser

def any_file_parser_failure() -> Mock:
    parser = Mock()
    parser.parse.side_effect = FileParsingError()
    return parser

def assert_file_parser_called_once_with(parser: Mock, filepath: str, filename: str = "any-file-name"):
    parser.parse.assert_called_once_with(filepath, filename)

def assert_file_equal(self: unittest.TestCase, expected: File, actual: File):
    self.assertEqual(expected.get_file_name(), actual.get_file_name())
    self.assertEqual(expected.get_size(), actual.get_size())
    self.assertEqual(expected.get_md5(), actual.get_md5())
    self.assertEqual(expected.get_sha1(), actual.get_sha1())
    self.assertEqual(expected.get_sha256(), actual.get_sha256())
    self.assertEqual(expected.get_sha512(), actual.get_sha512())
