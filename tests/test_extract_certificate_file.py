import unittest
from unittest.mock import Mock, mock_open, patch

from ninjadroid.use_cases.extract_certificate_file import ExtractCertificateFile


class TestExtractCertificateFile(unittest.TestCase):
    """
    UnitTest for extract_certificate_file.py.

    RUN: python -m unittest -v tests.test_extract_certificate_file
    """

    ANY_APK_FILE = "any-apk-file"
    ANY_CERT_NAME = "any-cert-name"
    ANY_CERT_FILE = "any-cert-file"
    ANY_CERT_PATH = "any-cert-path"
    ANY_DIRECTORY = "any-directory"

    sut = ExtractCertificateFile()

    @patch('ninjadroid.parsers.apk')
    @patch('ninjadroid.use_cases.extract_certificate_file.shutil')
    @patch('ninjadroid.use_cases.extract_certificate_file.ZipFile')
    @patch('ninjadroid.use_cases.extract_certificate_file.os')
    @patch("builtins.open", new_callable=mock_open)
    def test_execute(self, mock_file, mock_os, mock_zip, mock_shutil, mock_apk):
        mock_apk.get_file_name.return_value = TestExtractCertificateFile.ANY_APK_FILE
        mock_apk.get_cert.return_value = self.mock_cert(TestExtractCertificateFile.ANY_CERT_FILE)
        mock_zip.returnValue = self.mock_package()
        mock_os.path.basename.return_value = TestExtractCertificateFile.ANY_CERT_NAME
        mock_os.path.join.return_value = TestExtractCertificateFile.ANY_CERT_PATH
        mock_open.return_value = Mock()

        self.sut.execute(apk=mock_apk, output_directory=TestExtractCertificateFile.ANY_DIRECTORY)

        mock_zip.assert_called_once_with(TestExtractCertificateFile.ANY_APK_FILE)
        mock_os.path.join.assert_called_once_with(
            TestExtractCertificateFile.ANY_DIRECTORY,
            TestExtractCertificateFile.ANY_CERT_NAME
        )
        mock_file.assert_called_with(TestExtractCertificateFile.ANY_CERT_PATH, "wb")
        mock_shutil.copyfileobj.assert_called_once_with(mock_zip().__enter__().open().__enter__(), mock_file())

    @staticmethod
    def mock_cert(filename: str):
        mock_cert = Mock()
        mock_cert.get_file_name.return_value = filename
        return mock_cert

    @staticmethod
    def mock_package():
        mock_package = Mock()
        mock_package.open.returnValue = Mock()
        return mock_package


if __name__ == "__main__":
    unittest.main()
