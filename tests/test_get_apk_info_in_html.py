import unittest
from unittest.mock import Mock, mock_open, patch

from ninjadroid.use_cases.get_apk_info_in_html import GetApkInfoInHtml


class TestGetApkInfoInHtml(unittest.TestCase):
    """
    UnitTest for get_apk_info_in_html.py.

    RUN: python -m unittest -v tests.test_get_apk_info_in_html
    """

    ANY_APK_FILE = "any-apk-file"
    ANY_APK_MD5 = "any-apk-md5"
    ANY_APK_SHA1 = "any-apk-sha1"
    ANY_APK_SHA256 = "any-apk-sha256"
    ANY_APK_SHA512 = "any-apk-sha512"
    ANY_FILE = "any-file"
    ANY_DIRECTORY = "any-directory"
    ANY_HTML_PATH = "any-html-path"
    ANY_HTML_REPORT = "any-html-report"

    sut = GetApkInfoInHtml()

    @patch('ninjadroid.parsers.apk')
    @patch('ninjadroid.use_cases.get_apk_info_in_html.os')
    @patch("builtins.open", new_callable=mock_open)
    def test_execute(self, mock_file, mock_os, mock_apk):
        mock_apk.get_file_name.return_value = TestGetApkInfoInHtml.ANY_APK_FILE
        mock_apk.get_md5.return_value = TestGetApkInfoInHtml.ANY_APK_MD5
        mock_apk.get_sha1.return_value = TestGetApkInfoInHtml.ANY_APK_SHA1
        mock_apk.get_sha256.return_value = TestGetApkInfoInHtml.ANY_APK_SHA256
        mock_apk.get_sha512.return_value = TestGetApkInfoInHtml.ANY_APK_SHA512
        mock_os.path.join.return_value = TestGetApkInfoInHtml.ANY_HTML_PATH

        self.sut.execute(
            apk=mock_apk,
            input_filename=TestGetApkInfoInHtml.ANY_FILE,
            output_directory=TestGetApkInfoInHtml.ANY_DIRECTORY
        )

        mock_file.assert_called_with(TestGetApkInfoInHtml.ANY_HTML_PATH, "w")
        #mock_file().write.assert_called_once()


if __name__ == "__main__":
    unittest.main()
