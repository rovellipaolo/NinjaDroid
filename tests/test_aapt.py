from os import listdir
from os.path import join
from subprocess import PIPE
import unittest
from unittest.mock import ANY, patch, Mock

from ninjadroid.aapt.aapt import Aapt


class TestAapt(unittest.TestCase):
    """
    UnitTest for aapt.py.

    RUN: python -m unittest -v tests.test_aapt
    """

    files_properties = {
        "Example.apk": {
            "app_name": "Example",
            "package_name": "com.example.app",
            "version": {"name": "1.0", "code": 1},
            "sdk": {"target": "20", "min": "10", "max": "20"},
            "permissions": [
                "android.permission.INTERNET",
                "android.permission.READ_EXTERNAL_STORAGE",
                "android.permission.RECEIVE_BOOT_COMPLETED",
                "android.permission.WRITE_EXTERNAL_STORAGE"
            ],
            "receivers": [
                {"name": "com.example.app.ExampleBrodcastReceiver"},
                {"name": "com.example.app.ExampleBrodcastReceiver2"},
                {"name": "com.example.app.ExampleBrodcastReceiver3"},
                {"name": "com.example.app.ExampleBrodcastReceiver4"}
            ],
            "activities": [
                {"name": "com.example.app.HomeActivity"},
                {"name": "com.example.app.OtherActivity"}
            ],
            "services": [
                {"name": "com.example.app.ExampleService"},
                {"name": "com.example.app.ExampleService2"},
                {"name": "com.example.app.ExampleService3"}
            ],
        },
    }

    @staticmethod
    def any_popen(stdout):
        any_popen = Mock()
        any_popen.communicate.return_value = (stdout, "")
        return any_popen

    def test_extract_app_name_when_application_label_is_present(self):
        dump_badging = "application-label:'Example0'\n" \
            "application: label='Example1' icon='res/drawable-mdpi-v4/ic_launcher.png'\n" \
            "launchable-activity: name='com.example.app.HomeActivity'  label='Example2' icon=''"

        app_name = Aapt._extract_app_name(dump_badging)

        self.assertEqual("Example1", app_name)

    def test_extract_app_name_when_application_label_is_not_present_but_launchable_activity_label_is(self):
        dump_badging = "launchable-activity: name='com.example.app.HomeActivity'  label='Example2' icon=''"

        app_name = Aapt._extract_app_name(dump_badging)

        self.assertEqual("Example2", app_name)

    def test_extract_app_name_when_no_label_is_present(self):
        app_name = Aapt._extract_app_name("")

        self.assertEqual("", app_name)

    def test_extract_package_name(self):
        dump_badging = "package: name='com.example.app' versionCode='1' versionName='1.0' platformBuildVersionName='4'"

        package_name = Aapt._extract_package_name(dump_badging)

        self.assertEqual("com.example.app", package_name)

    def test_extract_version_name(self):
        dump_badging = "package: name='com.example.app' versionCode='1' versionName='1.0' platformBuildVersionName='4'"

        version_name = Aapt._extract_version_name(dump_badging)

        self.assertEqual("1.0", version_name)

    def _extract_version_code_when_present(self):
        dump_badging = "package: name='com.example.app' versionCode='1' versionName='1.0' platformBuildVersionName='4'"

        version_code = Aapt._extract_version_code(dump_badging)

        self.assertEqual(1, version_code)

    def _extract_version_code_when_missing(self):
        version_code = Aapt._extract_version_code("")

        self.assertEqual(None, version_code)

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

        self.assertEqual(
            [
                {"name": "com.example.app.HomeActivity"},
                {"name": "com.example.app.OtherActivity"}
            ],
            activities
        )

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

        self.assertEqual(
            [
                {"name": "com.example.app.ExampleService"},
                {"name": "com.example.app.OtherService"}
            ],
            services
        )

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
            [
                {"name": "com.example.app.ExampleBrodcastReceiver"},
                {"name": "com.example.app.OtherBrodcastReceiver"}
            ],
            receivers
        )

    def test_extract_broadcast_receivers_when_missing(self):
        receivers = Aapt._extract_broadcast_receivers("")

        self.assertEqual([], receivers)

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_app_name(self, mock_popen):
        mock_popen.return_value = self.any_popen(b"application: label='Example' icon='res/ic_launcher.png'\n")

        app_name = Aapt.get_app_name("any-file-path")

        mock_popen.assert_called_once_with(ANY, stdout=PIPE, stderr=None, shell=True)
        self.assertEqual("Example", app_name)

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_app_name_when_dumb_badging_fails(self, mock_popen):
        mock_popen.side_effect = RuntimeError()

        app_name = Aapt.get_app_name("any-file-path")

        mock_popen.assert_called_once_with(ANY, stdout=PIPE, stderr=None, shell=True)
        self.assertEqual("", app_name)

    def test_integration_get_app_name(self):
        for filename in listdir(join("tests", "data")):
            if filename in self.files_properties:
                file = join("tests", "data", filename)

                app_name = Aapt.get_app_name(file)

                self.assertEqual(self.files_properties[filename]["app_name"], app_name)

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_apk_info(self, mock_popen):
        dump_badging = b"package: name='com.example.app' versionCode='1' versionName='1.0' platformBuildVersionName='4'\n" \
                       b"sdkVersion:'10'\n" \
                       b"maxSdkVersion:'20'\n" \
                       b"targetSdkVersion:'15'"
        mock_popen.return_value = self.any_popen(dump_badging)

        apk = Aapt.get_apk_info("any-file-path")

        mock_popen.assert_called_once_with(ANY, stdout=PIPE, stderr=None, shell=True)
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
    def test_get_apk_info_when_dumb_badging_fails(self, mock_popen):
        mock_popen.side_effect = RuntimeError()

        apk = Aapt.get_apk_info("any-file-path")

        mock_popen.assert_called_once_with(ANY, stdout=PIPE, stderr=None, shell=True)
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

    def test_integration_get_apk_info(self):
        for filename in listdir(join("tests", "data")):
            if filename in self.files_properties:
                file = join("tests", "data", filename)

                apk = Aapt.get_apk_info(file)

                self.assertEqual(
                    {
                        "package_name": self.files_properties[filename]["package_name"],
                        "version": self.files_properties[filename]["version"],
                        "sdk": self.files_properties[filename]["sdk"]
                    },
                    apk
                )

    @patch('ninjadroid.aapt.aapt.Popen')
    def test_get_manifest_info_when_dumb_xmltree_fails(self, mock_popen):
        mock_popen.side_effect = RuntimeError()

        manifest = Aapt.get_manifest_info("any-file-path")

        mock_popen.assert_called_once_with(ANY, stdout=PIPE, stderr=None, shell=True)
        self.assertEqual(
            {
                "activities": [],
                "services": [],
                "receivers": []
            },
            manifest
        )

    def test_integration_get_manifest_info(self):
        for filename in listdir(join("tests", "data")):
            if filename in self.files_properties:
                file = join("tests", "data", filename)

                manifest = Aapt.get_manifest_info(file)

                self.assertEqual(
                    {
                        "activities": self.files_properties[filename]["activities"],
                        "services": self.files_properties[filename]["services"],
                        "receivers": self.files_properties[filename]["receivers"]
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
        mock_popen.return_value = self.any_popen(dump_permissions)

        permissions = Aapt.get_app_permissions("any-file-path")

        mock_popen.assert_called_once_with(ANY, stdout=PIPE, stderr=None, shell=True)
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

        mock_popen.assert_called_once_with(ANY, stdout=PIPE, stderr=None, shell=True)
        self.assertEqual([], permissions)

    def test_integration_get_app_permissions(self):
        for filename in listdir(join("tests", "data")):
            if filename in self.files_properties:
                file = join("tests", "data", filename)

                permissions = Aapt.get_app_permissions(file)

                self.assertEqual(self.files_properties[filename]["permissions"], permissions)


if __name__ == "__main__":
    unittest.main()
