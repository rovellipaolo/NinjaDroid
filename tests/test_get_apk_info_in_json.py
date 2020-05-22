import unittest
from unittest.mock import Mock, mock_open, patch

from ninjadroid.use_cases.get_apk_info_in_json import GetApkInfoInJson


class TestGetApkInfoInJson(unittest.TestCase):
    """
    UnitTest for get_apk_info_in_json.py.

    RUN: python -m unittest -v tests.test_get_apk_info_in_json
    """

    ANY_FILE = "any-file"
    ANY_DIRECTORY = "any-directory"
    ANY_JSON_PATH = "any-json-path"
    ANY_JSON_REPORT = "any-json-report"
    ANY_APK_DUMP = "any-apk-dump"

    sut = GetApkInfoInJson()

    @patch('ninjadroid.use_cases.get_apk_info_in_json.json')
    @patch('ninjadroid.parsers.apk')
    @patch('ninjadroid.use_cases.get_apk_info_in_json.os')
    @patch("builtins.open", new_callable=mock_open)
    def test_execute(self, mock_file, mock_os, mock_apk, mock_json):
        mock_os.path.join.return_value = TestGetApkInfoInJson.ANY_JSON_PATH
        mock_apk.dump.return_value = TestGetApkInfoInJson.ANY_APK_DUMP
        mock_json.dumps.return_value = TestGetApkInfoInJson.ANY_JSON_REPORT

        self.sut.execute(
            apk=mock_apk,
            input_filename=TestGetApkInfoInJson.ANY_FILE,
            output_directory=TestGetApkInfoInJson.ANY_DIRECTORY
        )

        mock_json.dumps.assert_called_once_with(
            TestGetApkInfoInJson.ANY_APK_DUMP,
            sort_keys=True,
            ensure_ascii=False,
            indent=4
        )
        mock_file.assert_called_with(TestGetApkInfoInJson.ANY_JSON_PATH, "w")
        mock_file().write.assert_called_once_with(TestGetApkInfoInJson.ANY_JSON_REPORT)


if __name__ == "__main__":
    unittest.main()
