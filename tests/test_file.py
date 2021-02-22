from os import listdir
from os.path import join
from parameterized import parameterized
import unittest
from unittest.mock import patch, mock_open

from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.file import File


class TestFile(unittest.TestCase):
    """
    UnitTest for file.py.

    RUN: python -m unittest -v tests.test_file
    """

    ANY_FILE_SIZE = 70058
    ANY_FILE_MD5 = "c9504f487c8b51412ba4980bfe3cc15d"
    ANY_FILE_SHA1 = "482a28812495b996a92191fbb3be1376193ca59b"
    ANY_FILE_SHA256 = "8773441a656b60c5e18481fd5ba9c1bf350d98789b975987cb3b2b57ee44ee51"
    ANY_FILE_SHA512 = "559eab9840ff2f8507842605e60bb0730442ddf9ee7ca4ab4f386f715c1a4707766065d6f0b977816886692bf88b400643979e2fd13e6999358a21cabdfb3071"

    @staticmethod
    def any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512):
        mock_isfile.return_value = True
        mock_access.return_value = True
        mock_getsize.return_value = TestFile.ANY_FILE_SIZE
        mock_md5.return_value.hexdigest.return_value = TestFile.ANY_FILE_MD5
        mock_sha1.return_value.hexdigest.return_value = TestFile.ANY_FILE_SHA1
        mock_sha256.return_value.hexdigest.return_value = TestFile.ANY_FILE_SHA256
        mock_sha512.return_value.hexdigest.return_value = TestFile.ANY_FILE_SHA512

    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_init(
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
        self.any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512)

        file = File("any-file-path", "any-file-name")

        mock_file.assert_called_with("any-file-path", "rb")
        self.assertEqual("any-file-name", file.get_file_name())
        self.assertEqual(TestFile.ANY_FILE_SIZE, file.get_size())
        self.assertEqual(TestFile.ANY_FILE_MD5, file.get_md5())
        self.assertEqual(TestFile.ANY_FILE_SHA1, file.get_sha1())
        self.assertEqual(TestFile.ANY_FILE_SHA256, file.get_sha256())
        self.assertEqual(TestFile.ANY_FILE_SHA512, file.get_sha512())

    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    def test_init_with_non_existing_file(self, mock_isfile, mock_access):
        mock_isfile.return_value = False
        mock_access.return_value = True
        with self.assertRaises(ParsingError):
            File("any-file-path", "any-file-name")

    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    def test_init_with_non_readable_file(self, mock_isfile, mock_access):
        mock_isfile.return_value = True
        mock_access.return_value = False
        with self.assertRaises(ParsingError):
            File("any-file-path", "any-file-name")

    def test_integration_init(self):
        for filename in listdir(join("tests", "data")):
            if filename in ["Example.apk", "AndroidManifest.xml", "AndroidManifestBinary.xml", "CERT.RSA", "classes.dex"]:
                file = File(join("tests", "data", filename))

                self.assertTrue(file is not None)
                self.assertTrue(type(file) is File)

    @parameterized.expand([
        [True],
        [False]
    ])
    @patch('ninjadroid.parsers.file.isfile')
    def test_is_a_file(self, expected, mock_isfile):
        mock_isfile.return_value = expected

        result = File.is_a_file("any-file-path")

        self.assertEquals(expected, result)

    def test_is_a_file_with_empty_path(self):
        result = File.is_a_file("")

        self.assertFalse(result)

    @parameterized.expand([
        [True, True, True],
        [True, False, False],
        [False, True, False],
        [False, False, False]
    ])
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    def test_is_a_readable_file(self, is_file, is_readable, expected, mock_isfile, mock_access):
        mock_isfile.return_value = is_file
        mock_access.return_value = is_readable

        result = File.is_a_readable_file("any-file-path")

        self.assertEquals(expected, result)

    def test_is_a_readable_file_with_empty_path(self):
        result = File.is_a_readable_file("")

        self.assertFalse(result)

    def test_integration_dump(self):
        file = File(join("tests", "data", "Example.apk"))

        dump = file.dump()

        self.assertEqual("tests/data/Example.apk", dump["file"])
        self.assertEqual(self.ANY_FILE_SIZE, dump["size"])
        self.assertEqual(self.ANY_FILE_MD5, dump["md5"])
        self.assertEqual(self.ANY_FILE_SHA1, dump["sha1"])
        self.assertEqual(self.ANY_FILE_SHA256, dump["sha256"])
        self.assertEqual(self.ANY_FILE_SHA512, dump["sha512"])


if __name__ == "__main__":
    unittest.main()
