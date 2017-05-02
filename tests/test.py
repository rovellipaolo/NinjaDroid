"""
TestSuite for ninjadroid.py.

RUN: python -m unittest -v tests.test
"""

import unittest

from tests.test_aapt import TestAapt
from tests.test_android_manifest import TestAndroidManifest
from tests.test_apk import TestAPK
from tests.test_cert import TestCert
from tests.test_dex import TestDex
from tests.test_file import TestFile
from tests.test_shell_command_signature import TestShellCommandSignature
from tests.test_signature import TestSignature
from tests.test_uri_signature import TestURISignature


def get_test_suite():
    """
    Retrieve the NinjaDroid TestSuite.
    :return:
    """
    suite = unittest.TestSuite()

    suite.addTest(TestFile)
    suite.addTest(TestAPK)
    suite.addTest(TestAapt)
    suite.addTest(TestAndroidManifest)
    suite.addTest(TestCert)
    suite.addTest(TestDex)
    suite.addTest(TestSignature)
    suite.addTest(TestURISignature)
    suite.addTest(TestShellCommandSignature)

    return suite


if __name__ == '__main__':
    # Test runner:
    runner = unittest.TextTestRunner()
    runner.run(get_test_suite())
