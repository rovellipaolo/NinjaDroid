from os.path import join
from parameterized import parameterized
import unittest
from unittest.mock import call, Mock, mock_open, patch
from tests.utils.popen import any_popen, assert_popen_called_once_with
from typing import List

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

    @staticmethod
    def any_signature(matches: List):
        signature = Mock()
        signature.search.side_effect = matches
        return signature

    @patch('ninjadroid.parsers.dex.ShellSignature')
    @patch('ninjadroid.parsers.dex.UriSignature')
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
            mock_popen,
            mock_uri_signature,
            mock_shell_signature
    ):
        mock_popen.return_value = any_popen(b"any-string\nany-url\nany-command")
        mock_uri_signature.return_value = self.any_signature(matches=[None, "any-url", None])
        mock_shell_signature.return_value = self.any_signature(matches=[None, None, "any-command"])
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
        self.assertEqual(["any-command", "any-string", "any-url"], dex.get_strings())
        self.assertEqual(["any-url"], dex.get_urls())
        self.assertEqual(["any-command"], dex.get_shell_commands())
        self.assertEqual([], dex.get_custom_signatures())

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

    @patch('ninjadroid.parsers.dex.Popen')
    def test_extract_strings(self, mock_popen):
        mock_popen.return_value = any_popen(b"1-any-string\n2-any-other-string\n0-yet-another-string")

        strings = Dex._extract_strings("any-file-path")

        assert_popen_called_once_with(mock_popen, "strings any-file-path")
        # NOTE: the strings are returned alphabetically ordered
        self.assertEqual(
            [
                "0-yet-another-string",
                "1-any-string",
                "2-any-other-string",
            ],
            strings
        )

    def test_extract_signatures(self):
        mock_signature = Mock()
        mock_signature.search.side_effect = ["any-match-1", None, "", "any-match-2", "any-match-0"]

        urls = Dex._extract_signatures(
            signature=mock_signature,
            strings=[
                "any-match-1",
                "any-non-match",
                "any-empty-match",
                "any-match-2",
                "any-match-0"
            ]
        )

        mock_signature.search.assert_has_calls([
            call("any-match-1"),
            call("any-non-match"),
            call("any-empty-match"),
            call("any-match-2"),
            call("any-match-0")
        ])
        # NOTE: the signatures are returned alphabetically ordered
        self.assertEqual(["any-match-0", "any-match-1", "any-match-2"], urls)

    def test_extract_signatures_with_min_string_len(self):
        mock_signature = Mock()
        mock_signature.search.return_value = "any-match"

        signatures = Dex._extract_signatures(
            signature=mock_signature,
            strings=[
                "any-match",
                "nop"  # NOTE: this string is too short and will be filtered before calling Signature.search()
             ],
            min_string_len=6
        )

        mock_signature.search.assert_has_calls([call("any-match")])
        self.assertEqual(["any-match"], signatures)

    def test_extract_signatures_when_no_match_is_found(self):
        mock_signature = Mock()
        mock_signature.search.return_value = None

        signatures = Dex._extract_signatures(signature=mock_signature, strings=["any-non-match"])

        mock_signature.search.assert_called_with("any-non-match")
        self.assertEqual([], signatures)

    def test_extract_signatures_when_no_string_is_passed(self):
        mock_signature = Mock()

        urls = Dex._extract_signatures(signature=mock_signature, strings=[])

        mock_signature.search.assert_not_called()
        self.assertEqual([], urls)

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
