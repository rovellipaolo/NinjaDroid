##
# TestSuite for ninjadroid.py.
#
# RUN: python -m unittest -v test.Test
#

import unittest

from test.TestAapt import TestAapt
from test.TestAndroidManifest import TestAndroidManifest
from test.TestAPK import TestAPK
from test.TestCERT import TestCERT
from test.TestDex import TestDex
from test.TestFile import TestFile
from test.TestShellCommandSignature import TestShellCommandSignature
from test.TestSignature import TestSignature
from test.TestURISignature import TestURISignature


##
# Retrieve the NinjaDroid TestSuite.
#
def get_test_suite():
    suite = unittest.TestSuite()

    suite.addTest(TestFile)
    suite.addTest(TestAPK)
    suite.addTest(TestAapt)
    suite.addTest(TestAndroidManifest)
    suite.addTest(TestCERT)
    suite.addTest(TestDex)
    suite.addTest(TestSignature)
    suite.addTest(TestURISignature)
    suite.addTest(TestShellCommandSignature)

    return suite


if __name__ == '__main__':
    # Test runner:
    runner = unittest.TextTestRunner()
    runner.run(get_test_suite())
