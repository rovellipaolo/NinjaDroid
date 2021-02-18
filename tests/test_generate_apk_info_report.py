import unittest
from unittest.mock import mock_open, patch

from ninjadroid.use_cases.generate_apk_info_report import GenerateApkInfoReport


class TestGenerateApkInfoReport(unittest.TestCase):
    """
    UnitTest for generate_apk_info_report.py.

    RUN: python -m unittest -v tests.test_generate_apk_info_report
    """

    ANY_FILE = "any-file"
    ANY_DIRECTORY = "any-directory"
    ANY_JSON_PATH = "any-json-path"
    ANY_JSON_REPORT = "any-json-report"
    ANY_APK_DUMP = { "any-key": "any-value" }

    sut = GenerateApkInfoReport()

    @patch('ninjadroid.use_cases.generate_apk_info_report.json')
    @patch('ninjadroid.parsers.apk')
    @patch('ninjadroid.use_cases.generate_apk_info_report.os')
    @patch("builtins.open", new_callable=mock_open)
    def test_execute(self, mock_file, mock_os, mock_apk, mock_json):
        mock_os.path.join.return_value = TestGenerateApkInfoReport.ANY_JSON_PATH
        mock_apk.dump.return_value = TestGenerateApkInfoReport.ANY_APK_DUMP
        mock_json.dumps.return_value = TestGenerateApkInfoReport.ANY_JSON_REPORT

        self.sut.execute(
            apk=mock_apk,
            input_filename=TestGenerateApkInfoReport.ANY_FILE,
            output_directory=TestGenerateApkInfoReport.ANY_DIRECTORY
        )

        mock_json.dumps.assert_called_once_with(
            TestGenerateApkInfoReport.ANY_APK_DUMP,
            sort_keys=True,
            ensure_ascii=False,
            indent=4
        )
        mock_file.assert_called_with(TestGenerateApkInfoReport.ANY_JSON_PATH, "w")
        mock_file().write.assert_called_once_with(TestGenerateApkInfoReport.ANY_JSON_REPORT)


if __name__ == "__main__":
    unittest.main()
