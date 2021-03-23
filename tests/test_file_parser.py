import unittest
from unittest.mock import patch, mock_open
from parameterized import parameterized
from tests.utils.file import any_file, assert_file_equal

from ninjadroid.parsers.file import FileParser, FileParsingError


# pylint: disable=too-many-arguments,line-too-long
class TestFileParser(unittest.TestCase):
    """
    Test File parser.
    """

    ANY_FILE_SIZE = 70058
    ANY_FILE_MD5 = "c9504f487c8b51412ba4980bfe3cc15d"
    ANY_FILE_SHA1 = "482a28812495b996a92191fbb3be1376193ca59b"
    ANY_FILE_SHA256 = "8773441a656b60c5e18481fd5ba9c1bf350d98789b975987cb3b2b57ee44ee51"
    ANY_FILE_SHA512 = "559eab9840ff2f8507842605e60bb0730442ddf9ee7ca4ab4f386f715c1a4707766065d6f0b977816886692bf88b400643979e2fd13e6999358a21cabdfb3071"

    sut = FileParser()

    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse(
            self,
            mock_file,
            mock_isfile,
            mock_access,
            mock_getsize,
            mock_md5,
            mock_sha1,
            mock_sha256,
            mock_sha512
    ):
        mock_isfile.return_value = True
        mock_access.return_value = True
        mock_getsize.return_value = self.ANY_FILE_SIZE
        mock_md5.return_value.hexdigest.return_value = self.ANY_FILE_MD5
        mock_sha1.return_value.hexdigest.return_value = self.ANY_FILE_SHA1
        mock_sha256.return_value.hexdigest.return_value = self.ANY_FILE_SHA256
        mock_sha512.return_value.hexdigest.return_value = self.ANY_FILE_SHA512

        file = self.sut.parse("any-file-path", "any-file-name")

        mock_file.assert_called_with("any-file-path", "rb")
        assert_file_equal(
            self,
            expected=any_file(
                filename="any-file-name",
                size=self.ANY_FILE_SIZE,
                md5=self.ANY_FILE_MD5,
                sha1=self.ANY_FILE_SHA1,
                sha256=self.ANY_FILE_SHA256,
                sha512=self.ANY_FILE_SHA512
            ),
            actual=file
        )

    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_without_filename(
            self,
            mock_file,
            mock_isfile,
            mock_access,
            mock_getsize,
            mock_md5,
            mock_sha1,
            mock_sha256,
            mock_sha512
    ):
        mock_isfile.return_value = True
        mock_access.return_value = True
        mock_getsize.return_value = self.ANY_FILE_SIZE
        mock_md5.return_value.hexdigest.return_value = self.ANY_FILE_MD5
        mock_sha1.return_value.hexdigest.return_value = self.ANY_FILE_SHA1
        mock_sha256.return_value.hexdigest.return_value = self.ANY_FILE_SHA256
        mock_sha512.return_value.hexdigest.return_value = self.ANY_FILE_SHA512

        file = self.sut.parse("any-file-path")

        mock_file.assert_called_with("any-file-path", "rb")
        assert_file_equal(
            self,
            expected=any_file(
                filename="any-file-path",
                size=self.ANY_FILE_SIZE,
                md5=self.ANY_FILE_MD5,
                sha1=self.ANY_FILE_SHA1,
                sha256=self.ANY_FILE_SHA256,
                sha512=self.ANY_FILE_SHA512
            ),
            actual=file
        )

    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_fails_when_open_fails(self, mock_file, mock_isfile, mock_access):
        mock_isfile.return_value = True
        mock_access.return_value = True
        mock_file.side_effect = OSError()

        with self.assertRaises(OSError):
            self.sut.parse("any-file-path")

    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    def test_parse_fails_with_non_existing_file(self, mock_isfile, mock_access):
        mock_isfile.return_value = False
        mock_access.return_value = True

        with self.assertRaises(FileParsingError):
            self.sut.parse("any-file-path")

    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    def test_parse_fails_with_non_readable_file(self, mock_isfile, mock_access):
        mock_isfile.return_value = True
        mock_access.return_value = False

        with self.assertRaises(FileParsingError):
            self.sut.parse("any-file-path")

    @parameterized.expand([
        [True],
        [False]
    ])
    @patch('ninjadroid.parsers.file.isfile')
    def test_is_file(self, expected, mock_isfile):
        mock_isfile.return_value = expected

        result = self.sut.is_file("any-path")

        self.assertEqual(expected, result)

    def test_is_file_with_empty_path(self):
        result = self.sut.is_file("")

        self.assertFalse(result)

    @parameterized.expand([
        [True, True, True],
        [True, False, False],
        [False, True, False],
        [False, False, False]
    ])
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    def test_is_readable_file(self, is_file, is_readable, expected, mock_isfile, mock_access):
        mock_isfile.return_value = is_file
        mock_access.return_value = is_readable

        result = self.sut.is_readable_file("any-path")

        self.assertEqual(expected, result)

    def test_is_readable_file_with_empty_path(self):
        result = self.sut.is_readable_file("")

        self.assertFalse(result)

    @parameterized.expand([
        [True, True, True],
        [True, False, False],
        [False, True, False],
        [False, False, False]
    ])
    @patch('ninjadroid.parsers.file.is_zipfile')
    @patch('ninjadroid.parsers.file.isfile')
    def test_is_zip_file(self, is_file, is_zip, expected, mock_isfile, mock_is_zipfile):
        mock_isfile.return_value = is_file
        mock_is_zipfile.return_value = is_zip

        result = self.sut.is_zip_file("any-path")

        self.assertEqual(expected, result)

    def test_is_zip_file_with_empty_path(self):
        result = self.sut.is_zip_file("")

        self.assertFalse(result)

    @parameterized.expand([
        [True],
        [False]
    ])
    @patch('ninjadroid.parsers.file.isdir')
    def test_is_directory(self, expected, mock_isdir):
        mock_isdir.return_value = expected

        result = self.sut.is_directory("any-path")

        self.assertEqual(expected, result)

    def test_is_directory_with_empty_path(self):
        result = self.sut.is_directory("")

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
