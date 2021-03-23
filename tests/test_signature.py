import unittest
from parameterized import parameterized

from ninjadroid.signatures.signature import Signature


class TestSignature(unittest.TestCase):
    """
    Test Signature parser.
    """

    sut = Signature()

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
        result = self.sut.is_valid(raw_string)

        self.assertEqual(expected, result)

    @parameterized.expand([
        ["\"mOnRootMePleaseDialogClickListener", "\"mOnRootMePleaseDialogClickListener", True],
        ["str_root_already_rooted", "str_root_already_rooted", True],
        ["tv_gen_exploit_msg", "tv_gen_exploit_msg", True],
        ["tattoo_hack_g6561203.ko", "tattoo_hack_g6561203.ko", True],
        ["6ixxx", "6ixxx", True],
        ["#preserveType: %b, type: %s, obj: %s", "#preserveType: %b, type: %s, obj: %s", True],
        [
            "Mozilla/5.0 (Linux; U; Android %s) Version/3.0.4 Mobile Safari/523.12.2 (AdMob-ANDROID-%s)",
            "Mozilla/5.0 (Linux; U; Android %s) Version/3.0.4 Mobile Safari/523.12.2 (AdMob-ANDROID-%s)",
            True
        ],
        [
            "8Lcom/corner23/android/universalandroot/UniversalAndroot;",
            "8Lcom/corner23/android/universalandroot/UniversalAndroot;",
            True
        ],
        [" - no match - ", None, False],
        ["http://www.domain.com", None, False],
        ["chmod 777", None, False],
    ])
    def test_search(self, pattern, expected_match, expected_is_valid):
        match, is_valid = self.sut.search(pattern)

        self.assertEqual(match, expected_match)
        self.assertEqual(is_valid, expected_is_valid)


if __name__ == '__main__':
    unittest.main()
