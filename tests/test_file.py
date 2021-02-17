from os import listdir
from os.path import join
import unittest

from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.file import File


# TODO: refactor these tests...
class TestFile(unittest.TestCase):
    """
    UnitTest for file.py.

    RUN: python -m unittest -v tests.test_file
    """

    files_properties = {
        "Example.apk": {
            "name": "tests/data/Example.apk",
            "size": 70058,
            "md5": "c9504f487c8b51412ba4980bfe3cc15d",
            "sha1": "482a28812495b996a92191fbb3be1376193ca59b",
            "sha256": "8773441a656b60c5e18481fd5ba9c1bf350d98789b975987cb3b2b57ee44ee51",
            "sha512": "559eab9840ff2f8507842605e60bb0730442ddf9ee7ca4ab4f386f715c1a4707766065d6f0b977816886692bf88b400643979e2fd13e6999358a21cabdfb3071",
        },
        "AndroidManifest.xml": {
            "name": "tests/data/AndroidManifest.xml",
            "size": 3358,
            "md5": "c098fdd0a5dcf615118dad5457a2d016",
            "sha1": "d69bbde630c8a5623b72a16d46b579432f2c944d",
            "sha256": "a042569824ff2e268fdde5b8e00981293b27fe8a2a1dc72aa791e579f80bd720",
            "sha512": "8875e2d19725c824c93e9f4e45b9ebcd599bffafde1af4b98975a2d6e497fde76870e5129eef289a25328562f4f21d9ff214db95dcd3ddb3b58f358ec362d78a",
        },
        "AndroidManifestBinary.xml": {
            "name": "tests/data/AndroidManifestBinary.xml",
            "size": 6544,
            "md5": "1f97f7e7ca62f39f8f81d79b1b540c37",
            "sha1": "011316a011e5b8738c12c662cb0b0a6ffe04ca74",
            "sha256": "7c8011a46191ecb368bf2e0104049abeb98bae8a7b1fa3328ff050aed85b1347",
            "sha512": "8c7c1ede610f9c6613418b46a52a196ad6d5e8cc067c2f26b931738ad8087f998d9ea95e80ec4352c95fbdbb93a4f29c646973535068a3a3d584da95480ab45f",
        },
        "CERT.RSA": {
            "name": "tests/data/CERT.RSA",
            "size": 906,
            "md5": "5026e73a2f0d8091aaf7908cffbc425e",
            "sha1": "37210614d362672e19cdd7940b7f5037de6cbcb8",
            "sha256": "0ba1a5ba50b277bb37d05e8b9d2c6422aad49b90c08e7136d2d7c204ceaaf412",
            "sha512": "e16ce3b471f10043be642472dc4f0156dccb434331c0c1ca19470b7dc0d025d4bb512fc5e77e78011e704b69fe0872e6fd7dee648e87401062f59149695f36f5",
        },
        "classes.dex": {
            "name": "tests/data/classes.dex",
            "size": 2132,
            "md5": "7bc52ece5249ccd2d72c4360f9be2ca5",
            "sha1": "89476799bf92798047ca026c922a5bc33983b008",
            "sha256": "3f543c68c4c059548cec619a68f329010d797e5e4c00aa46cd34c0d19cabe056",
            "sha512": "0725f961bc1bac47eb8dd045c2f0a0cf5475fd77089af7ddc3098e341a95d8b5624969b6fa47606a05d5a6adf9d74d0c52562ea41a376bd3d7d0aa3695ca2e22",
        },
    }

    @classmethod
    def setUpClass(cls):
        cls.files = {}

        for filename in listdir(join("tests", "data")):
            if filename in cls.files_properties:
                cls.files[filename] = File(join("tests", "data", filename))
                # print(cls.files[filename].dump())

    def test_init(self):
        for filename in self.files:
            files = self.files[filename]

            self.assertTrue(files is not None)
            self.assertTrue(type(files) is File)

    def test_init_with_non_existing_file(self):
        with self.assertRaises(ParsingError):
            File(join("tests", "data", "aaa_this_is_a_non_existent_file_xxx"))

    def test_get_raw_file(self):
        for filename in self.files:
            raw_file = self.files[filename].get_raw_file()

            self.assertTrue(len(raw_file) > 0)

    def test_get_file_name(self):
        for filename in self.files:
            name = self.files[filename].get_file_name()

            self.assertEqual(self.files_properties[filename]["name"], name)

    def test_get_size(self):
        for filename in self.files:
            size = self.files[filename].get_size()

            self.assertEqual(self.files_properties[filename]["size"], size)

    def test_get_md5(self):
        for filename in self.files:
            md5 = self.files[filename].get_md5()

            self.assertEqual(self.files_properties[filename]["md5"], md5)

    def test_get_sha1(self):
        for filename in self.files:
            sha1 = self.files[filename].get_sha1()

            self.assertEqual(self.files_properties[filename]["sha1"], sha1)

    def test_get_sha256(self):
        for filename in self.files:
            sha256 = self.files[filename].get_sha256()

            self.assertEqual(self.files_properties[filename]["sha256"], sha256)

    def test_get_sha512(self):
        for filename in self.files:
            sha512 = self.files[filename].get_sha512()

            self.assertEqual(self.files_properties[filename]["sha512"], sha512)

    def test_dump(self):
        for filename in self.files:
            dump = self.files[filename].dump()

            self.assertEqual(self.files_properties[filename]["name"], dump["file"])
            self.assertEqual(self.files_properties[filename]["size"], dump["size"])
            self.assertEqual(self.files_properties[filename]["md5"], dump["md5"])
            self.assertEqual(self.files_properties[filename]["sha1"], dump["sha1"])
            self.assertEqual(self.files_properties[filename]["sha256"], dump["sha256"])
            self.assertEqual(self.files_properties[filename]["sha512"], dump["sha512"])


if __name__ == "__main__":
    unittest.main()
