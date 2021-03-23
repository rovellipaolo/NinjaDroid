import unittest
from parameterized import parameterized

from ninjadroid.signatures.shell_signature import ShellSignature


class TestShellSignature(unittest.TestCase):
    """
    Test ShellSignature parser.
    """

    sut = ShellSignature()

    @parameterized.expand([
        ["/bin", True],
        ["/data", True],
        ["/data/local/bin", True],
        ["/data/local/sbin", True],
        ["/sbin", True],
        ["/system", True],
        ["/system/app", True],
        ["/system/bin", True],
        ["/system/sbin", True],
        ["su", True],
        ["_su_", True],
        ["am", True],
        ["cd", True],
        ["chmod", True],
        ["chown", True],
        ["cmp", True],
        ["dalvikvm", True],
        ["exit", True],
        ["iptables", True],
        ["kill", True],
        ["ls", True],
        ["mkdir", True],
        ["mount", True],
        ["mv", True],
        ["ping", True],
        ["pm", True],
        ["rm", True],
        ["rmdir", True],
        ["service", True],
        ["servicemanager", True],
        ["http://www.domain.com", False],
        ["apk", False],
        ["VersionConstants.java", False],
    ])
    def test_is_valid(self, pattern, expected):
        result = self.sut.is_valid(pattern)

        self.assertEqual(expected, result)

    @parameterized.expand([
        ["chmod 777", "chmod 777", True],
        ["_chmod_777", "_chmod_777", True],
        ["#chmod 777", "#chmod 777", True],
        ["$ chmod 777", "chmod 777", True],
        [" AAA chmod 777 ", "chmod 777", True],
        ["ls /data/local/bin", "ls /data/local/bin", True],
        ["mount -o remount", "mount -o remount", True],
        ["mount -o remount,ro -t", "mount -o remount,ro -t", True],
        ["mount -o remount,rw -t", "mount -o remount,rw -t", True],
        ["su_bin_resid", "su_bin_resid", True],
        ["/system/app/xxx.apk", "/system/app/xxx.apk", True],
        ["ls /system/app/xxx.apk", "ls /system/app/xxx.apk", True],
        [" ### /system/app/xxx.apk", "/system/app/xxx.apk", True],
        [" - no match - ", None, False],
        ["http://www.domain.com", None, False],
        ["Mozilla/5.0 (Linux; U; Android %s) Version/3.0.4 Mobile Safari/523.12.2 (AdMob-ANDROID-%s)", None, False],
    ])
    def test_search(self, pattern, expected_match, expected_is_valid):
        match, is_valid = self.sut.search(pattern)

        self.assertEqual(match, expected_match)
        self.assertEqual(is_valid, expected_is_valid)


if __name__ == '__main__':
    unittest.main()
