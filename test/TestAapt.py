##
# UnitTest for Aapt.py.
#
# RUN: python -m unittest -v test.TestAapt
#

from os import listdir
from os.path import join
import unittest

from lib.Aapt import Aapt


class TestAapt(unittest.TestCase):
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

    @classmethod
    def setUpClass(cls):
        cls.files = {}

        for filename in listdir(join('test', 'data')):
            if filename in cls.files_properties:
                cls.files[filename] = join('test', 'data', filename)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_app_name(self):
        for filename in self.files:
            self.assertTrue(Aapt.get_app_name(self.files[filename]) == self.files_properties[filename]['app_name'])

    def test_get_apk_info(self):
        for filename in self.files:
            apk = Aapt.get_apk_info(self.files[filename])
            self.assertTrue(apk['package_name'] == self.files_properties[filename]['package_name'])
            self.assertTrue(apk['version'] == self.files_properties[filename]['version'])
            self.assertTrue(apk['sdk'] == self.files_properties[filename]['sdk'])

    def test_get_manifest_info(self):
        for filename in self.files:
            man = Aapt.get_manifest_info(self.files[filename])
            self.assertTrue(man['activities'] == self.files_properties[filename]['activities'])
            self.assertTrue(man['services'] == self.files_properties[filename]['services'])
            self.assertTrue(man['receivers'] == self.files_properties[filename]['receivers'])

    def test_get_app_permissions(self):
        for filename in self.files:
            self.assertTrue(Aapt.get_app_permissions(self.files[filename]) == self.files_properties[filename]['permissions'])


if __name__ == '__main__':
    unittest.main()
