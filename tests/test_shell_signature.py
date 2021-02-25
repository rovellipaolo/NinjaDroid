from parameterized import parameterized
import unittest

from ninjadroid.signatures.shell_signature import ShellSignature


class TestShellSignature(unittest.TestCase):
    """
    UnitTest for Shell.py.

    RUN: python -m unittest -v tests.test_shell_signature
    """

    shell = ShellSignature()

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
    def test_is_valid(self, raw_string, expected):
        result = self.shell.is_valid(raw_string)

        self.assertEqual(expected, result)

    @parameterized.expand([
        ["chmod 777", "chmod 777"],
        ["_chmod_777", "_chmod_777"],
        ["#chmod 777", "#chmod 777"],
        ["$ chmod 777", "chmod 777"],
        [" AAA chmod 777 ", "chmod 777"],
        ["ls /data/local/bin", "ls /data/local/bin"],
        ["mount -o remount", "mount -o remount"],
        ["mount -o remount,ro -t", "mount -o remount,ro -t"],
        ["mount -o remount,rw -t", "mount -o remount,rw -t"],
        ["su_bin_resid", "su_bin_resid"],
        ["/system/app/xxx.apk", "/system/app/xxx.apk"],
        ["ls /system/app/xxx.apk", "ls /system/app/xxx.apk"],
        [" ### /system/app/xxx.apk", "/system/app/xxx.apk"],
        [" - no match - ", None],
        ["http://www.domain.com", None],
        ["Mozilla/5.0 (Linux; U; Android %s) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2 (AdMob-ANDROID-%s)", None],
    ])
    def test_search(self, raw_string, expected):
        match = self.shell.search(raw_string)

        self.assertEqual(expected, match)


if __name__ == '__main__':
    unittest.main()
