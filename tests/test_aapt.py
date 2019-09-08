from os import listdir
from os.path import join
import unittest

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

    def setUp(self):
        self.files = {}

        for filename in listdir(join("tests", "data")):
            if filename in self.files_properties:
                self.files[filename] = join("tests", "data", filename)

    def tearDown(self):
        pass

    def test_get_app_name(self):
        for filename in self.files:
            self.assertEqual(
                self.files_properties[filename]["app_name"],
                Aapt.get_app_name(self.files[filename])
            )

    def test_get_apk_info(self):
        for filename in self.files:
            apk = Aapt.get_apk_info(self.files[filename])
            self.assertEqual(apk["package_name"], self.files_properties[filename]["package_name"])
            self.assertEqual(apk["version"], self.files_properties[filename]["version"])
            self.assertEqual(apk["sdk"], self.files_properties[filename]["sdk"])

    def test_get_manifest_info(self):
        for filename in self.files:
            man = Aapt.get_manifest_info(self.files[filename])
            self.assertEqual(man["activities"], self.files_properties[filename]["activities"])
            self.assertEqual(man["services"], self.files_properties[filename]["services"])
            self.assertEqual(man["receivers"], self.files_properties[filename]["receivers"])

    def test_get_app_permissions(self):
        for filename in self.files:
            self.assertEqual(
                self.files_properties[filename]["permissions"],
                Aapt.get_app_permissions(self.files[filename])
            )


if __name__ == "__main__":
    unittest.main()
