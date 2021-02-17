import unittest

from ninjadroid.signatures.signature import Signature


class TestSignature(unittest.TestCase):
    """
    UnitTest for signature.py.

    RUN: python -m unittest -v tests.test_signature
    """

    valid_commands = [
        "apk",
        "root",
        "hack",
        "esploid",
        "tattoo",
        "AdMob",
    ]

    invalid_commands = [
        "http://www.domain.com",
        "adbd",
        "/system/bin",
        "VersionConstants.java"
    ]

    strings_containing_commands = {
        '"mOnRootMePleaseDialogClickListener': "\"mOnRootMePleaseDialogClickListener",
        'str_root_already_rooted': "str_root_already_rooted",
        'tv_gen_exploit_msg': "tv_gen_exploit_msg",
        'tattoo_hack_g6561203.ko': "tattoo_hack_g6561203.ko",
        '6ixxx': "6ixxx",
        '#preserveType: %b, type: %s, obj: %s': "#preserveType: %b, type: %s, obj: %s",
        'Mozilla/5.0 (Linux; U; Android %s) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2 (AdMob-ANDROID-%s)': "Mozilla/5.0 (Linux; U; Android %s) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2 (AdMob-ANDROID-%s)",
        '8Lcom/corner23/android/universalandroot/UniversalAndroot;': "8Lcom/corner23/android/universalandroot/UniversalAndroot;",
    }

    @classmethod
    def setUpClass(cls):
        cls.signature = Signature()

    def test_is_valid(self):
        for string in TestSignature.valid_commands:
            is_valid = self.signature.is_valid(string)

            self.assertTrue(is_valid, "Signature for " + string + " should be valid")

        for string in TestSignature.invalid_commands:
            is_valid = self.signature.is_valid(string)

            self.assertFalse(is_valid, "Signature for " + string + " should not be valid")
        pass

    def test_get_matches_in_string(self):
        for string in TestSignature.strings_containing_commands:
            matches = self.signature.get_matches_in_string(string)

            self.assertEqual(TestSignature.strings_containing_commands[string], matches)


if __name__ == '__main__':
    unittest.main()
