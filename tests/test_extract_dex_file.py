import unittest
from unittest.mock import Mock, mock_open, patch

from ninjadroid.use_cases.extract_dex_file import ExtractDexFile


# pylint: disable=too-many-arguments
class TestExtractDexFile(unittest.TestCase):
    """
    Test ExtractDexFile use case.
    """

    ANY_APK_FILE = "any-apk-file"
    ANY_DEX_FILE = "any-dex-file"
    ANY_DEX_PATH = "any-dex-path"
    ANY_DIRECTORY = "any-directory"
    ANY_OUTPUT_DIRECTORY = "any-output-directory"

    sut = ExtractDexFile()

    @patch('ninjadroid.parsers.apk')
    @patch('ninjadroid.use_cases.extract_dex_file.shutil')
    @patch('ninjadroid.use_cases.extract_dex_file.ZipFile')
    @patch('ninjadroid.use_cases.extract_dex_file.os')
    @patch("builtins.open", new_callable=mock_open)
    def test_execute(self, mock_file, mock_os, mock_zip, mock_shutil, mock_apk):
        mock_apk.get_file_name.return_value = TestExtractDexFile.ANY_APK_FILE
        mock_apk.get_dex_files.return_value = [self.mock_dex(TestExtractDexFile.ANY_DEX_FILE)]
        mock_zip.returnValue = self.mock_package()
        mock_os.path.join.return_value = TestExtractDexFile.ANY_DEX_PATH
        mock_os.path.split.return_value = [TestExtractDexFile.ANY_OUTPUT_DIRECTORY]

        self.sut.execute(apk=mock_apk, output_directory=TestExtractDexFile.ANY_DIRECTORY)

        mock_zip.assert_called_once_with(TestExtractDexFile.ANY_APK_FILE)
        mock_os.path.join.assert_called_once_with(TestExtractDexFile.ANY_DIRECTORY, TestExtractDexFile.ANY_DEX_FILE)
        mock_os.path.split.assert_called_once_with(TestExtractDexFile.ANY_DEX_PATH)
        mock_file.assert_called_with(TestExtractDexFile.ANY_DEX_PATH, "wb")
        mock_shutil.copyfileobj.assert_called_once_with(mock_zip().__enter__().open().__enter__(), mock_file())

    @staticmethod
    def mock_dex(filename: str):
        mock_dex = Mock()
        mock_dex.get_file_name.return_value = filename
        return mock_dex

    @staticmethod
    def mock_package():
        mock_package = Mock()
        mock_package.open.returnValue = Mock()
        return mock_package


if __name__ == "__main__":
    unittest.main()
