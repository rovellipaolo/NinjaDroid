import unittest

from lib.signatures.ShellCommandSignature import ShellCommandSignature


##
# UnitTest for Shell.py.
#
# RUN: python -m unittest -v test.TestShell
#
class TestShellCommandSignature(unittest.TestCase):
    valid_commands = [
        "/bin",
        "/data",
        "/data/local/bin",
        "/data/local/sbin",
        "/sbin",
        "/system",
        "/system/app",
        "/system/bin",
        "/system/sbin",
        "su",
        "_su_",
        "am",
        "cd",
        "chmod",
        "chown",
        "cmp",
        "dalvikvm",
        "exit",
        "iptables",
        "kill",
        "ls",
        "mkdir",
        "mount",
        "mv",
        "ping",
        "pm",
        "rm",
        "rmdir",
        "service",
        "servicemanager",
    ]

    invalid_commands = [
        "http://www.domain.com",
        "apk",
        "VersionConstants.java"
    ]

    strings_containing_commands = {
        'chmod 777': "chmod 777",
        '_chmod_777': "_chmod_777",
        '#chmod 777': "#chmod 777",
        '$ chmod 777': "chmod 777",
        ' AAA chmod 777 ': "chmod 777",
        'ls /data/local/bin': "ls /data/local/bin",
        'mount -o remount': "mount -o remount",
        'mount -o remount,ro -t': "mount -o remount,ro -t",
        'mount -o remount,rw -t': "mount -o remount,rw -t",
        'su_bin_resid': "su_bin_resid",
        '/system/app/xxx.apk': "/system/app/xxx.apk",
        'ls /system/app/xxx.apk': "ls /system/app/xxx.apk",
        ' ### /system/app/xxx.apk': "/system/app/xxx.apk",
    }

    @classmethod
    def setUpClass(cls):
        cls.shell = ShellCommandSignature()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_valid(self):
        for command in TestShellCommandSignature.valid_commands:
            print("Testing '" + command + "'...")
            self.assertTrue(self.shell.is_valid(command))

        for command in TestShellCommandSignature.invalid_commands:
            print("Testing '" + command + "'...")
            self.assertFalse(self.shell.is_valid(command))
        pass

    def test_get_matches_in_string(self):
        for string in TestShellCommandSignature.strings_containing_commands:
            print("Testing '" + string + "'...")
            self.assertTrue(self.shell.get_matches_in_string(string) ==
                            TestShellCommandSignature.strings_containing_commands[string])


if __name__ == '__main__':
    unittest.main()
