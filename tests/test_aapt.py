import unittest
from unittest.mock import patch
from tests.utils.popen import any_popen, assert_popen_called_once

from ninjadroid.aapt.aapt import Aapt


# pylint: disable=too-many-public-methods,protected-access
class TestAapt(unittest.TestCase):
    """
    Test Aapt class.
    """

    FILE_NAME = "Example.apk"

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_execute_dump_badging(self, mock_popen):
        mock_popen.return_value = any_popen(b"any-result")

        result = Aapt._execute_dump_badging("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual("any-result", result)

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_execute_dump_permissions(self, mock_popen):
        mock_popen.return_value = any_popen(b"any-result")

        result = Aapt._execute_dump_badging("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual("any-result", result)

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_execute_dump_xmltree(self, mock_popen):
        mock_popen.return_value = any_popen(b"any-result")

        result = Aapt._execute_dump_xmltree("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual("any-result", result)

    def test_extract_app_name_when_application_label_is_present(self):
        dump_badging = "application-label:'Example0'\n" \
            "application: label='Example1' icon='res/drawable-mdpi-v4/ic_launcher.png'\n" \
            "launchable-activity: name='com.example.app.HomeActivity'  label='Example2' icon=''"

        app_name = Aapt._extract_app_name(dump_badging)

        self.assertEqual("Example1", app_name)

    def test_extract_app_name_when_application_label_is_not_present_but_launchable_activity_label_is(self):
        app_name = Aapt._extract_app_name("launchable-activity: name='com.example.app.HomeActivity'  label='Example2'")

        self.assertEqual("Example2", app_name)

    def test_extract_app_name_when_no_label_is_present(self):
        app_name = Aapt._extract_app_name("")

        self.assertEqual("", app_name)

    def test_extract_package_name(self):
        package_name = Aapt._extract_package_name("package: name='com.example.app' versionCode='1' versionName='1.0'")

        self.assertEqual("com.example.app", package_name)

    def test_extract_version_name(self):
        version_name = Aapt._extract_version_name("package: name='com.example.app' versionCode='1' versionName='1.0'")

        self.assertEqual("1.0", version_name)

    def _extract_version_code_when_present(self):
        version_code = Aapt._extract_version_code("package: name='com.example.app' versionCode='1' versionName='1.0'")

        self.assertEqual(1, version_code)

    def _extract_version_code_when_invalid(self):
        version_code = Aapt._extract_version_code("package: name='com.example.app' versionCode='A' versionName='1.0'")

        self.assertIsNone(version_code)

    def _extract_version_code_when_missing(self):
        version_code = Aapt._extract_version_code("")

        self.assertIsNone(version_code)

    def test_extract_sdk_target_when_present(self):
        dump_badging = "sdkVersion:'10'\n" \
            "maxSdkVersion:'20'\n" \
            "targetSdkVersion:'15'"

        sdk_target = Aapt._extract_sdk_target_version(dump_badging)

        self.assertEqual("15", sdk_target)

    def test_extract_sdk_target_when_missing(self):
        sdk_target = Aapt._extract_sdk_target_version("")

        self.assertEqual("", sdk_target)

    def test_extract_sdk_max_version_when_present(self):
        dump_badging = "sdkVersion:'10'\n" \
            "maxSdkVersion:'20'\n" \
            "targetSdkVersion:'15'"

        max_version = Aapt._extract_sdk_max_version(dump_badging)

        self.assertEqual("20", max_version)

    def test_extract_sdk_max_version_when_missing(self):
        max_version = Aapt._extract_sdk_max_version("")

        self.assertEqual("", max_version)

    def test_extract_sdk_min_version_when_present(self):
        dump_badging = "sdkVersion:'10'\n" \
            "maxSdkVersion:'20'\n" \
            "targetSdkVersion:'15'"

        min_version = Aapt._extract_sdk_min_version(dump_badging)

        self.assertEqual("10", min_version)

    def test_extract_sdk_min_version_when_missing(self):
        min_version = Aapt._extract_sdk_min_version("")

        self.assertEqual("", min_version)

    def test_extract_activities(self):
        dump_badging = """N: android=http://schemas.android.com/apk/res/android
              E: manifest (line=2)
                E: application (line=8)
                  E: activity (line=9)
                    A: android:name(0x01010003)="com.example.app.HomeActivity" (Raw: "...")
                  E: activity (line=15)
                    A: android:name(0x01010003)="com.example.app.OtherActivity" (Raw: "...")
        """

        activities = Aapt._extract_activities(dump_badging)

        self.assertEqual(["com.example.app.HomeActivity", "com.example.app.OtherActivity"], activities)

    def test_extract_activities_when_missing(self):
        activities = Aapt._extract_activities("")

        self.assertEqual([], activities)

    def test_extract_services(self):
        dump_badging = """N: android=http://schemas.android.com/apk/res/android
              E: manifest (line=2)
                E: application (line=8)
                  E: service (line=25)
                    A: android:name(0x01010003)="com.example.app.ExampleService" (Raw: "...")
                  E: service (line=28)
                    A: android:name(0x01010003)="com.example.app.OtherService" (Raw: "...")
        """

        services = Aapt._extract_services(dump_badging)

        self.assertEqual(["com.example.app.ExampleService", "com.example.app.OtherService"], services)

    def test_extract_services_when_missing(self):
        services = Aapt._extract_services("")

        self.assertEqual([], services)

    def test_extract_broadcast_receivers(self):
        dump_badging = """N: android=http://schemas.android.com/apk/res/android
              E: manifest (line=2)
                E: application (line=8)
                  E: receiver (line=38)
                    A: android:name(0x01010003)="com.example.app.ExampleBrodcastReceiver" (Raw: "...")
                  E: receiver (line=44)
                    A: android:name(0x01010003)="com.example.app.OtherBrodcastReceiver" (Raw: "...")
        """

        receivers = Aapt._extract_broadcast_receivers(dump_badging)

        self.assertEqual(
            ["com.example.app.ExampleBrodcastReceiver", "com.example.app.OtherBrodcastReceiver"],
            receivers
        )

    def test_extract_broadcast_receivers_when_missing(self):
        receivers = Aapt._extract_broadcast_receivers("")

        self.assertEqual([], receivers)

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_app_name(self, mock_popen):
        mock_popen.return_value = any_popen(b"application: label='Example' icon='res/ic_launcher.png'\n")

        app_name = Aapt.get_app_name("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual("Example", app_name)

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_app_name_when_dumb_badging_fails(self, mock_popen):
        mock_popen.side_effect = RuntimeError()

        app_name = Aapt.get_app_name("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual("", app_name)

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_apk_info(self, mock_popen):
        dump_badging = b"package: name='com.example.app' versionCode='1' versionName='1.0'\n" \
                       b"sdkVersion:'10'\n" \
                       b"maxSdkVersion:'20'\n" \
                       b"targetSdkVersion:'15'"
        mock_popen.return_value = any_popen(dump_badging)

        apk = Aapt.get_apk_info("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual(
            {
                "package_name": "com.example.app",
                "version": {
                    "code": 1,
                    "name": "1.0"
                },
                "sdk": {
                    "max": "20",
                    "min": "10",
                    "target": "15"
                }
            },
            apk
        )

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_apk_info_with_invalid_version_code(self, mock_popen):
        mock_popen.return_value = any_popen(b"package: name='com.example.app' versionCode='A' versionName='1.0'\n")

        apk = Aapt.get_apk_info("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual(
            {
                "code": "",  # NOTE: None is converted into an empty string
                "name": "1.0"
            },
            apk["version"]
        )

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_apk_info_when_dumb_badging_fails(self, mock_popen):
        mock_popen.side_effect = RuntimeError()

        apk = Aapt.get_apk_info("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual(
            {
                "package_name": "",
                "version": {
                    "code": "",
                    "name": ""
                },
                "sdk": {}
            },
            apk
        )

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_manifest_info(self, mock_popen):
        dump_xmltree = b"N: android=http://schemas.android.com/apk/res/android\n" \
                       b"  E: manifest (line=2)\n" \
                       b"    E: application (line=8)\n" \
                       b"      E: activity (line=9)\n" \
                       b"        A: android:name(0x01010003)=\"any-activity\" (Raw: \"any-activity\")\n" \
                       b"      E: activity (line=15)\n" \
                       b"        A: android:name(0x01010003)=\"any-other-activity\" (Raw: \"any-other-activity\")\n" \
                       b"      E: service (line=25)\n" \
                       b"        A: android:name(0x01010003)=\"any-service\" (Raw: \"any-service\")\n" \
                       b"      E: service (line=26)\n" \
                       b"        A: android:name(0x01010003)=\"any-other-service\" (Raw: \"any-other-service\")\n" \
                       b"      E: receiver (line=28)\n" \
                       b"        A: android:name(0x01010003)=\"any-receiver\" (Raw: \"any-receiver\")\n" \
                       b"      E: receiver (line=29)\n" \
                       b"        A: android:name(0x01010003)=\"any-other-receiver\" (Raw: \"any-other-receiver\")"
        mock_popen.return_value = any_popen(dump_xmltree)

        manifest = Aapt.get_manifest_info("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual(
            {
                "activities": [
                    "any-activity",
                    "any-other-activity"
                ],
                "services": [
                    "any-service",
                    "any-other-service"
                ],
                "receivers": [
                    "any-receiver",
                    "any-other-receiver"
                ]
            },
            manifest
        )

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_manifest_info_when_dumb_xmltree_fails(self, mock_popen):
        mock_popen.side_effect = RuntimeError()

        manifest = Aapt.get_manifest_info("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual(
            {
                "activities": [],
                "services": [],
                "receivers": []
            },
            manifest
        )

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_app_permissions(self, mock_popen):
        dump_permissions = b"package: com.example.app\n" \
                           b"uses-permission: name='android.permission.READ_EXTERNAL_STORAGE'\n" \
                           b"uses-permission: name='android.permission.RECEIVE_BOOT_COMPLETED'\n" \
                           b"uses-permission: name='android.permission.WRITE_EXTERNAL_STORAGE'\n" \
                           b"uses-permission: name='android.permission.INTERNET'"
        mock_popen.return_value = any_popen(dump_permissions)

        permissions = Aapt.get_app_permissions("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual(
            [
                "android.permission.INTERNET",
                "android.permission.READ_EXTERNAL_STORAGE",
                "android.permission.RECEIVE_BOOT_COMPLETED",
                "android.permission.WRITE_EXTERNAL_STORAGE"
            ],
            permissions
        )

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_app_permissions_when_dumb_permissions_fails(self, mock_popen):
        mock_popen.side_effect = RuntimeError()

        permissions = Aapt.get_app_permissions("any-file-path")

        assert_popen_called_once(mock_popen)
        self.assertEqual([], permissions)


if __name__ == "__main__":
    unittest.main()
