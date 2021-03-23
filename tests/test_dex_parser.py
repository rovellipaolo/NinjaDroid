import unittest
from unittest.mock import call, Mock, patch
from typing import List
from parameterized import parameterized
from tests.utils.file import any_file, any_file_parser, any_file_parser_failure, assert_file_equal, \
    assert_file_parser_called_once_with
from tests.utils.popen import any_popen, assert_popen_called_once_with

from ninjadroid.parsers.dex import DexParser
from ninjadroid.parsers.file import FileParsingError


class TestDexParser(unittest.TestCase):
    """
    Test Dex parser.
    """

    sut = DexParser()

    @staticmethod
    def any_signature(matches: List):
        signature = Mock()
        signature.search.side_effect = matches
        return signature

    @patch('ninjadroid.parsers.dex.ShellSignature')
    @patch('ninjadroid.parsers.dex.UriSignature')
    @patch('ninjadroid.parsers.dex.Popen')
    @patch('ninjadroid.parsers.dex.FileParser')
    def test_parse(self, mock_file_parser, mock_popen, mock_uri_signature, mock_shell_signature):
        file = any_file()
        mock_parser_instance = any_file_parser(file=file)
        mock_file_parser.return_value = mock_parser_instance
        mock_popen.return_value = any_popen(b"any-string\nany-url\nany-command")
        mock_uri_signature.return_value = self.any_signature(matches=[
            (None, False),
            ("any-url", True),
            (None, False)
        ])
        mock_shell_signature.return_value = self.any_signature(matches=[
            (None, False),
            (None, False),
            ("any-command", True)
        ])

        dex = DexParser().parse("any-file-path", "any-file-name")

        assert_file_parser_called_once_with(mock_parser_instance, filepath="any-file-path", filename="any-file-name")
        assert_popen_called_once_with(mock_popen, "strings any-file-path")
        assert_file_equal(self, expected=file, actual=dex)
        self.assertEqual(["any-command", "any-string", "any-url"], dex.get_strings())
        self.assertEqual(["any-url"], dex.get_urls())
        self.assertEqual(["any-command"], dex.get_shell_commands())
        self.assertEqual([], dex.get_custom_signatures())

    @patch('ninjadroid.parsers.dex.Popen')
    @patch('ninjadroid.parsers.dex.FileParser')
    def test_parse_fails_when_file_parser_fails(self, mock_file_parser, mock_popen):
        mock_parser_instance = any_file_parser_failure()
        mock_file_parser.return_value = mock_parser_instance

        with self.assertRaises(FileParsingError):
            self.sut.parse("any-file-path", "any-file-name")
        assert_file_parser_called_once_with(mock_parser_instance, filepath="any-file-path", filename="any-file-name")
        mock_popen.assert_not_called()

    @patch('ninjadroid.parsers.dex.Popen')
    def test_parse_strings(self, mock_popen):
        mock_popen.return_value = any_popen(b"1-any-string\n2-any-other-string\n0-yet-another-string")

        strings = DexParser.parse_strings("any-file-path")

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

    def test_parse_signatures(self):
        mock_signature = Mock()
        mock_signature.search.side_effect = [
            ("any-match-1", True),
            (None, False),
            ("", True),
            ("any-match-2", True),
            ("any-match-0", True)
        ]

        urls = DexParser.parse_signatures(
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

    def test_parse_signatures_with_min_string_len(self):
        mock_signature = Mock()
        mock_signature.search.return_value = ("any-match", True)

        signatures = DexParser.parse_signatures(
            signature=mock_signature,
            strings=[
                "any-match",
                "nop"  # NOTE: this string is too short and will be filtered before calling Signature.search()
             ],
            min_string_len=6
        )

        mock_signature.search.assert_has_calls([call("any-match")])
        self.assertEqual(["any-match"], signatures)

    def test_parse_signatures_when_no_match_is_found(self):
        mock_signature = Mock()
        mock_signature.search.return_value = (None, False)

        signatures = DexParser.parse_signatures(signature=mock_signature, strings=["any-non-match"])

        mock_signature.search.assert_called_with("any-non-match")
        self.assertEqual([], signatures)

    def test_parse_signatures_when_empty_match_is_found(self):
        mock_signature = Mock()
        mock_signature.search.return_value = ("", True)

        signatures = DexParser.parse_signatures(signature=mock_signature, strings=["any-empty-match"])

        mock_signature.search.assert_called_with("any-empty-match")
        self.assertEqual([], signatures)

    def test_parse_signatures_when_no_string_is_passed(self):
        mock_signature = Mock()

        urls = DexParser.parse_signatures(signature=mock_signature, strings=[])

        mock_signature.search.assert_not_called()
        self.assertEqual([], urls)

    @parameterized.expand([
        ["classes.dex", True],
        ["whatever.dex", True],
        ["AndroidManifest.xml", False],
        ["META-INF/CERT.RSA", False],
        ["Example.apk", False]
    ])
    def test_looks_like_dex(self, filename, expected):
        result = DexParser.looks_like_dex(filename)

        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
