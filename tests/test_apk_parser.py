from typing import List
import unittest
from unittest.mock import Mock, patch
from zipfile import BadZipFile
from parameterized import parameterized

from ninjadroid.parsers.apk import APK, ApkParser, ApkParsingError
from ninjadroid.parsers.cert import CertParsingError
from ninjadroid.parsers.manifest import AndroidManifestParsingError
from ninjadroid.parsers.file import File, FileParsingError
from tests.utils.file import any_file, assert_file_equal


# pylint: disable=too-many-arguments,too-many-locals
class TestApkParser(unittest.TestCase):
    """
    Test APK parser.
    """

    def assert_apk_equal(
            self,
            apk: APK,
            app_name: str,
            manifest: File,
            cert: File,
            dex_files: List[File],
            other_files: List[File]
    ):
        self.assertEqual(app_name, apk.get_app_name())
        self.assertEqual(manifest, apk.get_manifest())
        self.assertEqual(cert, apk.get_cert())
        self.assertEqual(dex_files, apk.get_dex_files())
        self.assertEqual(other_files, apk.get_other_files())

    @patch('ninjadroid.parsers.apk.Aapt')
    @patch('ninjadroid.parsers.apk.DexParser')
    @patch('ninjadroid.parsers.apk.CertParser')
    @patch('ninjadroid.parsers.apk.AndroidManifestParser')
    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse(
            self,
            mock_zipfile,
            mock_mkdtemp,
            mock_rmtree,
            mock_file_parser,
            mock_manifest_parser,
            mock_cert_parser,
            mock_dex_parser,
            mock_aapt
    ):
        file = any_file(filename="any-apk-file")
        manifest = any_file(filename="any-manifest-file-name")
        cert = any_file(filename="any-cert-file-name")
        dex = any_file(filename="any-dex-file-name")
        resource = any_file(filename="any-resource-file")
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = [
            "any-manifest-file-name",
            "any-cert-file-name",
            "any-dex-file-name",
            "any-resource-file",
            "any-resource-directory"
        ]
        tmp_directory = Mock()
        mock_mkdtemp.return_value = tmp_directory
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.is_directory.side_effect = [False, True]
        mock_file_parser.return_value.parse.side_effect = [file, cert, dex, resource]
        mock_manifest_parser.looks_like_manifest.side_effect = [True, False, False, False, False]
        mock_manifest_parser.return_value.parse.return_value = manifest
        mock_cert_parser.looks_like_cert.side_effect = [True, False, False, False]
        mock_dex_parser.looks_like_dex.side_effect = [True, False, False]
        mock_aapt.get_app_name.return_value = "any-app-name"

        apk = ApkParser().parse("any-file-path", extended_processing=False)

        mock_mkdtemp.assert_called_with(".ninjadroid")
        mock_zipfile.assert_called_with("any-file-path")
        mock_rmtree.assert_called_with(tmp_directory)
        assert_file_equal(self, expected=file, actual=apk)
        self.assert_apk_equal(
            apk=apk,
            app_name="any-app-name",
            manifest=manifest,
            cert=cert,
            dex_files=[dex],
            other_files=[]
        )

    @patch('ninjadroid.parsers.apk.Aapt')
    @patch('ninjadroid.parsers.apk.DexParser')
    @patch('ninjadroid.parsers.apk.CertParser')
    @patch('ninjadroid.parsers.apk.AndroidManifestParser')
    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse_with_extended_processing(
            self,
            mock_zipfile,
            mock_mkdtemp,
            mock_rmtree,
            mock_file_parser,
            mock_manifest_parser,
            mock_cert_parser,
            mock_dex_parser,
            mock_aapt
    ):
        tmp_directory = Mock()
        file = any_file(filename="any-apk-file")
        manifest = any_file(filename="any-manifest-file-name")
        cert = any_file(filename="any-cert-file-name")
        dex = any_file(filename="any-dex-file-name")
        resource = any_file(filename="any-resource-file")
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = [
            "any-manifest-file-name",
            "any-cert-file-name",
            "any-dex-file-name",
            "any-resource-file",
            "any-resource-directory"
        ]
        mock_mkdtemp.return_value = tmp_directory
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.is_directory.side_effect = [False, True]
        mock_file_parser.return_value.parse.side_effect = [file, resource]
        mock_manifest_parser.looks_like_manifest.side_effect = [True, False, False, False, False]
        mock_manifest_parser.return_value.parse.return_value = manifest
        mock_cert_parser.looks_like_cert.side_effect = [True, False, False, False]
        mock_cert_parser.return_value.parse.return_value = cert
        mock_dex_parser.looks_like_dex.side_effect = [True, False, False]
        mock_dex_parser.return_value.parse.return_value = dex
        mock_aapt.get_app_name.return_value = "any-app-name"

        apk = ApkParser().parse("any-file-path", extended_processing=True)

        mock_mkdtemp.assert_called_with(".ninjadroid")
        mock_zipfile.assert_called_with("any-file-path")
        mock_rmtree.assert_called_with(tmp_directory)
        assert_file_equal(self, expected=file, actual=apk)
        self.assert_apk_equal(
            apk=apk,
            app_name="any-app-name",
            manifest=manifest,
            cert=cert,
            dex_files=[dex],
            other_files=[resource]
        )

    @patch('ninjadroid.parsers.apk.Aapt')
    @patch('ninjadroid.parsers.apk.DexParser')
    @patch('ninjadroid.parsers.apk.CertParser')
    @patch('ninjadroid.parsers.apk.AndroidManifestParser')
    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse_when_rmtree_fails(
            self,
            mock_zipfile,
            mock_mkdtemp,
            mock_rmtree,
            mock_file_parser,
            mock_manifest_parser,
            mock_cert_parser,
            mock_dex_parser,
            mock_aapt
    ):
        file = any_file(filename="any-apk-file")
        manifest = any_file(filename="any-manifest-file-name")
        cert = any_file(filename="any-cert-file-name")
        dex = any_file(filename="any-dex-file-name")
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = [
            "any-manifest-file-name",
            "any-cert-file-name",
            "any-dex-file-name"
        ]
        tmp_directory = Mock()
        mock_mkdtemp.return_value = tmp_directory
        mock_rmtree.side_effect = OSError()
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.return_value.parse.side_effect = [file, cert, dex]
        mock_manifest_parser.looks_like_manifest.side_effect = [True, False, False]
        mock_manifest_parser.return_value.parse.return_value = manifest
        mock_cert_parser.looks_like_cert.side_effect = [True, False]
        mock_aapt.get_app_name.return_value = "any-app-name"
        mock_dex_parser.looks_like_dex.side_effect = [True]

        apk = ApkParser().parse("any-file-path", extended_processing=False)

        mock_mkdtemp.assert_called_with(".ninjadroid")
        mock_zipfile.assert_called_with("any-file-path")
        mock_rmtree.assert_called_with(tmp_directory)
        assert_file_equal(self, expected=file, actual=apk)
        self.assert_apk_equal(
            apk=apk,
            app_name="any-app-name",
            manifest=manifest,
            cert=cert,
            dex_files=[dex],
            other_files=[]
        )

    @patch('ninjadroid.parsers.apk.AndroidManifestParser')
    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse_when_manifest_parser_fails(
            self,
            mock_zipfile,
            mock_mkdtemp,
            mock_rmtree,
            mock_file_parser,
            mock_manifest_parser
    ):
        file = any_file(filename="any-apk-file")
        cert = any_file(filename="any-cert-file-name")
        dex = any_file(filename="any-dex-file-name")
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = [
            "any-manifest-file-name",
            "any-cert-file-name",
            "any-dex-file-name"
        ]
        tmp_directory = Mock()
        mock_mkdtemp.return_value = tmp_directory
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.return_value.parse.side_effect = [file, cert, dex]
        mock_manifest_parser.looks_like_manifest.side_effect = [True]
        mock_manifest_parser.return_value.parse.side_effect = AndroidManifestParsingError()

        with self.assertRaises(ApkParsingError):
            ApkParser().parse("any-file-path", extended_processing=False)
        mock_rmtree.assert_called_with(tmp_directory)

    @patch('ninjadroid.parsers.apk.CertParser')
    @patch('ninjadroid.parsers.apk.AndroidManifestParser')
    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse_when_cert_parser_fails(
            self,
            mock_zipfile,
            mock_mkdtemp,
            mock_rmtree,
            mock_file_parser,
            mock_manifest_parser,
            mock_cert_parser
    ):
        file = any_file(filename="any-apk-file")
        manifest = any_file(filename="any-manifest-file-name")
        cert = any_file(filename="any-cert-file-name")
        dex = any_file(filename="any-dex-file-name")
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = [
            "any-manifest-file-name",
            "any-cert-file-name",
            "any-dex-file-name"
        ]
        tmp_directory = Mock()
        mock_mkdtemp.return_value = tmp_directory
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.return_value.parse.side_effect = [file, cert, dex]
        mock_manifest_parser.looks_like_manifest.side_effect = [True, False]
        mock_manifest_parser.return_value.parse.return_value = manifest
        mock_cert_parser.looks_like_cert.side_effect = [True]
        mock_cert_parser.return_value.parse.side_effect = CertParsingError()

        with self.assertRaises(ApkParsingError):
            ApkParser().parse("any-file-path", extended_processing=True)
        mock_rmtree.assert_called_with(tmp_directory)

    @patch('ninjadroid.parsers.apk.DexParser')
    @patch('ninjadroid.parsers.apk.CertParser')
    @patch('ninjadroid.parsers.apk.AndroidManifestParser')
    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse_when_dex_parser_fails(
            self,
            mock_zipfile,
            mock_mkdtemp,
            mock_rmtree,
            mock_file_parser,
            mock_manifest_parser,
            mock_cert_parser,
            mock_dex_parser
    ):
        tmp_directory = Mock()
        file = any_file(filename="any-apk-file")
        manifest = any_file(filename="any-manifest-file-name")
        cert = any_file(filename="any-cert-file-name")
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = [
            "any-manifest-file-name",
            "any-cert-file-name",
            "any-dex-file-name"
        ]
        mock_mkdtemp.return_value = tmp_directory
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.return_value.parse.return_value = file
        mock_manifest_parser.looks_like_manifest.side_effect = [True, False, False]
        mock_manifest_parser.return_value.parse.return_value = manifest
        mock_cert_parser.looks_like_cert.side_effect = [True, False]
        mock_cert_parser.return_value.parse.return_value = cert
        mock_dex_parser.looks_like_dex.side_effect = [True]
        mock_dex_parser.return_value.parse.side_effect = FileParsingError()

        with self.assertRaises(ApkParsingError):
            ApkParser().parse("any-file-path", extended_processing=True)
        mock_rmtree.assert_called_with(tmp_directory)

    @patch('ninjadroid.parsers.apk.Aapt')
    @patch('ninjadroid.parsers.apk.DexParser')
    @patch('ninjadroid.parsers.apk.CertParser')
    @patch('ninjadroid.parsers.apk.AndroidManifestParser')
    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse_when_file_parser_fails(
            self,
            mock_zipfile,
            mock_mkdtemp,
            mock_rmtree,
            mock_file_parser,
            mock_manifest_parser,
            mock_cert_parser,
            mock_dex_parser,
            mock_aapt
    ):
        tmp_directory = Mock()
        file = any_file(filename="any-apk-file")
        manifest = any_file(filename="any-manifest-file-name")
        cert = any_file(filename="any-cert-file-name")
        dex = any_file(filename="any-dex-file-name")
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = [
            "any-manifest-file-name",
            "any-cert-file-name",
            "any-dex-file-name",
            "any-resource-file"
        ]
        mock_mkdtemp.return_value = tmp_directory
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.is_directory.return_value = False
        mock_file_parser.return_value.parse.side_effect = [file, FileParsingError()]
        mock_manifest_parser.looks_like_manifest.side_effect = [True, False, False, False]
        mock_manifest_parser.return_value.parse.return_value = manifest
        mock_cert_parser.looks_like_cert.side_effect = [True, False, False]
        mock_cert_parser.return_value.parse.return_value = cert
        mock_dex_parser.looks_like_dex.side_effect = [True, False]
        mock_dex_parser.return_value.parse.return_value = dex
        mock_aapt.get_app_name.return_value = "any-app-name"

        apk = ApkParser().parse("any-file-path", extended_processing=True)

        mock_mkdtemp.assert_called_with(".ninjadroid")
        mock_zipfile.assert_called_with("any-file-path")
        mock_rmtree.assert_called_with(tmp_directory)
        assert_file_equal(self, expected=file, actual=apk)
        self.assert_apk_equal(
            apk=apk,
            app_name="any-app-name",
            manifest=manifest,
            cert=cert,
            dex_files=[dex],
            other_files=[]
        )

    @patch('ninjadroid.parsers.apk.DexParser')
    @patch('ninjadroid.parsers.apk.CertParser')
    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse_when_manifest_not_present(
            self,
            mock_zipfile,
            mock_mkdtemp,
            mock_rmtree,
            mock_file_parser,
            mock_cert_parser,
            mock_dex_parser
    ):
        file = any_file(filename="any-apk-file")
        cert = any_file(filename="any-cert-file-name")
        dex = any_file(filename="any-dex-file-name")
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = [
            "any-cert-file-name",
            "any-dex-file-name"
        ]
        tmp_directory = Mock()
        mock_mkdtemp.return_value = tmp_directory
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.return_value.parse.side_effect = [file, cert, dex]
        mock_cert_parser.looks_like_cert.side_effect = [True, False]
        mock_dex_parser.looks_like_dex.side_effect = [True]

        with self.assertRaises(ApkParsingError):
            ApkParser().parse("any-file-path", extended_processing=False)
        mock_rmtree.assert_called_with(tmp_directory)

    @patch('ninjadroid.parsers.apk.DexParser')
    @patch('ninjadroid.parsers.apk.AndroidManifestParser')
    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse_when_cert_not_present(
            self,
            mock_zipfile,
            mock_mkdtemp,
            mock_rmtree,
            mock_file_parser,
            mock_manifest_parser,
            mock_dex_parser
    ):
        file = any_file(filename="any-apk-file")
        manifest = any_file(filename="any-manifest-file-name")
        dex = any_file(filename="any-dex-file-name")
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = [
            "any-manifest-file-name",
            "any-dex-file-name"
        ]
        tmp_directory = Mock()
        mock_mkdtemp.return_value = tmp_directory
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.return_value.parse.side_effect = [file, dex]
        mock_manifest_parser.looks_like_manifest.side_effect = [True, False]
        mock_manifest_parser.return_value.parse.return_value = manifest
        mock_dex_parser.looks_like_dex.side_effect = [True]

        with self.assertRaises(ApkParsingError):
            ApkParser().parse("any-file-path", extended_processing=False)
        mock_rmtree.assert_called_with(tmp_directory)

    @patch('ninjadroid.parsers.apk.CertParser')
    @patch('ninjadroid.parsers.apk.AndroidManifestParser')
    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse_when_dex_not_present(
            self,
            mock_zipfile,
            mock_mkdtemp,
            mock_rmtree,
            mock_file_parser,
            mock_manifest_parser,
            mock_cert_parser
    ):
        file = any_file(filename="any-apk-file")
        manifest = any_file(filename="any-manifest-file-name")
        cert = any_file(filename="any-cert-file-name")
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = [
            "any-manifest-file-name",
            "any-cert-file-name"
        ]
        tmp_directory = Mock()
        mock_mkdtemp.return_value = tmp_directory
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.return_value.parse.side_effect = [file, cert]
        mock_manifest_parser.looks_like_manifest.side_effect = [True, False]
        mock_manifest_parser.return_value.parse.return_value = manifest
        mock_cert_parser.looks_like_cert.side_effect = [True]

        with self.assertRaises(ApkParsingError):
            ApkParser().parse("any-file-path", extended_processing=False)
        mock_rmtree.assert_called_with(tmp_directory)

    @patch('ninjadroid.parsers.apk.rmtree')
    @patch('ninjadroid.parsers.apk.mkdtemp')
    @patch('ninjadroid.parsers.apk.ZipFile')
    @patch('ninjadroid.parsers.apk.FileParser')
    def test_parse_when_no_file_present(self, mock_file_parser, mock_zipfile, mock_mkdtemp, mock_rmtree):
        tmp_directory = Mock()
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.return_value.parse.return_value = any_file()
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = []
        mock_mkdtemp.return_value = tmp_directory

        with self.assertRaises(ApkParsingError):
            ApkParser().parse("any-file-path", extended_processing=False)
        mock_rmtree.assert_called_with(tmp_directory)

    @patch('ninjadroid.parsers.apk.FileParser')
    @patch('ninjadroid.parsers.apk.ZipFile')
    def test_parse_when_zipfile_fails(self, mock_file_parser, mock_zipfile):
        mock_file_parser.is_zip_file.return_value = True
        mock_file_parser.return_value.parse.return_value = any_file()
        mock_zipfile.side_effect = BadZipFile()

        with self.assertRaises(BadZipFile):
            ApkParser().parse("any-file-path", extended_processing=False)

    @parameterized.expand([
        ["Example.apk", True],
        ["AndroidManifest.xml", False],
        ["META-INF/CERT.RSA", False],
        ["classes.dex", False]
    ])
    @patch('ninjadroid.parsers.apk.FileParser')
    def test_looks_like_apk(self, filename, expected, mock_file_parser):
        mock_file_parser.is_zip_file.return_value = expected

        result = ApkParser.looks_like_apk(filename)

        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
