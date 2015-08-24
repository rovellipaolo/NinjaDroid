##
# TestSuite for ninjadroid.py.
#
# RUN: python -m unittest -v test.Test
#

import unittest

from test.TestAapt import TestAapt
from test.TestAndroidManifest import TestAndroidManifest, ErrorAndroidManifestParsing
from test.TestAPK import TestAPK
from test.TestCERT import TestCERT
from test.TestDex import TestDex
from test.TestFile import TestFile, ErrorFileParsing
from test.TestShell import TestShell
from test.TestSignature import TestSignature
from test.TestURI import TestURI


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
    suite.addTest(TestURI)
    suite.addTest(TestShell)

    return suite


if __name__ == '__main__':
    # Test runner:
    runner = unittest.TextTestRunner()
    runner.run(get_test_suite())
