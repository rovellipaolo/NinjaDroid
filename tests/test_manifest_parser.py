from os.path import join
from parameterized import parameterized
from typing import Dict, List
import unittest
from unittest.mock import ANY, call, Mock, mock_open, patch
from tests.utils.file import any_file, any_file_parser, any_file_parser_failure, assert_file_equal, assert_file_parser_called_once_with
from xml.parsers.expat import ExpatError

from ninjadroid.parsers.file import FileParsingError
from ninjadroid.parsers.manifest import AndroidManifestParser, AndroidManifestParsingError, AppActivity, AppBroadcastReceiver, AppService, AppSdk, AppVersion


class TestAndroidManifestParser(unittest.TestCase):
    sut = AndroidManifestParser()

    @staticmethod
    def any_axmlprinter() -> Mock:
        axmlprinter = Mock()
        axmlprinter.get_buff.return_value = "any-axml-raw-value"
        return axmlprinter

    @staticmethod
    def any_aapt_apk_info(
        package_name: str,
        version_code: int,
        version_name: str,
        sdk_min: str,
        sdk_target: str,
        sdk_max: str
    ) -> Dict:
        return {
            "package_name": package_name,
            "version": {
                "code": version_code,
                "name": version_name
            },
            "sdk": {
                "min": sdk_min,
                "target": sdk_target,
                "max": sdk_max
            }
        }

    @staticmethod
    def any_aapt_manifest_info(activities: List[str], services: List[str], receivers: str) -> Dict:
        return {
            "activities": activities,
            "services": services,
            "receivers": receivers
        }

    @staticmethod
    def any_axmlprinter_xml(
            package_name: str,
            version_code: str,
            version_name: str,
            sdk_min: str,
            sdk_target: str,
            sdk_max: str,
            permissions: List[str]
    ) -> Mock:
        xml = Mock()
        xml.documentElement.getAttribute.side_effect = [
            package_name,
            version_code,
            version_name
        ]
        sdk_xml = Mock()
        sdk_xml.hasAttribute.return_value = True
        sdk_xml.getAttribute.side_effect = [
            sdk_min,
            sdk_target,
            sdk_max
        ]
        permissions_xml = Mock()
        permissions_xml.getAttribute.side_effect = permissions
        xml.documentElement.getElementsByTagName.side_effect = [
            [sdk_xml],
            [permissions_xml, permissions_xml, permissions_xml]
        ]
        return xml

    @patch('ninjadroid.parsers.manifest.minidom')
    @patch('ninjadroid.parsers.manifest.FileParser')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse(self, mock_file, mock_file_parser, mock_minidom):
        file = any_file(filename="AndroidManifest.xml")
        mock_parser_instance = any_file_parser(file=file)
        mock_file_parser.return_value = mock_parser_instance
        mock_minidom.parse.return_value = self.any_axmlprinter_xml(
            package_name="any-package-name",
            version_code="1",
            version_name="any-version-name",
            sdk_max="20",
            sdk_min="10",
            sdk_target="15",
            permissions=["any-permission-1", "any-permission-2", "any-permission-0"]
        )

        manifest = self.sut.parse(
            filepath="any-file-path",
            binary = False,
            apk_path = "any_apk_path",
            extended_processing = False
        )

        assert_file_parser_called_once_with(mock_parser_instance, filepath="any-file-path", filename="AndroidManifest.xml")
        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        assert_file_equal(self, expected=file, actual=manifest)
        self.assertEqual("any-package-name", manifest.get_package_name())
        self.assertEqual(AppVersion(code=1, name="any-version-name"), manifest.get_version())
        self.assertEqual(AppSdk(min_version="10", target_version="15", max_version="20"), manifest.get_sdk())
        self.assertEqual(["any-permission-0", "any-permission-1", "any-permission-2"], manifest.get_permissions())
        self.assertEqual([], manifest.get_activities())
        self.assertEqual([], manifest.get_services())
        self.assertEqual([], manifest.get_broadcast_receivers())

    @patch('ninjadroid.parsers.manifest.minidom')
    @patch('ninjadroid.parsers.manifest.FileParser')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_with_invalid_version_code(self, mock_file, mock_file_parser, mock_minidom):
        file = any_file(filename="AndroidManifest.xml")
        mock_parser_instance = any_file_parser(file=file)
        mock_file_parser.return_value = mock_parser_instance
        mock_minidom.parse.return_value = self.any_axmlprinter_xml(
            package_name="any-package-name",
            version_code="A",
            version_name="any-version-name",
            sdk_max="20",
            sdk_min="10",
            sdk_target="15",
            permissions=["any-permission-1", "any-permission-2", "any-permission-0"]
        )

        manifest = self.sut.parse(
            filepath="any-file-path",
            binary = False,
            apk_path = "any_apk_path",
            extended_processing = False
        )

        assert_file_parser_called_once_with(mock_parser_instance, filepath="any-file-path", filename="AndroidManifest.xml")
        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        # NOTE: no version code is returned
        self.assertEqual(AppVersion(code=None, name="any-version-name"), manifest.get_version())

    @patch('ninjadroid.parsers.manifest.minidom')
    @patch('ninjadroid.parsers.manifest.AXMLPrinter')
    @patch('ninjadroid.parsers.manifest.FileParser')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_binary(self, mock_file, mock_file_parser, mock_axmlprinter, mock_minidom):
        file = any_file(filename="AndroidManifest.xml")
        mock_parser_instance = any_file_parser(file=file)
        mock_file_parser.return_value = mock_parser_instance
        mock_axmlprinter.return_value = self.any_axmlprinter()
        mock_minidom.parseString.return_value = self.any_axmlprinter_xml(
            package_name="any-package-name",
            version_code="1",
            version_name="any-version-name",
            sdk_max="20",
            sdk_min="10",
            sdk_target="15",
            permissions=["any-permission-1", "any-permission-2", "any-permission-0"]
        )

        manifest = self.sut.parse(
            filepath="any-file-path",
            binary = True,
            apk_path = None,
            extended_processing = False
        )

        assert_file_parser_called_once_with(mock_parser_instance, filepath="any-file-path", filename="AndroidManifest.xml")
        mock_file.assert_called_with("any-file-path", "rb")
        mock_axmlprinter.assert_called_with(ANY)
        mock_minidom.parseString.assert_called_with("any-axml-raw-value")
        assert_file_equal(self, expected=file, actual=manifest)
        self.assertEqual("any-package-name", manifest.get_package_name())
        self.assertEqual(AppVersion(code=1, name="any-version-name"), manifest.get_version())
        self.assertEqual(AppSdk(min_version="10", target_version="15", max_version="20"), manifest.get_sdk())
        self.assertEqual(["any-permission-0", "any-permission-1", "any-permission-2"], manifest.get_permissions())
        self.assertEqual([], manifest.get_activities())
        self.assertEqual([], manifest.get_services())
        self.assertEqual([], manifest.get_broadcast_receivers())

    @patch('ninjadroid.parsers.manifest.minidom')
    @patch('ninjadroid.parsers.manifest.AXMLPrinter')
    @patch('ninjadroid.parsers.manifest.FileParser')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_binary_when_axmlprinter_fails(self, mock_file, mock_file_parser, mock_axmlprinter, mock_minidom):
        file = any_file(filename="AndroidManifest.xml")
        mock_parser_instance = any_file_parser(file=file)
        mock_file_parser.return_value = mock_parser_instance
        mock_axmlprinter.side_effect = IOError()

        with self.assertRaises(AndroidManifestParsingError):
            self.sut.parse(
                filepath="any-file-path",
                binary = True,
                apk_path = None,
                extended_processing = False
            )

    @patch('ninjadroid.parsers.manifest.minidom')
    @patch('ninjadroid.parsers.manifest.FileParser')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_when_minidom_fails_without_apk_path(self, mock_file, mock_file_parser, mock_minidom):
        file = any_file(filename="AndroidManifest.xml")
        mock_parser_instance = any_file_parser(file=file)
        mock_file_parser.return_value = mock_parser_instance
        mock_minidom.parse.side_effect = ExpatError()

        with self.assertRaises(AndroidManifestParsingError):
            self.sut.parse(
                filepath="any-file-path",
                binary = False,
                apk_path = None,
                extended_processing = False
            )

    @patch('ninjadroid.parsers.manifest.Aapt')
    @patch('ninjadroid.parsers.manifest.minidom')
    @patch('ninjadroid.parsers.manifest.FileParser')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_when_minidom_fails_with_apk_path(self, mock_file, mock_file_parser, mock_minidom, mock_aapt):
        file = any_file(filename="AndroidManifest.xml")
        mock_parser_instance = any_file_parser(file=file)
        mock_file_parser.return_value = mock_parser_instance
        mock_minidom.parse.side_effect = ExpatError()
        mock_aapt.get_apk_info.return_value = self.any_aapt_apk_info(
            package_name="any-package-name",
            version_code=1,
            version_name="any-version-name",
            sdk_max="20",
            sdk_min="10",
            sdk_target="15"
        )
        mock_aapt.get_app_permissions.return_value = ["any-permission-0", "any-permission-1", "any-permission-2"]

        manifest = self.sut.parse(
            filepath="any-file-path",
            binary = False,
            apk_path = "any_apk_path",
            extended_processing = False
        )

        assert_file_parser_called_once_with(mock_parser_instance, filepath="any-file-path", filename="AndroidManifest.xml")
        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        mock_aapt.get_apk_info.assert_called_with("any_apk_path")
        mock_aapt.get_app_permissions.assert_called_with("any_apk_path")
        assert_file_equal(self, expected=file, actual=manifest)
        self.assertEqual("any-package-name", manifest.get_package_name())
        self.assertEqual(AppVersion(code=1, name="any-version-name"), manifest.get_version())
        self.assertEqual(AppSdk(min_version="10", target_version="15", max_version="20"), manifest.get_sdk())
        self.assertEqual(["any-permission-0", "any-permission-1", "any-permission-2"], manifest.get_permissions())
        self.assertEqual([], manifest.get_activities())
        self.assertEqual([], manifest.get_services())
        self.assertEqual([], manifest.get_broadcast_receivers())

    @patch('ninjadroid.parsers.manifest.Aapt')
    @patch('ninjadroid.parsers.manifest.minidom')
    @patch('ninjadroid.parsers.manifest.FileParser')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_when_minidom_fails_with_apk_path_and_extended_processing(self, mock_file, mock_file_parser, mock_minidom, mock_aapt):
        file = any_file(filename="AndroidManifest.xml")
        mock_parser_instance = any_file_parser(file=file)
        mock_file_parser.return_value = mock_parser_instance
        mock_minidom.parse.side_effect = ExpatError()
        mock_aapt.get_apk_info.return_value = self.any_aapt_apk_info(
            package_name="any-package-name",
            version_code=1,
            version_name="any-version-name",
            sdk_max="20",
            sdk_min="10",
            sdk_target="15"
        )
        mock_aapt.get_app_permissions.return_value = ["any-permission-0", "any-permission-1", "any-permission-2"]
        mock_aapt.get_manifest_info.return_value = self.any_aapt_manifest_info(
            activities=["any-activity-name"],
            services=["any-service-name"],
            receivers=["any-broadcast-receiver-name"]
        )

        manifest = self.sut.parse(
            filepath="any-file-path",
            binary = False,
            apk_path = "any_apk_path",
            extended_processing = True
        )

        assert_file_parser_called_once_with(mock_parser_instance, filepath="any-file-path", filename="AndroidManifest.xml")
        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        mock_aapt.get_apk_info.assert_called_with("any_apk_path")
        mock_aapt.get_app_permissions.assert_called_with("any_apk_path")
        mock_aapt.get_manifest_info.assert_called_with("any_apk_path")
        assert_file_equal(self, expected=file, actual=manifest)
        self.assertEqual("any-package-name", manifest.get_package_name())
        self.assertEqual(AppVersion(code=1, name="any-version-name"), manifest.get_version())
        self.assertEqual(AppSdk(min_version="10", target_version="15", max_version="20"), manifest.get_sdk())
        self.assertEqual(["any-permission-0", "any-permission-1", "any-permission-2"], manifest.get_permissions())
        self.assertEqual([AppActivity(name="any-activity-name")], manifest.get_activities())
        self.assertEqual([AppService(name="any-service-name")], manifest.get_services())
        self.assertEqual([AppBroadcastReceiver(name="any-broadcast-receiver-name")], manifest.get_broadcast_receivers())

    @parameterized.expand([
        ["AndroidManifest.xml", True],
        ["AndroidManifest", False],
        ["Whatever.xml", False]
    ])
    def test_looks_like_a_cert(self, filename, expected):
        result = AndroidManifestParser.looks_like_a_manifest(filename)

        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
