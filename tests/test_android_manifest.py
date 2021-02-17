from os.path import join
import unittest

from ninjadroid.errors.android_manifest_parsing_error import AndroidManifestParsingError
from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.android_manifest import AndroidManifest


# TODO: refactor these tests...
class TestAndroidManifest(unittest.TestCase):
    """
    UnitTest for android_manifest.py.

    RUN: python -m unittest -v tests.test_android_manifest
    """

    @classmethod
    def setUpClass(cls):
        cls.manifests = {
            "summary": AndroidManifest(
                filepath=join("tests", "data", "AndroidManifest.xml"),
                binary=False,
                apk_path="",
                extended_processing=False
            ),
            "extended": AndroidManifest(
                filepath=join("tests", "data", "AndroidManifest.xml"),
                binary=False,
                apk_path="",
                extended_processing=True
            ),
            "binary": AndroidManifest(
                filepath=join("tests", "data", "AndroidManifestBinary.xml"),
                binary=True,
                apk_path="",
                extended_processing=True
            )
        }
        # print(self.manifests["summary"].dump())
        # print(self.manifests["extended"].dump())
        # print(self.manifests["binary"].dump())

    def test_init(self):
        self.assertTrue(self.manifests["summary"] is not None)
        self.assertTrue(type(self.manifests["summary"]) is AndroidManifest)
        self.assertTrue(self.manifests["extended"] is not None)
        self.assertTrue(type(self.manifests["extended"]) is AndroidManifest)
        self.assertTrue(self.manifests["binary"] is not None)
        self.assertTrue(type(self.manifests["binary"]) is AndroidManifest)

    def test_init_with_wrong_configuration_but_original_apk(self):
        manifest = AndroidManifest(
            filepath=join("tests", "data", "AndroidManifestBinary.xml"),
            binary=False,
            apk_path=join("tests", "data", "Example.apk")
        )

        self.assertTrue(manifest is not None)
        self.assertTrue(type(manifest) is AndroidManifest)

    def test_init_with_wrong_configuration(self):
        with self.assertRaises(AndroidManifestParsingError):
            AndroidManifest(join("tests", "data", "AndroidManifestBinary.xml"), False)

    def test_init_with_non_existing_file(self):
        with self.assertRaises(ParsingError):
            AndroidManifest(join("tests", "data", "aaa_this_is_a_non_existent_file_xxx"))

    def test_init_with_non_manifests_file(self):
        with self.assertRaises(AndroidManifestParsingError):
            AndroidManifest(join("tests", "data", "classes.dex"), False)
            AndroidManifest(join("tests", "data", "classes.dex"), True)
            AndroidManifest(join("tests", "data", "CERT.RSA"), False)
            AndroidManifest(join("tests", "data", "CERT.RSA"), True)

    def test_get_raw_file(self):
        self.assertTrue(len(self.manifests["summary"].get_raw_file()) > 0)
        self.assertTrue(len(self.manifests["extended"].get_raw_file()) > 0)
        self.assertTrue(len(self.manifests["binary"].get_raw_file()) > 0)

    def test_get_file_name(self):
        self.assertEqual("AndroidManifest.xml", self.manifests["summary"].get_file_name())
        self.assertEqual("AndroidManifest.xml", self.manifests["extended"].get_file_name())
        self.assertEqual("AndroidManifest.xml", self.manifests["binary"].get_file_name())

    def test_get_size(self):
        self.assertEqual(3358, self.manifests["summary"].get_size())
        self.assertEqual(3358, self.manifests["extended"].get_size())
        self.assertEqual(6544, self.manifests["binary"].get_size())

    def test_get_md5(self):
        self.assertEqual("c098fdd0a5dcf615118dad5457a2d016", self.manifests["summary"].get_md5())
        self.assertEqual("c098fdd0a5dcf615118dad5457a2d016", self.manifests["extended"].get_md5())
        self.assertEqual("1f97f7e7ca62f39f8f81d79b1b540c37", self.manifests["binary"].get_md5())

    def test_get_sha1(self):
        self.assertEqual("d69bbde630c8a5623b72a16d46b579432f2c944d", self.manifests["summary"].get_sha1())
        self.assertEqual("d69bbde630c8a5623b72a16d46b579432f2c944d", self.manifests["extended"].get_sha1())
        self.assertEqual("011316a011e5b8738c12c662cb0b0a6ffe04ca74", self.manifests["binary"].get_sha1())

    def test_get_sha256(self):
        self.assertEqual(
            "a042569824ff2e268fdde5b8e00981293b27fe8a2a1dc72aa791e579f80bd720",
            self.manifests["summary"].get_sha256()
        )
        self.assertEqual(
            "a042569824ff2e268fdde5b8e00981293b27fe8a2a1dc72aa791e579f80bd720",
            self.manifests["extended"].get_sha256()
        )
        self.assertEqual(
            "7c8011a46191ecb368bf2e0104049abeb98bae8a7b1fa3328ff050aed85b1347",
            self.manifests["binary"].get_sha256()
        )

    def test_get_sha512(self):
        self.assertEqual(
            "8875e2d19725c824c93e9f4e45b9ebcd599bffafde1af4b98975a2d6e497fde76870e5129eef289a25328562f4f21d9ff214db95dcd3ddb3b58f358ec362d78a",
            self.manifests["summary"].get_sha512()
        )
        self.assertEqual(
            "8875e2d19725c824c93e9f4e45b9ebcd599bffafde1af4b98975a2d6e497fde76870e5129eef289a25328562f4f21d9ff214db95dcd3ddb3b58f358ec362d78a",
            self.manifests["extended"].get_sha512()
        )
        self.assertEqual(
            "8c7c1ede610f9c6613418b46a52a196ad6d5e8cc067c2f26b931738ad8087f998d9ea95e80ec4352c95fbdbb93a4f29c646973535068a3a3d584da95480ab45f",
            self.manifests["binary"].get_sha512()
        )

    def test_get_package_name(self):
        for man in self.manifests:
            package_name = self.manifests[man].get_package_name()
            self.assertEqual("com.example.app", package_name)

    def test_get_version(self):
        for man in self.manifests:
            version = self.manifests[man].get_version()
            self.assertEqual(1, version["code"])
            self.assertEqual("1.0", version["name"])

    def test_get_sdk_version(self):
        sdk = self.manifests["summary"].get_sdk_version()

        self.assertIsNone(sdk)

    def test_get_sdk_version_with_extended_processing(self):
        for man in ["extended", "binary"]:
            sdk = self.manifests[man].get_sdk_version()

            self.assertEqual("20", sdk["target"])
            self.assertEqual("10", sdk["min"])
            self.assertEqual("20", sdk["max"])

    def test_get_permissions(self):
        permissions = self.manifests["summary"].get_permissions()

        self.assertIsNone(permissions)

    def test_get_permissions_with_extended_processing(self):
        expected_permissions = [
            "android.permission.INTERNET",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.RECEIVE_BOOT_COMPLETED",
            "android.permission.WRITE_EXTERNAL_STORAGE"
        ]
        expected_permissions.sort()

        for man in ["extended", "binary"]:
            permissions = self.manifests[man].get_permissions()

            self.assertEqual(expected_permissions, permissions)

    def test_get_activities(self):
        activities = self.manifests["summary"].get_activities()

        self.assertIsNone(activities)

    def test_get_activities_with_extended_processing(self):
        for man in ["extended", "binary"]:
            activities = self.manifests[man].get_activities()

            # Test 1st Activity:
            self.assertTrue("name" in activities[0])
            self.assertEqual("com.example.app.HomeActivity", activities[0]["name"])
            self.assertTrue("allowEmbedded" not in activities[0])
            self.assertTrue("allowTaskReparenting" not in activities[0])
            self.assertTrue("alwaysRetainTaskState" not in activities[0])
            self.assertTrue("autoRemoveFromRecents" not in activities[0])
            self.assertTrue("banner" not in activities[0])
            self.assertTrue("clearTaskOnLaunch" not in activities[0])
            self.assertTrue("configChanges" in activities[0])
            self.assertTrue(activities[0]["configChanges"] == "orientation|screenSize" or
                            activities[0]["configChanges"] == "0x00000480")
            self.assertTrue("documentLaunchMode" not in activities[0])
            self.assertTrue("enabled" not in activities[0])
            self.assertTrue("excludeFromRecents" not in activities[0])
            self.assertTrue("exported" not in activities[0])
            self.assertTrue("finishOnTaskLaunch" not in activities[0])
            self.assertTrue("hardwareAccelerated" not in activities[0])
            self.assertTrue("icon" not in activities[0])
            self.assertTrue("label" in activities[0])
            self.assertTrue(activities[0]["label"] == "@string/app_name" or activities[0]["label"] == "@7F040000")
            self.assertTrue("launchMode" in activities[0])
            self.assertTrue(activities[0]["launchMode"] == "singleTop" or activities[0]["launchMode"] == "1")
            self.assertTrue("maxRecents" not in activities[0])
            self.assertTrue("multiprocess" not in activities[0])
            self.assertTrue("noHistory" not in activities[0])
            self.assertTrue("parentActivityName" not in activities[0])
            self.assertTrue("permission" not in activities[0])
            self.assertTrue("process" not in activities[0])
            self.assertTrue("relinquishTaskIdentity" not in activities[0])
            self.assertTrue("screenOrientation" not in activities[0])
            self.assertTrue("stateNotNeeded" not in activities[0])
            self.assertTrue("taskAffinity" not in activities[0])
            self.assertTrue("theme" not in activities[0])
            self.assertTrue("uiOptions" not in activities[0])
            self.assertTrue("windowSoftInputMode" not in activities[0])
            # Test meta-data parsing:
            self.assertTrue("meta-data" not in activities[0])
            # Test intent-filter parsing:
            self.assertTrue("intent-filter" in activities[0])
            self.assertTrue(len(activities[0]["intent-filter"]) == 1)
            # priority
            self.assertTrue("priority" not in activities[0]["intent-filter"][0])
            # action
            self.assertTrue("action" in activities[0]["intent-filter"][0])
            self.assertEqual(1, len(activities[0]["intent-filter"][0]["action"]))
            self.assertEqual(activities[0]["intent-filter"][0]["action"][0], "android.intent.action.MAIN")
            # category
            self.assertTrue("category" in activities[0]["intent-filter"][0])
            self.assertEqual(1, len(activities[0]["intent-filter"][0]["category"]))
            self.assertEqual("android.intent.category.LAUNCHER", activities[0]["intent-filter"][0]["category"][0])
            # data
            self.assertTrue("data" not in activities[0]["intent-filter"][0])

            # Test 2nd Activity:
            self.assertTrue("name" in activities[1])
            self.assertEqual("com.example.app.OtherActivity", activities[1]["name"])
            self.assertTrue("allowEmbedded" not in activities[1])
            self.assertTrue("allowTaskReparenting" not in activities[1])
            self.assertTrue("alwaysRetainTaskState" not in activities[1])
            self.assertTrue("autoRemoveFromRecents" not in activities[1])
            self.assertTrue("banner" not in activities[1])
            self.assertTrue("clearTaskOnLaunch" not in activities[1])
            self.assertTrue("configChanges" not in activities[1])
            self.assertTrue("documentLaunchMode" not in activities[1])
            self.assertTrue("enabled" not in activities[1])
            self.assertTrue("excludeFromRecents" not in activities[1])
            self.assertTrue("exported" not in activities[1])
            self.assertTrue("finishOnTaskLaunch" not in activities[1])
            self.assertTrue("hardwareAccelerated" not in activities[1])
            self.assertTrue("icon" not in activities[1])
            self.assertTrue("label" in activities[1])
            self.assertTrue(activities[1]["label"] == "@string/other_name" or activities[1]["label"] == "@7F040001")
            self.assertTrue("launchMode" in activities[1])
            self.assertTrue(activities[1]["launchMode"] == "singleTop" or activities[1]["launchMode"] == "1")
            self.assertTrue("maxRecents" not in activities[1])
            self.assertTrue("multiprocess" not in activities[1])
            self.assertTrue("noHistory" in activities[1])
            self.assertTrue(activities[1]["noHistory"] == "true")
            self.assertTrue("parentActivityName" in activities[1])
            self.assertEqual("com.example.app.HomeActivity", activities[1]["parentActivityName"])
            self.assertTrue("permission" not in activities[1])
            self.assertTrue("process" not in activities[1])
            self.assertTrue("relinquishTaskIdentity" not in activities[1])
            self.assertTrue("screenOrientation" not in activities[1])
            self.assertTrue("stateNotNeeded" not in activities[1])
            self.assertTrue("taskAffinity" not in activities[1])
            self.assertTrue("theme" not in activities[1])
            self.assertTrue("uiOptions" not in activities[1])
            self.assertTrue("windowSoftInputMode" not in activities[1])
            # Test meta-data parsing:
            self.assertTrue("meta-data" in activities[1])
            self.assertEqual(1, len(activities[1]["meta-data"]))
            self.assertTrue("name" in activities[1]["meta-data"][0])
            self.assertEqual("android.support.PARENT_ACTIVITY", activities[1]["meta-data"][0]["name"])
            self.assertTrue("value" in activities[1]["meta-data"][0])
            self.assertEqual("com.example.app.HomeActivity", activities[1]["meta-data"][0]["value"])
            self.assertTrue("resource" not in activities[1]["meta-data"][0])
            # Test intent-filter parsing:
            self.assertTrue("intent-filter" in activities[1])
            self.assertEqual(1, len(activities[1]["intent-filter"]))
            # priority
            self.assertTrue("priority" not in activities[1]["intent-filter"][0])
            # action
            self.assertTrue("action" in activities[1]["intent-filter"][0])
            self.assertEqual(1, len(activities[1]["intent-filter"][0]["action"]))
            self.assertEqual("android.intent.action.VIEW", activities[1]["intent-filter"][0]["action"][0])
            # category
            self.assertTrue("category" in activities[1]["intent-filter"][0])
            self.assertEqual(1, len(activities[1]["intent-filter"][0]["category"]))
            self.assertEqual("android.intent.category.DEFAULT", activities[1]["intent-filter"][0]["category"][0])
            # data
            self.assertTrue("data" in activities[1]["intent-filter"][0])
            self.assertEqual(3, len(activities[1]["intent-filter"][0]["data"]))
            self.assertTrue("scheme" in activities[1]["intent-filter"][0]["data"][0])
            self.assertEqual("content", activities[1]["intent-filter"][0]["data"][0]["scheme"])
            self.assertTrue("scheme" in activities[1]["intent-filter"][0]["data"][1])
            self.assertEqual("file", activities[1]["intent-filter"][0]["data"][1]["scheme"])
            self.assertTrue("mimeType" in activities[1]["intent-filter"][0]["data"][2])
            self.assertEqual(
                "application/vnd.android.package-archive",
                activities[1]["intent-filter"][0]["data"][2]["mimeType"]
            )

    def test_get_services(self):
        services = self.manifests["summary"].get_services()

        self.assertIsNone(services)

    def test_get_services_with_extended_processing(self):
        for man in ["extended", "binary"]:
            services = self.manifests[man].get_services()

            # Test 1st Service:
            self.assertTrue("name" in services[0])
            self.assertEqual("com.example.app.ExampleService", services[0]["name"])
            self.assertTrue("enabled" not in services[0])
            self.assertTrue("exported" not in services[0])
            self.assertTrue("icon" not in services[0])
            self.assertTrue("isolatedProcess" not in services[0])
            self.assertTrue("label" not in services[0])
            self.assertTrue("permission" not in services[0])
            self.assertTrue("process" not in services[0])
            # Test meta-data parsing:
            self.assertTrue("meta-data" not in services[0])
            # Test intent-filter parsing:
            self.assertTrue("intent-filter" not in services[0])

            # Test 2nd Service:
            self.assertTrue("name" in services[1])
            self.assertEqual("com.example.app.ExampleService2", services[1]["name"])
            self.assertTrue("enabled" in services[1])
            self.assertEqual("false", services[1]["enabled"])
            self.assertTrue("exported" in services[1])
            self.assertEqual("true", services[1]["exported"])
            self.assertTrue("icon" not in services[1])
            self.assertTrue("isolatedProcess" in services[1])
            self.assertEqual("true", services[1]["isolatedProcess"])
            self.assertTrue("label" not in services[1])
            self.assertTrue("permission" not in services[1])
            self.assertTrue("process" not in services[1])
            # Test meta-data parsing:
            self.assertTrue("meta-data" not in services[1])
            # Test intent-filter parsing:
            self.assertTrue("intent-filter" not in services[1])

            # Test 3rd Service:
            self.assertTrue("name" in services[2])
            self.assertEqual("com.example.app.ExampleService3", services[2]["name"])
            self.assertTrue("enabled" in services[2])
            self.assertEqual( "true", services[2]["enabled"])
            self.assertTrue("exported" in services[2])
            self.assertEqual("false", services[2]["exported"])
            self.assertTrue("icon" not in services[2])
            self.assertTrue("isolatedProcess" in services[2])
            self.assertEqual("false", services[2]["isolatedProcess"])
            self.assertTrue("label" not in services[2])
            self.assertTrue("permission" not in services[2])
            self.assertTrue("process" not in services[2])
            # Test meta-data parsing:
            self.assertTrue("meta-data" not in services[2])
            # Test intent-filter parsing:
            self.assertTrue("intent-filter" not in services[2])

    def test_get_broadcast_receivers(self):
        receivers = self.manifests["summary"].get_broadcast_receivers()

        self.assertIsNone(receivers)

    def test_get_broadcast_receivers_with_extended_processing(self):
        for man in ["extended", "binary"]:
            receivers = self.manifests[man].get_broadcast_receivers()

            # Test 1st BroadcastReceiver:
            self.assertTrue("name" in receivers[0])
            self.assertEqual("com.example.app.ExampleBrodcastReceiver", receivers[0]["name"])
            self.assertTrue("enabled" not in receivers[0])
            self.assertTrue("exported" not in receivers[0])
            self.assertTrue("icon" not in receivers[0])
            self.assertTrue("label" not in receivers[0])
            self.assertTrue("permission" not in receivers[0])
            self.assertTrue("process" not in receivers[0])
            # Test meta-data parsing:
            self.assertTrue("meta-data" not in receivers[0])
            # Test intent-filter parsing:
            self.assertTrue("intent-filter" not in receivers[0])

            # Test 2nd BroadcastReceiver:
            self.assertTrue("name" in receivers[1])
            self.assertEqual("com.example.app.ExampleBrodcastReceiver2", receivers[1]["name"])
            self.assertTrue("enabled" not in receivers[1])
            self.assertTrue("exported" in receivers[1])
            self.assertEqual("false", receivers[1]["exported"])
            self.assertTrue("icon" not in receivers[1])
            self.assertTrue("label" not in receivers[1])
            self.assertTrue("permission" not in receivers[1])
            self.assertTrue("process" not in receivers[1])
            # Test meta-data parsing:
            self.assertTrue("meta-data" not in receivers[1])
            # Test intent-filter parsing:
            self.assertTrue("intent-filter" in receivers[1])
            self.assertEqual(1, len(receivers[1]["intent-filter"]))
            # priority
            self.assertTrue("priority" in receivers[1]["intent-filter"][0])
            self.assertEqual("1000", receivers[1]["intent-filter"][0]["priority"])
            # action
            self.assertTrue("action" in receivers[1]["intent-filter"][0])
            self.assertEqual(2, len(receivers[1]["intent-filter"][0]["action"]))
            self.assertEqual("android.intent.action.BOOT_COMPLETED", receivers[1]["intent-filter"][0]["action"][0])
            self.assertEqual("android.intent.action.MY_PACKAGE_REPLACED", receivers[1]["intent-filter"][0]["action"][1])
            # category
            self.assertTrue("category" not in receivers[1]["intent-filter"][0])
            # data
            self.assertTrue("data" not in receivers[1]["intent-filter"][0])

            # Test 3rd BroadcastReceiver:
            self.assertTrue("name" in receivers[2])
            self.assertEqual("com.example.app.ExampleBrodcastReceiver3", receivers[2]["name"])
            self.assertTrue("enabled" in receivers[2])
            self.assertEqual("true", receivers[2]["enabled"])
            self.assertTrue("exported" in receivers[2])
            self.assertEqual("false", receivers[2]["exported"])
            self.assertTrue("icon" not in receivers[2])
            self.assertTrue("label" not in receivers[2])
            self.assertTrue("permission" not in receivers[2])
            self.assertTrue("process" not in receivers[2])
            # Test meta-data parsing:
            self.assertTrue("meta-data" not in receivers[2])
            # Test intent-filter parsing:
            self.assertTrue("intent-filter" in receivers[2])
            self.assertEqual(1, len(receivers[2]["intent-filter"]))
            # priority
            self.assertTrue("priority" in receivers[2]["intent-filter"][0])
            self.assertEqual("800", receivers[2]["intent-filter"][0]["priority"])
            # action
            self.assertTrue("action" in receivers[2]["intent-filter"][0])
            self.assertEqual(3, len(receivers[2]["intent-filter"][0]["action"]))
            self.assertEqual(
                "android.intent.action.BROADCAST_PACKAGE_REMOVED",
                receivers[2]["intent-filter"][0]["action"][0]
            )
            self.assertEqual("android.intent.action.PACKAGE_ADDED", receivers[2]["intent-filter"][0]["action"][1])
            self.assertEqual("android.intent.action.PACKAGE_REPLACED", receivers[2]["intent-filter"][0]["action"][2])
            # category
            self.assertTrue("category" not in receivers[2]["intent-filter"][0])
            # data
            self.assertTrue("data" in receivers[2]["intent-filter"][0])
            self.assertEqual(1, len(receivers[2]["intent-filter"][0]["data"]))
            self.assertTrue("scheme" in receivers[2]["intent-filter"][0]["data"][0])
            self.assertEqual("package", receivers[2]["intent-filter"][0]["data"][0]["scheme"])

            # Test 4th BroadcastReceiver:
            self.assertTrue("name" in receivers[3])
            self.assertEqual("com.example.app.ExampleBrodcastReceiver4", receivers[3]["name"])
            self.assertTrue("enabled" in receivers[3])
            self.assertEqual("false", receivers[3]["enabled"])
            self.assertTrue("exported" in receivers[3])
            self.assertEqual("true", receivers[3]["exported"])
            self.assertTrue("icon" not in receivers[3])
            self.assertTrue("label" not in receivers[3])
            self.assertTrue("permission" not in receivers[3])
            self.assertTrue("process" not in receivers[3])
            # Test meta-data parsing:
            self.assertTrue("meta-data" not in receivers[3])
            # Test intent-filter parsing:
            self.assertTrue("intent-filter" not in receivers[3])

    def test_dump(self):
        dump = self.manifests["summary"].dump()

        self.assertEqual("AndroidManifest.xml", dump["file"])
        self.assertEqual('com.example.app', dump["package"])
        self.assertEqual({"code": 1, "name": "1.0"}, dump["version"])

    def test_dump_with_extended_processing(self):
        for man in ["extended", "binary"]:
            dump = self.manifests[man].dump()

            self.assertEqual("AndroidManifest.xml", dump["file"])
            self.assertEqual('com.example.app', dump["package"])
            self.assertEqual({"code": 1, "name": "1.0"}, dump["version"])


if __name__ == "__main__":
    unittest.main()
