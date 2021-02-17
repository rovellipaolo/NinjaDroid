import unittest
from unittest.mock import patch

from ninjadroid.use_cases.print_apk_info import PrintApkInfo


class TestPrintApkInfo(unittest.TestCase):
    """
    UnitTest for print_apk_info.py.

    RUN: python -m unittest -v tests.test_print_apk_info
    """

    ANY_JSON_REPORT = "any-json-report"
    ANY_APK_DUMP = { "any-key": "any-value" }

    sut = PrintApkInfo()

    @patch('ninjadroid.use_cases.print_apk_info.json')
    @patch('ninjadroid.parsers.apk')
    def test_execute(self, mock_apk, mock_json):
        mock_apk.dump.return_value = TestPrintApkInfo.ANY_APK_DUMP
        mock_json.dumps.return_value = TestPrintApkInfo.ANY_JSON_REPORT

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


if __name__ == "__main__":
    unittest.main()
