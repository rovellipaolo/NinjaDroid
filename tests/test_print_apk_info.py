import unittest
from unittest.mock import patch
from parameterized import parameterized

from ninjadroid.use_cases.print_apk_info import PrintApkInfo


class TestPrintApkInfo(unittest.TestCase):
    """
    UnitTest for print_apk_info.py.

    RUN: python -m unittest -v tests.test_print_apk_info
    """

    ANY_JSON_REPORT = "any-json-report"
    ANY_APK_DUMP = {
        "any-key": "any-value",
        "any-dict-key": {
            "any-dict-internal-key": "any-dict-internal-value"
        },
        "any-list-key": [
            "any-list-internal-value",
            "any-other-list-internal-value"
        ]
    }

    sut = PrintApkInfo()

    @patch('ninjadroid.use_cases.print_apk_info.json')
    @patch('ninjadroid.parsers.apk')
    def test_execute(self, mock_apk, mock_json):
        mock_apk.dump.return_value = TestPrintApkInfo.ANY_APK_DUMP

        self.sut.execute(
            apk=mock_apk,
            as_json=False
        )

        mock_apk.dump.assert_called_once_with()
        mock_json.dumps.assert_not_called()

    @patch('ninjadroid.use_cases.print_apk_info.json')
    @patch('ninjadroid.parsers.apk')
    def test_execute_as_json(self, mock_apk, mock_json):
        mock_apk.dump.return_value = TestPrintApkInfo.ANY_APK_DUMP
        mock_json.dumps.return_value = TestPrintApkInfo.ANY_JSON_REPORT

        self.sut.execute(
            apk=mock_apk,
            as_json=True
        )

        mock_apk.dump.assert_called_once_with()
        mock_json.dumps.assert_called_once_with(
            TestPrintApkInfo.ANY_APK_DUMP,
            sort_keys=True,
            ensure_ascii=False,
            indent=4
        )

    @parameterized.expand([
        [None, None, 0, "- None"],
        [None, None, 1, "\t- None"],
        [None, None, 2, "\t\t- None"],
        [None, "value", 0, "- value"],
        [None, "value", 1, "\t- value"],
        [None, "value", 2, "\t\t- value"],
        ["key", None, 0, "key:"],
        ["key", None, 1, "\tkey:"],
        ["key", None, 2, "\t\tkey:"],
        ["key", "value", 0, "key:     value"],
        ["key", "value", 1, "\tkey:    value"],
        ["key", "value", 2, "\t\tkey:   value"],
    ])
    def test_format_value(self, key, value, depth, expected):
        result = PrintApkInfo.format_value(key=key, value=value, depth=depth)

        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
