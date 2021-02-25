from parameterized import parameterized
import unittest

from ninjadroid.signatures.signature import Signature


class TestSignature(unittest.TestCase):
    """
    UnitTest for signature.py.

    RUN: python -m unittest -v tests.test_signature
    """

    signature = Signature()

    @parameterized.expand([
        ["apk", True],
        ["root", True],
        ["hack", True],
        ["esploid", True],
        ["tattoo", True],
        ["AdMob", True],
        ["http://www.domain.com", False],
        ["adbd", False],
        ["/system/bin", False],
        ["VersionConstants.java", False],
    ])
    def test_is_valid(self, raw_string, expected):
        result = self.signature.is_valid(raw_string)

        self.assertEqual(expected, result)

    @parameterized.expand([
        ["\"mOnRootMePleaseDialogClickListener", "\"mOnRootMePleaseDialogClickListener"],
        ["str_root_already_rooted", "str_root_already_rooted"],
        ["tv_gen_exploit_msg", "tv_gen_exploit_msg"],
        ["tattoo_hack_g6561203.ko", "tattoo_hack_g6561203.ko"],
        ["6ixxx", "6ixxx"],
        ["#preserveType: %b, type: %s, obj: %s", "#preserveType: %b, type: %s, obj: %s"],
        ["Mozilla/5.0 (Linux; U; Android %s) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2 (AdMob-ANDROID-%s)", "Mozilla/5.0 (Linux; U; Android %s) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2 (AdMob-ANDROID-%s)"],
        ["8Lcom/corner23/android/universalandroot/UniversalAndroot;", "8Lcom/corner23/android/universalandroot/UniversalAndroot;"],
        [" - no match - ", None],
        ["http://www.domain.com", None],
        ["chmod 777", None],
    ])
    def test_search(self, raw_string, expected):
        match = self.signature.search(raw_string)

        self.assertEqual(expected, match)


if __name__ == '__main__':
    unittest.main()
