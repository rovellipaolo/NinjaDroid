from os.path import join
from parameterized import parameterized
import unittest
from unittest.mock import ANY, call, Mock, mock_open, patch
from xml.parsers.expat import ExpatError

from ninjadroid.errors.android_manifest_parsing_error import AndroidManifestParsingError
from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.android_manifest import AndroidManifest


class TestAndroidManifest(unittest.TestCase):
    """
    UnitTest for android_manifest.py.

    RUN: python -m unittest -v tests.test_android_manifest
    """

    FILE_NAME = "AndroidManifest.xml"
    ANY_FILE_SIZE = 3358
    ANY_FILE_MD5 = "c098fdd0a5dcf615118dad5457a2d016"
    ANY_FILE_SHA1 = "d69bbde630c8a5623b72a16d46b579432f2c944d"
    ANY_FILE_SHA256 = "a042569824ff2e268fdde5b8e00981293b27fe8a2a1dc72aa791e579f80bd720"
    ANY_FILE_SHA512 = "8875e2d19725c824c93e9f4e45b9ebcd599bffafde1af4b98975a2d6e497fde76870e5129eef289a25328562f4f21d9ff214db95dcd3ddb3b58f358ec362d78a"

    @staticmethod
    def any_file(
            mock_isfile: Mock,
            mock_access: Mock,
            mock_getsize: Mock,
            mock_md5: Mock,
            mock_sha1: Mock,
            mock_sha256: Mock,
            mock_sha512: Mock
    ):
        mock_isfile.return_value = True
        mock_access.return_value = True
        mock_getsize.return_value = TestAndroidManifest.ANY_FILE_SIZE
        mock_md5.return_value.hexdigest.return_value = TestAndroidManifest.ANY_FILE_MD5
        mock_sha1.return_value.hexdigest.return_value = TestAndroidManifest.ANY_FILE_SHA1
        mock_sha256.return_value.hexdigest.return_value = TestAndroidManifest.ANY_FILE_SHA256
        mock_sha512.return_value.hexdigest.return_value = TestAndroidManifest.ANY_FILE_SHA512

    @staticmethod
    def any_json():
        return {}

    @staticmethod
    def any_axmlprinter():
        axmlprinter = Mock()
        axmlprinter.get_buff.return_value = "any-axml-raw-value"
        return axmlprinter

    @staticmethod
    def any_aapt_apk_info(
        package_name: str,
        version_code: int,
        version_name: str,
        sdk_max: str = "",
        sdk_min: str = "",
        sdk_target: str = ""
    ):
        return {
            "package_name": package_name,
            "version": {
                "code": version_code,
                "name": version_name
            },
            "sdk": {
                "max": sdk_max,
                "min": sdk_min,
                "target": sdk_target
            }
        }

    @staticmethod
    def any_aapt_manifest_info():
        return {
            "activities": [
                {"name": "com.example.app.HomeActivity"}
            ],
            "services": [
                {"name": "com.example.app.ExampleService"}
            ],
            "receivers": [
                {"name": "com.example.app.ExampleBrodcastReceiver"}
            ]
        }

    @staticmethod
    def any_xml(
            package_name: str,
            version_code: str,
            version_name: str
    ):
        xml = Mock()
        xml.documentElement.getAttribute.side_effect = [
            package_name,
            version_code,
            version_name
        ]
        xml.documentElement.getElementsByTagName.hasAttribute.return_value = True
        return xml

    @patch('ninjadroid.parsers.android_manifest.minidom')
    @patch('ninjadroid.parsers.android_manifest.json')
    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_init(
            self,
            mock_file,
            mock_isfile,
            mock_access,
            mock_getsize,
            mock_md5,
            mock_sha1,
            mock_sha256,
            mock_sha512,
            mock_json,
            mock_minidom
    ):
        mock_json.load.return_value = self.any_json()
        mock_minidom.parse.return_value = self.any_xml(
            package_name="any-package-name",
            version_code="1",
            version_name="any-version-name"
        )
        self.any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512)

        manifest = AndroidManifest(
            filepath="any-file-path",
            binary = False,
            apk_path = "any_apk_path",
            extended_processing = False
        )

        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        self.assertEqual(TestAndroidManifest.FILE_NAME, manifest.get_file_name())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SIZE, manifest.get_size())
        self.assertEqual(TestAndroidManifest.ANY_FILE_MD5, manifest.get_md5())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA1, manifest.get_sha1())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA256, manifest.get_sha256())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA512, manifest.get_sha512())
        self.assertEqual("any-package-name", manifest.get_package_name())
        self.assertEqual(
            {
                "name": "any-version-name",
                "code": 1
            },
            manifest.get_version()
        )
        self.assertEqual(None, manifest.get_sdk_version())
        self.assertEqual(None, manifest.get_permissions())
        self.assertEqual(None, manifest.get_activities())
        self.assertEqual(None, manifest.get_services())
        self.assertEqual(None, manifest.get_broadcast_receivers())

    @patch('ninjadroid.parsers.android_manifest.minidom')
    @patch('ninjadroid.parsers.android_manifest.json')
    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_init_with_invalid_version_code(
            self,
            mock_file,
            mock_isfile,
            mock_access,
            mock_getsize,
            mock_md5,
            mock_sha1,
            mock_sha256,
            mock_sha512,
            mock_json,
            mock_minidom
    ):
        mock_json.load.return_value = self.any_json()
        mock_minidom.parse.return_value = self.any_xml(
            package_name="any-package-name",
            version_code="A",
            version_name="any-version-name"
        )
        self.any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512)

        manifest = AndroidManifest(
            filepath="any-file-path",
            binary = False,
            apk_path = None,
            extended_processing = False
        )

        mock_file.assert_called_with("any-file-path", "rb")
        # NOTE: no version code is returned
        self.assertEqual(
            {
                "name": "any-version-name",
                "code": ""
            },
            manifest.get_version()
        )

    @patch('ninjadroid.parsers.android_manifest.minidom')
    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_init_when_minidom_fails_and_no_apk_path(
            self,
            mock_file,
            mock_isfile,
            mock_access,
            mock_getsize,
            mock_md5,
            mock_sha1,
            mock_sha256,
            mock_sha512,
            mock_minidom
    ):
        mock_minidom.parse.side_effect = ExpatError()
        self.any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512)

        with self.assertRaises(AndroidManifestParsingError):
            AndroidManifest(
                filepath="any-file-path",
                binary = False,
                apk_path = None,
                extended_processing = False
            )

    @patch('ninjadroid.parsers.android_manifest.Aapt')
    @patch('ninjadroid.parsers.android_manifest.minidom')
    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_init_when_minidom_fails_with_apk_path(
            self,
            mock_file,
            mock_isfile,
            mock_access,
            mock_getsize,
            mock_md5,
            mock_sha1,
            mock_sha256,
            mock_sha512,
            mock_minidom,
            mock_aapt
    ):
        mock_minidom.parse.side_effect = ExpatError()
        mock_aapt.get_apk_info.return_value = self.any_aapt_apk_info(
            package_name="any-package-name",
            version_code=1,
            version_name="any-version-name"
        )
        self.any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512)

        manifest = AndroidManifest(
            filepath="any-file-path",
            binary = False,
            apk_path = "any_apk_path",
            extended_processing = False
        )

        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        mock_aapt.get_apk_info.assert_called_with("any_apk_path")
        self.assertEqual(TestAndroidManifest.FILE_NAME, manifest.get_file_name())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SIZE, manifest.get_size())
        self.assertEqual(TestAndroidManifest.ANY_FILE_MD5, manifest.get_md5())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA1, manifest.get_sha1())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA256, manifest.get_sha256())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA512, manifest.get_sha512())
        self.assertEqual("any-package-name", manifest.get_package_name())
        self.assertEqual(
            {
                "name": "any-version-name",
                "code": 1
            },
            manifest.get_version()
        )
        self.assertEqual(None, manifest.get_sdk_version())
        self.assertEqual(None, manifest.get_permissions())
        self.assertEqual(None, manifest.get_activities())
        self.assertEqual(None, manifest.get_services())
        self.assertEqual(None, manifest.get_broadcast_receivers())

    @patch('ninjadroid.parsers.android_manifest.Aapt')
    @patch('ninjadroid.parsers.android_manifest.minidom')
    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_init_when_minidom_fails_with_apk_path_and_extended_processing(
            self,
            mock_file,
            mock_isfile,
            mock_access,
            mock_getsize,
            mock_md5,
            mock_sha1,
            mock_sha256,
            mock_sha512,
            mock_minidom,
            mock_aapt
    ):
        mock_minidom.parse.side_effect = ExpatError()
        mock_aapt.get_apk_info.return_value = self.any_aapt_apk_info(
            package_name="any-package-name",
            version_code=1,
            version_name="any-version-name",
            sdk_max="20",
            sdk_min="10",
            sdk_target="15"
        )
        mock_aapt.get_app_permissions.return_value = ["any-permission-1", "any-permission-2"]
        mock_aapt.get_manifest_info.return_value = self.any_aapt_manifest_info()
        self.any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512)

        manifest = AndroidManifest(
            filepath="any-file-path",
            binary = False,
            apk_path = "any_apk_path",
            extended_processing = True
        )

        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parse.assert_called_with("any-file-path")
        mock_aapt.get_apk_info.assert_called_with("any_apk_path")
        self.assertEqual(TestAndroidManifest.FILE_NAME, manifest.get_file_name())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SIZE, manifest.get_size())
        self.assertEqual(TestAndroidManifest.ANY_FILE_MD5, manifest.get_md5())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA1, manifest.get_sha1())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA256, manifest.get_sha256())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA512, manifest.get_sha512())
        self.assertEqual("any-package-name", manifest.get_package_name())
        self.assertEqual(
            {
                "name": "any-version-name",
                "code": 1
            },
            manifest.get_version()
        )
        self.assertEqual(
            {
                "target": "15",
                "min": "10",
                "max": "20"
            },
            manifest.get_sdk_version()
        )
        self.assertEqual(["any-permission-1", "any-permission-2"], manifest.get_permissions())
        self.assertEqual([{"name": "com.example.app.HomeActivity"}], manifest.get_activities())
        self.assertEqual([{"name": "com.example.app.ExampleService"}], manifest.get_services())
        self.assertEqual([{"name": "com.example.app.ExampleBrodcastReceiver"}], manifest.get_broadcast_receivers())

    @patch('ninjadroid.parsers.android_manifest.AXMLPrinter')
    @patch('ninjadroid.parsers.android_manifest.minidom')
    @patch('ninjadroid.parsers.android_manifest.json')
    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_init_binary(
            self,
            mock_file,
            mock_isfile,
            mock_access,
            mock_getsize,
            mock_md5,
            mock_sha1,
            mock_sha256,
            mock_sha512,
            mock_json,
            mock_minidom,
            mock_axmlprinter
    ):
        mock_axmlprinter.return_value = self.any_axmlprinter()
        mock_json.load.return_value = self.any_json()
        mock_minidom.parseString.return_value = self.any_xml(
            package_name="any-package-name",
            version_code="1",
            version_name="any-version-name"
        )
        self.any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512)

        manifest = AndroidManifest(
            filepath="any-file-path",
            binary = True,
            apk_path = None,
            extended_processing = False
        )

        mock_file.assert_called_with("any-file-path", "rb")
        mock_minidom.parseString.assert_called_with("any-axml-raw-value")
        self.assertEqual(TestAndroidManifest.FILE_NAME, manifest.get_file_name())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SIZE, manifest.get_size())
        self.assertEqual(TestAndroidManifest.ANY_FILE_MD5, manifest.get_md5())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA1, manifest.get_sha1())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA256, manifest.get_sha256())
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA512, manifest.get_sha512())
        self.assertEqual("any-package-name", manifest.get_package_name())
        self.assertEqual(
            {
                "name": "any-version-name",
                "code": 1
            },
            manifest.get_version()
        )
        self.assertEqual(None, manifest.get_sdk_version())
        self.assertEqual(None, manifest.get_permissions())
        self.assertEqual(None, manifest.get_activities())
        self.assertEqual(None, manifest.get_services())
        self.assertEqual(None, manifest.get_broadcast_receivers())

    @patch('ninjadroid.parsers.android_manifest.AXMLPrinter')
    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_init_binary_when_axmlprinter_fails(
            self,
            mock_file,
            mock_isfile,
            mock_access,
            mock_getsize,
            mock_md5,
            mock_sha1,
            mock_sha256,
            mock_sha512,
            mock_axmlprinter
    ):
        mock_axmlprinter.side_effect = IOError()
        self.any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512)

        with self.assertRaises(AndroidManifestParsingError):
            AndroidManifest(
                filepath="any-file-path",
                binary = True,
                apk_path = None,
                extended_processing = False
            )

    @parameterized.expand([
        [
            AndroidManifest(
                filepath=join("tests", "data", "AndroidManifest.xml"),
                binary=False,
                apk_path="",
                extended_processing=False
            )
        ],
        [
            AndroidManifest(
                filepath=join("tests", "data", "AndroidManifestBinary.xml"),
                binary=True,
                apk_path="",
                extended_processing=False
            )
        ]
    ])
    def test_integration_init(self, manifest):
        self.assertTrue(manifest is not None)
        self.assertTrue(type(manifest) is AndroidManifest)

    def test_integration_init_with_non_manifests_file(self):
        with self.assertRaises(AndroidManifestParsingError):
            AndroidManifest(filepath=join("tests", "data", "classes.dex"), binary=False)
            AndroidManifest(filepath=join("tests", "data", "classes.dex"), binary=True)
            AndroidManifest(filepath=join("tests", "data", "CERT.RSA"), binary=False)
            AndroidManifest(filepath=join("tests", "data", "CERT.RSA"), binary=True)

    @parameterized.expand([
        ["AndroidManifest.xml", True],
        ["AndroidManifest", False],
        ["Whatever.xml", False]
    ])
    def test_looks_like_a_cert(self, filename, expected):
        result = AndroidManifest.looks_like_a_manifest(filename)

        self.assertEqual(expected, result)

    def test_integration_dump(self):
        manifest = AndroidManifest(
            filepath=join("tests", "data", "AndroidManifest.xml"),
            binary=False,
            apk_path="",
            extended_processing=False
        )

        dump = manifest.dump()

        self.assertEqual(TestAndroidManifest.FILE_NAME, dump["file"])
        self.assertEqual(TestAndroidManifest.ANY_FILE_SIZE, dump["size"])
        self.assertEqual(TestAndroidManifest.ANY_FILE_MD5, dump["md5"])
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA1, dump["sha1"])
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA256, dump["sha256"])
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA512, dump["sha512"])
        self.assertEqual('com.example.app', dump["package"])
        self.assertEqual({"code": 1, "name": "1.0"}, dump["version"])


    def test_integration_dump_with_extended_processing(self):
        manifest = AndroidManifest(
            filepath=join("tests", "data", "AndroidManifest.xml"),
            binary=False,
            apk_path="",
            extended_processing=True
        )

        dump = manifest.dump()

        self.assertEqual(TestAndroidManifest.FILE_NAME, dump["file"])
        self.assertEqual(TestAndroidManifest.ANY_FILE_SIZE, dump["size"])
        self.assertEqual(TestAndroidManifest.ANY_FILE_MD5, dump["md5"])
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA1, dump["sha1"])
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA256, dump["sha256"])
        self.assertEqual(TestAndroidManifest.ANY_FILE_SHA512, dump["sha512"])
        self.assertEqual('com.example.app', dump["package"])
        self.assertEqual({"code": 1, "name": "1.0"}, dump["version"])
        self.assertEqual({"target": "20", "min": "10", "max": "20"}, dump["sdk"])
        self.assertEqual(
            [
                "android.permission.INTERNET",
                "android.permission.READ_EXTERNAL_STORAGE",
                "android.permission.RECEIVE_BOOT_COMPLETED",
                "android.permission.WRITE_EXTERNAL_STORAGE"
            ],
            dump["permissions"]
        )


if __name__ == "__main__":
    unittest.main()
