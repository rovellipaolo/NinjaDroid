from typing import Dict, List
import unittest
from unittest.mock import ANY, Mock, mock_open, patch
from xml.parsers.expat import ExpatError
from parameterized import parameterized
from tests.utils.file import any_file, any_file_parser, assert_file_equal, assert_file_parser_called_once_with

from ninjadroid.parsers.manifest import AndroidManifest, AndroidManifestParser, AndroidManifestParsingError, \
    AppActivity, AppBroadcastReceiver, AppService, AppSdk, AppVersion


# pylint: disable=too-many-arguments,too-many-locals,unused-argument
class TestAndroidManifestParser(unittest.TestCase):
    """
    Test AndroidManifest parser.
    """

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

    @staticmethod
    def any_axmlprinter_xml_with_extended_processing(
            package_name: str,
            version_code: str,
            version_name: str,
            sdk_min: str,
            sdk_target: str,
            sdk_max: str,
            permissions: List[str],
            activities: List[str],
            services: List[str],
            receivers: List[str]
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
        application_xml = Mock()
        activity_xml = Mock()
        activity_xml.getAttribute.side_effect = activities
        activity_xml.hasAttribute.return_value = False
        activity_xml.getElementsByTagName.return_value = []
        service_xml = Mock()
        service_xml.getAttribute.side_effect = services
        service_xml.hasAttribute.return_value = False
        service_xml.getElementsByTagName.return_value = []
        receiver_xml = Mock()
        receiver_xml.getAttribute.side_effect = receivers
        receiver_xml.hasAttribute.return_value = False
        receiver_xml.getElementsByTagName.return_value = []
        application_xml.getElementsByTagName.side_effect = [
            [activity_xml],
            [service_xml],
            [receiver_xml]
        ]
        xml.documentElement.getElementsByTagName.side_effect = [
            [application_xml],
            [sdk_xml],
            [permissions_xml, permissions_xml, permissions_xml]
        ]
        return xml

    def assert_manifest_equal(
            self,
            manifest: AndroidManifest,
            package_name: str,
            version: AppVersion,
            sdk: AppSdk,
            permissions: List[str],
            activities: List[AppActivity],
            services: List[AppService],
            receivers: List[AppBroadcastReceiver]
    ):
        self.assertEqual(package_name, manifest.get_package_name())
        self.assertEqual(version, manifest.get_version())
        self.assertEqual(sdk, manifest.get_sdk())
        self.assertEqual(permissions, manifest.get_permissions())
        self.assertEqual(activities, manifest.get_activities())
        self.assertEqual(services, manifest.get_services())
        self.assertEqual(receivers, manifest.get_broadcast_receivers())

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

        assert_file_parser_called_once_with(
            mock_parser_instance,
            filepath="any-file-path",
            filename="AndroidManifest.xml"
        )
        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        assert_file_equal(self, expected=file, actual=manifest)
        self.assert_manifest_equal(
            manifest=manifest,
            package_name="any-package-name",
            version=AppVersion(code=1, name="any-version-name"),
            sdk=AppSdk(min_version="10", target_version="15", max_version="20"),
            permissions=["any-permission-0", "any-permission-1", "any-permission-2"],
            activities=[],
            services=[],
            receivers=[]
        )

    @patch('ninjadroid.parsers.manifest.minidom')
    @patch('ninjadroid.parsers.manifest.FileParser')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_with_extended_processing(self, mock_file, mock_file_parser, mock_minidom):
        file = any_file(filename="AndroidManifest.xml")
        mock_parser_instance = any_file_parser(file=file)
        mock_file_parser.return_value = mock_parser_instance
        mock_minidom.parse.return_value = self.any_axmlprinter_xml_with_extended_processing(
            package_name="any-package-name",
            version_code="1",
            version_name="any-version-name",
            sdk_max="20",
            sdk_min="10",
            sdk_target="15",
            permissions=["any-permission-1", "any-permission-2", "any-permission-0"],
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

        assert_file_parser_called_once_with(
            mock_parser_instance,
            filepath="any-file-path",
            filename="AndroidManifest.xml"
        )
        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        assert_file_equal(self, expected=file, actual=manifest)
        self.assert_manifest_equal(
            manifest=manifest,
            package_name="any-package-name",
            version=AppVersion(code=1, name="any-version-name"),
            sdk=AppSdk(min_version="10", target_version="15", max_version="20"),
            permissions=["any-permission-0", "any-permission-1", "any-permission-2"],
            activities=[AppActivity(name="any-activity-name")],
            services=[AppService(name="any-service-name")],
            receivers=[AppBroadcastReceiver(name="any-broadcast-receiver-name")]
        )

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

        assert_file_parser_called_once_with(
            mock_parser_instance,
            filepath="any-file-path",
            filename="AndroidManifest.xml"
        )
        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        self.assert_manifest_equal(
            manifest=manifest,
            package_name="any-package-name",
            # NOTE: no version code is returned
            version=AppVersion(code=None, name="any-version-name"),
            sdk=AppSdk(min_version="10", target_version="15", max_version="20"),
            permissions=["any-permission-0", "any-permission-1", "any-permission-2"],
            activities=[],
            services=[],
            receivers=[]
        )

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

        assert_file_parser_called_once_with(
            mock_parser_instance,
            filepath="any-file-path",
            filename="AndroidManifest.xml"
        )
        mock_file.assert_called_with("any-file-path", "rb")
        mock_axmlprinter.assert_called_with(ANY)
        mock_minidom.parseString.assert_called_with("any-axml-raw-value")
        assert_file_equal(self, expected=file, actual=manifest)
        self.assert_manifest_equal(
            manifest=manifest,
            package_name="any-package-name",
            version=AppVersion(code=1, name="any-version-name"),
            sdk=AppSdk(min_version="10", target_version="15", max_version="20"),
            permissions=["any-permission-0", "any-permission-1", "any-permission-2"],
            activities=[],
            services=[],
            receivers=[]
        )

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

        assert_file_parser_called_once_with(
            mock_parser_instance,
            filepath="any-file-path",
            filename="AndroidManifest.xml"
        )
        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        mock_aapt.get_apk_info.assert_called_with("any_apk_path")
        mock_aapt.get_app_permissions.assert_called_with("any_apk_path")
        assert_file_equal(self, expected=file, actual=manifest)
        self.assert_manifest_equal(
            manifest=manifest,
            package_name="any-package-name",
            version=AppVersion(code=1, name="any-version-name"),
            sdk=AppSdk(min_version="10", target_version="15", max_version="20"),
            permissions=["any-permission-0", "any-permission-1", "any-permission-2"],
            activities=[],
            services=[],
            receivers=[]
        )

    @patch('ninjadroid.parsers.manifest.Aapt')
    @patch('ninjadroid.parsers.manifest.minidom')
    @patch('ninjadroid.parsers.manifest.FileParser')
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_when_minidom_fails_with_apk_path_and_extended_processing(
            self,
            mock_file,
            mock_file_parser,
            mock_minidom,
            mock_aapt
    ):
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

        assert_file_parser_called_once_with(
            mock_parser_instance,
            filepath="any-file-path",
            filename="AndroidManifest.xml"
        )
        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        mock_aapt.get_apk_info.assert_called_with("any_apk_path")
        mock_aapt.get_app_permissions.assert_called_with("any_apk_path")
        mock_aapt.get_manifest_info.assert_called_with("any_apk_path")
        assert_file_equal(self, expected=file, actual=manifest)
        self.assert_manifest_equal(
            manifest=manifest,
            package_name="any-package-name",
            version=AppVersion(code=1, name="any-version-name"),
            sdk=AppSdk(min_version="10", target_version="15", max_version="20"),
            permissions=["any-permission-0", "any-permission-1", "any-permission-2"],
            activities=[AppActivity(name="any-activity-name")],
            services=[AppService(name="any-service-name")],
            receivers=[AppBroadcastReceiver(name="any-broadcast-receiver-name")]
        )

    @parameterized.expand([
        ["AndroidManifest.xml", True],
        ["AndroidManifest", False],
        ["Whatever.xml", False],
        ["META-INF/CERT.RSA", False],
        ["classes.dex", False],
        ["Example.apk", False]
    ])
    def test_looks_like_manifest(self, filename, expected):
        result = AndroidManifestParser.looks_like_manifest(filename)

        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
