from os import listdir
from os.path import join
import unittest

from lib.errors.APKParsingError import APKParsingError
from lib.errors.ParsingError import ParsingError
from lib.parsers.APK import APK


##
# UnitTest for APK.py.
#
# RUN: python -m unittest -v test.TestAPK
#
class TestAPK(unittest.TestCase):
    apks_properties = {
        "Example.apk": {
            "name": "test/data/Example.apk",
            "size": 70058,
            "md5": "c9504f487c8b51412ba4980bfe3cc15d",
            "sha1": "482a28812495b996a92191fbb3be1376193ca59b",
            "sha256": "8773441a656b60c5e18481fd5ba9c1bf350d98789b975987cb3b2b57ee44ee51",
            "sha512": "559eab9840ff2f8507842605e60bb0730442ddf9ee7ca4ab4f386f715c1a4707766065d6f0b977816886692bf88b400643979e2fd13e6999358a21cabdfb3071",
            "app_name": "Example",
            "file_list": [
                {
                    "name": "res/drawable-hdpi-v4/ic_launcher.png",
                    "size": 9193,
                    "md5": "e74dbf28ebab4e1b7442a9c78067d1c2",
                    "sha1": "450d3d44325fdf259810a60e6afa36103e186b3d",
                    "sha256": "9b2639dbfdd60e0dab70e572f39660c8dfabd19b7987a7619d770824db342925",
                    "sha512": "44050c4db6d5275b70856050c0d58d3d9892ba09bd8cf1a8343a3c6d4f2e2af6eae1f8b687efb59b7f8122e5bea1a63e08546fee35124cc0faab40ef6274ab4f",
                },
                {
                    "name": "res/drawable-hdpi-v4/ic_launcher_logo.png",
                    "size": 9193,
                    "md5": "e74dbf28ebab4e1b7442a9c78067d1c2",
                    "sha1": "450d3d44325fdf259810a60e6afa36103e186b3d",
                    "sha256": "9b2639dbfdd60e0dab70e572f39660c8dfabd19b7987a7619d770824db342925",
                    "sha512": "44050c4db6d5275b70856050c0d58d3d9892ba09bd8cf1a8343a3c6d4f2e2af6eae1f8b687efb59b7f8122e5bea1a63e08546fee35124cc0faab40ef6274ab4f",
                },
                {
                    "name": "res/drawable-ldpi-v4/ic_launcher.png",
                    "size": 2658,
                    "md5": "58b9a42eeb99fad5321208fe02f24375",
                    "sha1": "09ea65885b4080e515ef7064e816c77991c0757b",
                    "sha256": "c4f061b2c758185371f39afcb166ba039e955d3be2619ab5469a1b873f952d0d",
                    "sha512": "415ed16de6fd335b24bd985d9152323d04fc02287acd3f26fa98722832cfecf89cf2c77ad8ae3f5588acc5cac401129ac3b3d714abbf8dcc492ab2fd98f106e5",
                },
                {
                    "name": "res/drawable-ldpi-v4/ic_launcher_logo.png",
                    "size": 2658,
                    "md5": "58b9a42eeb99fad5321208fe02f24375",
                    "sha1": "09ea65885b4080e515ef7064e816c77991c0757b",
                    "sha256": "c4f061b2c758185371f39afcb166ba039e955d3be2619ab5469a1b873f952d0d",
                    "sha512": "415ed16de6fd335b24bd985d9152323d04fc02287acd3f26fa98722832cfecf89cf2c77ad8ae3f5588acc5cac401129ac3b3d714abbf8dcc492ab2fd98f106e5",
                },
                {
                    "name": "res/drawable-mdpi-v4/ic_launcher.png",
                    "size": 5057,
                    "md5": "acefc1f320111a8d71bcdb8b4aa0656c",
                    "sha1": "23730fd0d5e720d1f719be1afc8c48fa7305da6c",
                    "sha256": "05346d62d4096537906928af523ef9d5997663707a1d48e08f20992584e1424d",
                    "sha512": "59896fc52679e86898dc09b56fb53270d4297c53adee26f864657c5ef4aff9e5f5922dfa9370c3d1748068aa7b1270e0fa8a1323ce3b69c7548a50ca221befc1",
                },
                {
                    "name": "res/drawable-mdpi-v4/ic_launcher_logo.png",
                    "size": 5057,
                    "md5": "acefc1f320111a8d71bcdb8b4aa0656c",
                    "sha1": "23730fd0d5e720d1f719be1afc8c48fa7305da6c",
                    "sha256": "05346d62d4096537906928af523ef9d5997663707a1d48e08f20992584e1424d",
                    "sha512": "59896fc52679e86898dc09b56fb53270d4297c53adee26f864657c5ef4aff9e5f5922dfa9370c3d1748068aa7b1270e0fa8a1323ce3b69c7548a50ca221befc1",
                },
                {
                    "name": "res/drawable-xhdpi-v4/ic_launcher.png",
                    "size": 14068,
                    "md5": "94f5591633218c0b469b65947fd8943b",
                    "sha1": "502cd84fa444f26d7ecfdf4a355064867977f236",
                    "sha256": "29d15992424b40757135f47fc8ddd15e30c7774646b37755608f7cfec1df7d8a",
                    "sha512": "d5b48e065a614c5a2400b6565dc36777d9923d8d5154487113dd1f46b05d36d1db3f28fb72f61a68fcbd225c93495541579574e6611f650fe2857767412c3b1f",
                },
                {
                    "name": "res/drawable-xhdpi-v4/ic_launcher_logo.png",
                    "size": 14068,
                    "md5": "94f5591633218c0b469b65947fd8943b",
                    "sha1": "502cd84fa444f26d7ecfdf4a355064867977f236",
                    "sha256": "29d15992424b40757135f47fc8ddd15e30c7774646b37755608f7cfec1df7d8a",
                    "sha512": "d5b48e065a614c5a2400b6565dc36777d9923d8d5154487113dd1f46b05d36d1db3f28fb72f61a68fcbd225c93495541579574e6611f650fe2857767412c3b1f",
                },
                {
                    "name": "res/layout/main.xml",
                    "size": 552,
                    "md5": "8cdec0105448937475e45e22c80fd611",
                    "sha1": "51ebf14ed21238f7d147a6744cae18c0f55fcbe6",
                    "sha256": "e74db1ac37395ca9fd25b93261d3ab76ed7dfc9b355ea63d856afc7453313738",
                    "sha512": "2d2147365b8b00f2db7498b7f0ed8a360fc15bd43dfd3704b4b1cb912619d9ff1bc35837eb1e601ea6d1aa3a8c0d555f2105d6ed37de919fa128568527765d63",
                },
                {
                    "name": "resources.arsc",
                    "size": 1640,
                    "md5": "2886f2825eef3b5c4478852935c68640",
                    "sha1": "1eff126288b4bea6fa78eb79832d6a7fa098695e",
                    "sha256": "ac46f54fa12dc20e94619465482186047505fb9f27508861220063c93f0c6c4e",
                    "sha512": "da8c41d0c27839ed89cb06a2f89f6993bd88f5179e97f3291f0e17348868b3e9c106e96f482ecd86f11808170937773e7599ccd338900908359e870ea5446169",
                },
                {
                    "name": "META-INF/MANIFEST.MF",
                    "size": 1061,
                    "md5": "6098a6409625f1c0d97cd33c13ad300c",
                    "sha1": "ccfe31190feb259a4a56599ad1403a956f6944b5",
                    "sha256": "8a18f285481346919f4df55f576ee504bf5abecb068a2d642fdef17f3b5cd631",
                    "sha512": "17a68bf605aff149aa31e1b0b81af3d3f74f939e1cb7a10f3eddf84775f901b09ba9722efad1265b0057cdfcd12c6fac701067993081620b00bbfcc4efff3599",
                },
                {
                    "name": "META-INF/CERT.SF",
                    "size": 1114,
                    "md5": "fb02917b68510e413a06e52873802bcd",
                    "sha1": "dfb7bbb487010b980152610fe7d669c1b4f626be",
                    "sha256": "e2fa373f8b065ef7c78387ab9242e98dd19bdeb2b768295506295f7beb0bfe3f",
                    "sha512": "3aa74603588ca5c563b6586d1216dc6cea3b8d2a1a47eb189197e8f20cd7508d3e652c7ff849261e95cff52451476b2993caadf051fdf66cc01f5e6e16b180fc",
                }
            ],
        },
    }

    @classmethod
    def setUpClass(cls):
        cls.apks = {}

        for filename in listdir(join('test', 'data')):
            if filename in cls.apks_properties:
                cls.apks[filename] = APK(join('test', 'data', filename))
                #print(cls.apks[filename].dump())

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        for filename in self.apks:
            self.assertTrue(self.apks[filename] is not None)
            self.assertTrue(type(self.apks[filename]) is APK)

        # Test the class raise when a non-existing file is given:
        with self.assertRaises(ParsingError):
            APK(join('test', 'data', 'aaa_this_is_a_non_existent_file_xxx'))

        # Test the class raise when a non-existing file is given:
        with self.assertRaises(APKParsingError):
            APK(join('test', 'data', 'AndroidManifest.xml'))
            APK(join('test', 'data', 'CERT.RSA'))
            APK(join('test', 'data', 'classes.dex'))

    def test_get_raw_file(self):
        for filename in self.apks:
            self.assertTrue(len(self.apks[filename].get_raw_file()) > 0)

    def test_get_file_name(self):
        for filename in self.apks:
            self.assertTrue(self.apks[filename].get_file_name() == self.apks_properties[filename]['name'])

    def test_get_size(self):
        for filename in self.apks:
            self.assertTrue(self.apks[filename].get_size() == self.apks_properties[filename]['size'])

    def test_get_md5(self):
        for filename in self.apks:
            self.assertTrue(self.apks[filename].get_md5() == self.apks_properties[filename]['md5'])

    def test_get_sha1(self):
        for filename in self.apks:
            self.assertTrue(self.apks[filename].get_sha1() == self.apks_properties[filename]['sha1'])

    def test_get_sha256(self):
        for filename in self.apks:
            self.assertTrue(self.apks[filename].get_sha256() == self.apks_properties[filename]['sha256'])

    def test_get_sha512(self):
        for filename in self.apks:
            self.assertTrue(self.apks[filename].get_sha512() == self.apks_properties[filename]['sha512'])

    def test_get_file_list(self):
        for filename in self.apks:
            file_list = self.apks[filename].get_file_list()
            self.assertTrue(len(file_list) == len(self.apks_properties[filename]['file_list']))
            for i in range(len(file_list)):
                self.assertTrue(file_list[i].get_file_name() == self.apks_properties[filename]['file_list'][i]["name"])
                self.assertTrue(file_list[i].get_size() == self.apks_properties[filename]['file_list'][i]["size"])
                self.assertTrue(file_list[i].get_md5() == self.apks_properties[filename]['file_list'][i]["md5"])
                self.assertTrue(file_list[i].get_sha1() == self.apks_properties[filename]['file_list'][i]["sha1"])
                self.assertTrue(file_list[i].get_sha256() == self.apks_properties[filename]['file_list'][i]["sha256"])
                self.assertTrue(file_list[i].get_sha512() == self.apks_properties[filename]['file_list'][i]["sha512"])

    def test_get_app_name(self):
        for filename in self.apks:
            self.assertTrue(self.apks[filename].get_app_name() == self.apks_properties[filename]['app_name'])


if __name__ == '__main__':
    unittest.main()
