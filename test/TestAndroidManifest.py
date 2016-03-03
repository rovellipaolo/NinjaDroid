##
# UnitTest for AndroidManifest.py.
#
# RUN: python -m unittest -v test.TestAndroidManifest
#

from os.path import join
import unittest

from lib.errors.AndroidManifestParsingError import AndroidManifestParsingError
from lib.errors.ParsingError import ParsingError
from lib.parsers.AndroidManifest import AndroidManifest


class TestAndroidManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifests = {}

        try:
            cls.manifests['clean'] = AndroidManifest(join('test', 'data', 'AndroidManifest.xml'), False)
            #print(self.manifests['clean'].dump())

            cls.manifests['binary'] = AndroidManifest(join('test', 'data', 'AndroidManifestBinary.xml'), True)
            #print(self.manifests['binary'].dump())
        except:
            pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        self.assertTrue(self.manifests['clean'] is not None)
        self.assertTrue(type(self.manifests['clean']) is AndroidManifest)
        self.assertTrue(self.manifests['binary'] is not None)
        self.assertTrue(type(self.manifests['binary']) is AndroidManifest)

        # Test the class raise when a non-existing file is given:
        with self.assertRaises(ParsingError):
            AndroidManifest(join('test', 'data', 'aaa_this_is_a_non_existent_file_xxx'))

        # Test the class raise when a non-AndroidManifest.xml file is given:
        with self.assertRaises(AndroidManifestParsingError):
            AndroidManifest(join('test', 'data', 'classes.dex'), False)
            AndroidManifest(join('test', 'data', 'classes.dex'), True)
            AndroidManifest(join('test', 'data', 'CERT.RSA'), False)
            AndroidManifest(join('test', 'data', 'CERT.RSA'), True)

    def test_get_raw_file(self):
        self.assertTrue(len(self.manifests['clean'].get_raw_file()) > 0)
        self.assertTrue(len(self.manifests['binary'].get_raw_file()) > 0)

    def test_get_file_name(self):
        self.assertTrue(self.manifests['clean'].get_file_name() == "AndroidManifest.xml")
        self.assertTrue(self.manifests['binary'].get_file_name() == "AndroidManifest.xml")

    def test_get_size(self):
        self.assertTrue(self.manifests['clean'].get_size() == 3358)
        self.assertTrue(self.manifests['binary'].get_size() == 6544)

    def test_get_md5(self):
        self.assertTrue(self.manifests['clean'].get_md5() == "c098fdd0a5dcf615118dad5457a2d016")
        self.assertTrue(self.manifests['binary'].get_md5() == "1f97f7e7ca62f39f8f81d79b1b540c37")

    def test_get_sha1(self):
        self.assertTrue(self.manifests['clean'].get_sha1() == "d69bbde630c8a5623b72a16d46b579432f2c944d")
        self.assertTrue(self.manifests['binary'].get_sha1() == "011316a011e5b8738c12c662cb0b0a6ffe04ca74")

    def test_get_sha256(self):
        self.assertTrue(self.manifests['clean'].get_sha256() == "a042569824ff2e268fdde5b8e00981293b27fe8a2a1dc72aa791e579f80bd720")
        self.assertTrue(self.manifests['binary'].get_sha256() == "7c8011a46191ecb368bf2e0104049abeb98bae8a7b1fa3328ff050aed85b1347")

    def test_get_sha512(self):
        self.assertTrue(self.manifests['clean'].get_sha512() == "8875e2d19725c824c93e9f4e45b9ebcd599bffafde1af4b98975a2d6e497fde76870e5129eef289a25328562f4f21d9ff214db95dcd3ddb3b58f358ec362d78a")
        self.assertTrue(self.manifests['binary'].get_sha512() == "8c7c1ede610f9c6613418b46a52a196ad6d5e8cc067c2f26b931738ad8087f998d9ea95e80ec4352c95fbdbb93a4f29c646973535068a3a3d584da95480ab45f")

    def test_get_package_name(self):
        for man in self.manifests:
            self.assertTrue(self.manifests[man].get_package_name() == "com.example.app")

    def test_get_version(self):
        for man in self.manifests:
            version = self.manifests[man].get_version()
            self.assertTrue(version['code'] == 1)
            self.assertTrue(version['name'] == "1.0")

    def test_get_sdk_version(self):
        for man in self.manifests:
            sdk = self.manifests[man].get_sdk_version()
            self.assertTrue(('target' in sdk) and (sdk['target'] == "20"))
            self.assertTrue(('min' in sdk) and (sdk['min'] == "10"))
            self.assertTrue(('max' in sdk) and (sdk['max'] == "20"))

    def test_get_permissions(self):
        permissions = ['android.permission.INTERNET', 'android.permission.READ_EXTERNAL_STORAGE', 'android.permission.RECEIVE_BOOT_COMPLETED', 'android.permission.WRITE_EXTERNAL_STORAGE']
        permissions.sort()

        for man in self.manifests:
            self.assertTrue(self.manifests[man].get_permissions() == permissions)

    def test_get_number_of_permissions(self):
        for man in self.manifests:
            self.assertTrue(self.manifests[man].get_number_of_permissions() == 4)

    def test_get_activities(self):
        for man in self.manifests:
            activities = self.manifests[man].get_activities()

            # Test 1st Activity:
            self.assertTrue('name' in activities[0])
            self.assertTrue(activities[0]['name'] == "com.example.app.HomeActivity")
            self.assertTrue('allowEmbedded' not in activities[0])
            self.assertTrue('allowTaskReparenting' not in activities[0])
            self.assertTrue('alwaysRetainTaskState' not in activities[0])
            self.assertTrue('autoRemoveFromRecents' not in activities[0])
            self.assertTrue('banner' not in activities[0])
            self.assertTrue('clearTaskOnLaunch' not in activities[0])
            self.assertTrue('configChanges' in activities[0])
            self.assertTrue(activities[0]['configChanges'] == "orientation|screenSize" or activities[0]['configChanges'] == "0x00000480")
            self.assertTrue('documentLaunchMode' not in activities[0])
            self.assertTrue('enabled' not in activities[0])
            self.assertTrue('excludeFromRecents' not in activities[0])
            self.assertTrue('exported' not in activities[0])
            self.assertTrue('finishOnTaskLaunch' not in activities[0])
            self.assertTrue('hardwareAccelerated' not in activities[0])
            self.assertTrue('icon' not in activities[0])
            self.assertTrue('label' in activities[0])
            self.assertTrue(activities[0]['label'] == "@string/app_name" or activities[0]['label'] == "@7F040000")
            self.assertTrue('launchMode' in activities[0])
            self.assertTrue(activities[0]['launchMode'] == "singleTop" or activities[0]['launchMode'] == "1")
            self.assertTrue('maxRecents' not in activities[0])
            self.assertTrue('multiprocess' not in activities[0])
            self.assertTrue('noHistory' not in activities[0])
            self.assertTrue('parentActivityName' not in activities[0])
            self.assertTrue('permission' not in activities[0])
            self.assertTrue('process' not in activities[0])
            self.assertTrue('relinquishTaskIdentity' not in activities[0])
            self.assertTrue('screenOrientation' not in activities[0])
            self.assertTrue('stateNotNeeded' not in activities[0])
            self.assertTrue('taskAffinity' not in activities[0])
            self.assertTrue('theme' not in activities[0])
            self.assertTrue('uiOptions' not in activities[0])
            self.assertTrue('windowSoftInputMode' not in activities[0])
            # Test meta-data parsing:
            self.assertTrue('meta-data' not in activities[0])
            # Test intent-filter parsing:
            self.assertTrue('intent-filter' in activities[0])
            self.assertTrue(len(activities[0]['intent-filter']) == 1)
            # priority
            self.assertTrue('priority' not in activities[0]['intent-filter'][0])
            # action
            self.assertTrue('action' in activities[0]['intent-filter'][0])
            self.assertTrue(len(activities[0]['intent-filter'][0]['action']) == 1)
            self.assertTrue(activities[0]['intent-filter'][0]['action'][0] == "android.intent.action.MAIN")
            # category
            self.assertTrue('category' in activities[0]['intent-filter'][0])
            self.assertTrue(len(activities[0]['intent-filter'][0]['category']) == 1)
            self.assertTrue(activities[0]['intent-filter'][0]['category'][0] == "android.intent.category.LAUNCHER")
            # data
            self.assertTrue('data' not in activities[0]['intent-filter'][0])

            # Test 2nd Activity:
            self.assertTrue('name' in activities[1])
            self.assertTrue(activities[1]['name'] == "com.example.app.OtherActivity")
            self.assertTrue('allowEmbedded' not in activities[1])
            self.assertTrue('allowTaskReparenting' not in activities[1])
            self.assertTrue('alwaysRetainTaskState' not in activities[1])
            self.assertTrue('autoRemoveFromRecents' not in activities[1])
            self.assertTrue('banner' not in activities[1])
            self.assertTrue('clearTaskOnLaunch' not in activities[1])
            self.assertTrue('configChanges' not in activities[1])
            self.assertTrue('documentLaunchMode' not in activities[1])
            self.assertTrue('enabled' not in activities[1])
            self.assertTrue('excludeFromRecents' not in activities[1])
            self.assertTrue('exported' not in activities[1])
            self.assertTrue('finishOnTaskLaunch' not in activities[1])
            self.assertTrue('hardwareAccelerated' not in activities[1])
            self.assertTrue('icon' not in activities[1])
            self.assertTrue('label' in activities[1])
            self.assertTrue(activities[1]['label'] == "@string/other_name" or activities[1]['label'] == "@7F040001")
            self.assertTrue('launchMode' in activities[1])
            self.assertTrue(activities[1]['launchMode'] == "singleTop" or activities[1]['launchMode'] == "1")
            self.assertTrue('maxRecents' not in activities[1])
            self.assertTrue('multiprocess' not in activities[1])
            self.assertTrue('noHistory' in activities[1])
            self.assertTrue(activities[1]['noHistory'] == "true")
            self.assertTrue('parentActivityName' in activities[1])
            self.assertTrue(activities[1]['parentActivityName'] == "com.example.app.HomeActivity")
            self.assertTrue('permission' not in activities[1])
            self.assertTrue('process' not in activities[1])
            self.assertTrue('relinquishTaskIdentity' not in activities[1])
            self.assertTrue('screenOrientation' not in activities[1])
            self.assertTrue('stateNotNeeded' not in activities[1])
            self.assertTrue('taskAffinity' not in activities[1])
            self.assertTrue('theme' not in activities[1])
            self.assertTrue('uiOptions' not in activities[1])
            self.assertTrue('windowSoftInputMode' not in activities[1])
            # Test meta-data parsing:
            self.assertTrue('meta-data' in activities[1])
            self.assertTrue(len(activities[1]['meta-data']) == 1)
            self.assertTrue('name' in activities[1]['meta-data'][0])
            self.assertTrue(activities[1]['meta-data'][0]['name'] == "android.support.PARENT_ACTIVITY")
            self.assertTrue('value' in activities[1]['meta-data'][0])
            self.assertTrue(activities[1]['meta-data'][0]['value'] == "com.example.app.HomeActivity")
            self.assertTrue('resource' not in activities[1]['meta-data'][0])
            # Test intent-filter parsing:
            self.assertTrue('intent-filter' in activities[1])
            self.assertTrue(len(activities[1]['intent-filter']) == 1)
            # priority
            self.assertTrue('priority' not in activities[1]['intent-filter'][0])
            # action
            self.assertTrue('action' in activities[1]['intent-filter'][0])
            self.assertTrue(len(activities[1]['intent-filter'][0]['action']) == 1)
            self.assertTrue(activities[1]['intent-filter'][0]['action'][0] == "android.intent.action.VIEW")
            # category
            self.assertTrue('category' in activities[1]['intent-filter'][0])
            self.assertTrue(len(activities[1]['intent-filter'][0]['category']) == 1)
            self.assertTrue(activities[1]['intent-filter'][0]['category'][0] == "android.intent.category.DEFAULT")
            # data
            self.assertTrue('data' in activities[1]['intent-filter'][0])
            self.assertTrue(len(activities[1]['intent-filter'][0]['data']) == 3)
            self.assertTrue('scheme' in activities[1]['intent-filter'][0]['data'][0])
            self.assertTrue(activities[1]['intent-filter'][0]['data'][0]['scheme'] == "content")
            self.assertTrue('scheme' in activities[1]['intent-filter'][0]['data'][1])
            self.assertTrue(activities[1]['intent-filter'][0]['data'][1]['scheme'] == "file")
            self.assertTrue('mimeType' in activities[1]['intent-filter'][0]['data'][2])
            self.assertTrue(activities[1]['intent-filter'][0]['data'][2]['mimeType'] == "application/vnd.android.package-archive")

    def test_get_number_of_activities(self):
        for man in self.manifests:
            self.assertTrue(self.manifests[man].get_number_of_activities() == 2)

    def test_get_services(self):
        for man in self.manifests:
            services = self.manifests[man].get_services()

            # Test 1st Service:
            self.assertTrue('name' in services[0])
            self.assertTrue(services[0]['name'] == "com.example.app.ExampleService")
            self.assertTrue('enabled' not in services[0])
            self.assertTrue('exported' not in services[0])
            self.assertTrue('icon' not in services[0])
            self.assertTrue('isolatedProcess' not in services[0])
            self.assertTrue('label' not in services[0])
            self.assertTrue('permission' not in services[0])
            self.assertTrue('process' not in services[0])
            # Test meta-data parsing:
            self.assertTrue('meta-data' not in services[0])
            # Test intent-filter parsing:
            self.assertTrue('intent-filter' not in services[0])

            # Test 2nd Service:
            self.assertTrue('name' in services[1])
            self.assertTrue(services[1]['name'] == "com.example.app.ExampleService2")
            self.assertTrue('enabled' in services[1])
            self.assertTrue(services[1]['enabled'] == "false")
            self.assertTrue('exported' in services[1])
            self.assertTrue(services[1]['exported'] == "true")
            self.assertTrue('icon' not in services[1])
            self.assertTrue('isolatedProcess' in services[1])
            self.assertTrue(services[1]['isolatedProcess'] == "true")
            self.assertTrue('label' not in services[1])
            self.assertTrue('permission' not in services[1])
            self.assertTrue('process' not in services[1])
            # Test meta-data parsing:
            self.assertTrue('meta-data' not in services[1])
            # Test intent-filter parsing:
            self.assertTrue('intent-filter' not in services[1])

            # Test 3rd Service:
            self.assertTrue('name' in services[2])
            self.assertTrue(services[2]['name'] == "com.example.app.ExampleService3")
            self.assertTrue('enabled' in services[2])
            self.assertTrue(services[2]['enabled'] == "true")
            self.assertTrue('exported' in services[2])
            self.assertTrue(services[2]['exported'] == "false")
            self.assertTrue('icon' not in services[2])
            self.assertTrue('isolatedProcess' in services[2])
            self.assertTrue(services[2]['isolatedProcess'] == "false")
            self.assertTrue('label' not in services[2])
            self.assertTrue('permission' not in services[2])
            self.assertTrue('process' not in services[2])
            # Test meta-data parsing:
            self.assertTrue('meta-data' not in services[2])
            # Test intent-filter parsing:
            self.assertTrue('intent-filter' not in services[2])

    def test_get_number_of_services(self):
        for man in self.manifests:
            self.assertTrue(self.manifests[man].get_number_of_services() == 3)

    def test_get_broadcast_receivers(self):
        for man in self.manifests:
            receivers = self.manifests[man].get_broadcast_receivers()

            # Test 1st BroadcastReceiver:
            self.assertTrue('name' in receivers[0])
            self.assertTrue(receivers[0]['name'] == "com.example.app.ExampleBrodcastReceiver")
            self.assertTrue('enabled' not in receivers[0])
            self.assertTrue('exported' not in receivers[0])
            self.assertTrue('icon' not in receivers[0])
            self.assertTrue('label' not in receivers[0])
            self.assertTrue('permission' not in receivers[0])
            self.assertTrue('process' not in receivers[0])
            # Test meta-data parsing:
            self.assertTrue('meta-data' not in receivers[0])
            # Test intent-filter parsing:
            self.assertTrue('intent-filter' not in receivers[0])

            # Test 2nd BroadcastReceiver:
            self.assertTrue('name' in receivers[1])
            self.assertTrue(receivers[1]['name'] == "com.example.app.ExampleBrodcastReceiver2")
            self.assertTrue('enabled' not in receivers[1])
            self.assertTrue('exported' in receivers[1])
            self.assertTrue(receivers[1]['exported'] == "false")
            self.assertTrue('icon' not in receivers[1])
            self.assertTrue('label' not in receivers[1])
            self.assertTrue('permission' not in receivers[1])
            self.assertTrue('process' not in receivers[1])
            # Test meta-data parsing:
            self.assertTrue('meta-data' not in receivers[1])
            # Test intent-filter parsing:
            self.assertTrue('intent-filter' in receivers[1])
            self.assertTrue(len(receivers[1]['intent-filter']) == 1)
            # priority
            self.assertTrue('priority' in receivers[1]['intent-filter'][0])
            self.assertTrue(receivers[1]['intent-filter'][0]['priority'] == "1000")
            # action
            self.assertTrue('action' in receivers[1]['intent-filter'][0])
            self.assertTrue(len(receivers[1]['intent-filter'][0]['action']) == 2)
            self.assertTrue(receivers[1]['intent-filter'][0]['action'][0] == "android.intent.action.BOOT_COMPLETED")
            self.assertTrue(receivers[1]['intent-filter'][0]['action'][1] == "android.intent.action.MY_PACKAGE_REPLACED")
            # category
            self.assertTrue('category' not in receivers[1]['intent-filter'][0])
            # data
            self.assertTrue('data' not in receivers[1]['intent-filter'][0])

            # Test 3rd BroadcastReceiver:
            self.assertTrue('name' in receivers[2])
            self.assertTrue(receivers[2]['name'] == "com.example.app.ExampleBrodcastReceiver3")
            self.assertTrue('enabled' in receivers[2])
            self.assertTrue(receivers[2]['enabled'] == "true")
            self.assertTrue('exported' in receivers[2])
            self.assertTrue(receivers[2]['exported'] == "false")
            self.assertTrue('icon' not in receivers[2])
            self.assertTrue('label' not in receivers[2])
            self.assertTrue('permission' not in receivers[2])
            self.assertTrue('process' not in receivers[2])
            # Test meta-data parsing:
            self.assertTrue('meta-data' not in receivers[2])
            # Test intent-filter parsing:
            self.assertTrue('intent-filter' in receivers[2])
            self.assertTrue(len(receivers[2]['intent-filter']) == 1)
            # priority
            self.assertTrue('priority' in receivers[2]['intent-filter'][0])
            self.assertTrue(receivers[2]['intent-filter'][0]['priority'] == "800")
            # action
            self.assertTrue('action' in receivers[2]['intent-filter'][0])
            self.assertTrue(len(receivers[2]['intent-filter'][0]['action']) == 3)
            self.assertTrue(receivers[2]['intent-filter'][0]['action'][0] == "android.intent.action.BROADCAST_PACKAGE_REMOVED")
            self.assertTrue(receivers[2]['intent-filter'][0]['action'][1] == "android.intent.action.PACKAGE_ADDED")
            self.assertTrue(receivers[2]['intent-filter'][0]['action'][2] == "android.intent.action.PACKAGE_REPLACED")
            # category
            self.assertTrue('category' not in receivers[2]['intent-filter'][0])
            # data
            self.assertTrue('data' in receivers[2]['intent-filter'][0])
            self.assertTrue(len(receivers[2]['intent-filter'][0]['data']) == 1)
            self.assertTrue('scheme' in receivers[2]['intent-filter'][0]['data'][0])
            self.assertTrue(receivers[2]['intent-filter'][0]['data'][0]['scheme'] == "package")

            # Test 4th BroadcastReceiver:
            self.assertTrue('name' in receivers[3])
            self.assertTrue(receivers[3]['name'] == "com.example.app.ExampleBrodcastReceiver4")
            self.assertTrue('enabled' in receivers[3])
            self.assertTrue(receivers[3]['enabled'] == "false")
            self.assertTrue('exported' in receivers[3])
            self.assertTrue(receivers[3]['exported'] == "true")
            self.assertTrue('icon' not in receivers[3])
            self.assertTrue('label' not in receivers[3])
            self.assertTrue('permission' not in receivers[3])
            self.assertTrue('process' not in receivers[3])
            # Test meta-data parsing:
            self.assertTrue('meta-data' not in receivers[3])
            # Test intent-filter parsing:
            self.assertTrue('intent-filter' not in receivers[3])

    def test_get_number_of_broadcast_receivers(self):
        for man in self.manifests:
            self.assertTrue(self.manifests[man].get_number_of_broadcast_receivers() == 4)


if __name__ == '__main__':
    unittest.main()
