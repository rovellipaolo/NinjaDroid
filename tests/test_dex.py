from os.path import join
from parameterized import parameterized
import unittest
from unittest.mock import patch, mock_open
from tests.utils.popen import any_popen, assert_popen_called_once_with

from ninjadroid.parsers.dex import Dex
from ninjadroid.errors.parsing_error import ParsingError


class TestDex(unittest.TestCase):
    """
    UnitTest for dex.py.

    RUN: python -m unittest -v tests.test_dex
    """

    FILE_NAME = "classes.dex"
    ANY_FILE_SIZE = 2132
    ANY_FILE_MD5 = "7bc52ece5249ccd2d72c4360f9be2ca5"
    ANY_FILE_SHA1 = "89476799bf92798047ca026c922a5bc33983b008"
    ANY_FILE_SHA256 = "3f543c68c4c059548cec619a68f329010d797e5e4c00aa46cd34c0d19cabe056"
    ANY_FILE_SHA512 = "0725f961bc1bac47eb8dd045c2f0a0cf5475fd77089af7ddc3098e341a95d8b5624969b6fa47606a05d5a6adf9d74d0c52562ea41a376bd3d7d0aa3695ca2e22"

    @staticmethod
    def any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512):
        mock_isfile.return_value = True
        mock_access.return_value = True
        mock_getsize.return_value = TestDex.ANY_FILE_SIZE
        mock_md5.return_value.hexdigest.return_value = TestDex.ANY_FILE_MD5
        mock_sha1.return_value.hexdigest.return_value = TestDex.ANY_FILE_SHA1
        mock_sha256.return_value.hexdigest.return_value = TestDex.ANY_FILE_SHA256
        mock_sha512.return_value.hexdigest.return_value = TestDex.ANY_FILE_SHA512

    @patch('ninjadroid.parsers.dex.Popen')
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
            mock_sha512,
            mock_popen
    ):
        mock_popen.return_value = any_popen(b"")
        self.any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512)

        dex = Dex("any-file-path", "any-file-name")

        mock_file.assert_called_with("any-file-path", "rb")
        assert_popen_called_once_with(mock_popen, "strings any-file-path")
        self.assertEqual("any-file-name", dex.get_file_name())
        self.assertEqual(TestDex.ANY_FILE_SIZE, dex.get_size())
        self.assertEqual(TestDex.ANY_FILE_MD5, dex.get_md5())
        self.assertEqual(TestDex.ANY_FILE_SHA1, dex.get_sha1())
        self.assertEqual(TestDex.ANY_FILE_SHA256, dex.get_sha256())
        self.assertEqual(TestDex.ANY_FILE_SHA512, dex.get_sha512())

    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    def test_init_with_non_existing_file(self, mock_isfile, mock_access):
        mock_isfile.return_value = False
        mock_access.return_value = True
        with self.assertRaises(ParsingError):
            Dex("any-file-path", "any-file-name")

    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    def test_init_with_non_readable_file(self, mock_isfile, mock_access):
        mock_isfile.return_value = True
        mock_access.return_value = False
        with self.assertRaises(ParsingError):
            Dex("any-file-path", "any-file-name")

    def test_integration_init(self):
        dex = Dex(join("tests", "data", TestDex.FILE_NAME), TestDex.FILE_NAME)

        self.assertTrue(dex is not None)
        self.assertTrue(type(dex) is Dex)

    @parameterized.expand([
        ["classes.dex", True],
        ["whatever.dex", True],
        ["AndroidManifest.xml", False],
        ["META-INF/CERT.RSA", False],
        ["Example.apk", False]
    ])
    def test_looks_like_a_dex(self, filename, expected):
        result = Dex.looks_like_a_dex(filename)

        self.assertEqual(expected, result)

    def test_integration_dump(self):
        dex = Dex(join("tests", "data", TestDex.FILE_NAME), TestDex.FILE_NAME)

        dump = dex.dump()

        self.assertEqual(TestDex.FILE_NAME, dump["file"])
        self.assertEqual(TestDex.ANY_FILE_SIZE, dump["size"])
        self.assertEqual(TestDex.ANY_FILE_MD5, dump["md5"])
        self.assertEqual(TestDex.ANY_FILE_SHA1, dump["sha1"])
        self.assertEqual(TestDex.ANY_FILE_SHA256, dump["sha256"])
        self.assertEqual(TestDex.ANY_FILE_SHA512, dump["sha512"])
        self.assertEqual([], dump["urls"])
        self.assertEqual(["set"], dump["shell_commands"])


if __name__ == "__main__":
    unittest.main()
