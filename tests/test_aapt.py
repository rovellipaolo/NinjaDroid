from os import listdir
from os.path import join
import unittest
from unittest.mock import patch

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

    def test_integration_get_app_name(self):
        for filename in listdir(join("tests", "data")):
            if filename in self.files_properties:
                file = join("tests", "data", filename)

                app_name = Aapt.get_app_name(file)

                self.assertEqual(self.files_properties[filename]["app_name"], app_name)

    def test_integration_get_app_name_when_dumb_badging_fails(self):
        app_name = Aapt.get_app_name("aaa_this_is_a_non_existent_file_xxx.apk")

        self.assertEqual("", app_name)

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

    def test_integration_get_apk_info_when_dumb_badging_fails(self):
        apk = Aapt.get_apk_info("aaa_this_is_a_non_existent_file_xxx.apk")

        self.assertEqual(
            {
                "package_name": "",
                "version": {"code": "", "name": ""},
                "sdk": {}
            },
            apk
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

    def test_integration_get_manifest_info_when_dump_xmltree_fails(self):
        manifest = Aapt.get_manifest_info("aaa_this_is_a_non_existent_file_xxx.apk")

        self.assertEqual(
            {
                "activities": [],
                "services": [],
                "receivers": []
            },
            manifest
        )

    def test_integration_get_app_permissions(self):
        for filename in listdir(join("tests", "data")):
            if filename in self.files_properties:
                file = join("tests", "data", filename)

                permissions = Aapt.get_app_permissions(file)

                self.assertEqual(self.files_properties[filename]["permissions"], permissions)

    def test_integration_get_app_permissions_when_dump_permissions_fails(self):
        permissions = Aapt.get_app_permissions("aaa_this_is_a_non_existent_file_xxx.apk")

        self.assertEqual([], permissions)


if __name__ == "__main__":
    unittest.main()
