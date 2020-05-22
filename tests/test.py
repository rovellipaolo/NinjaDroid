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
from tests.test_extract_certificate_file import TestExtractCertificateFile
from tests.test_extract_dex_file import TestExtractDexFile
from tests.test_file import TestFile
from tests.test_get_apk_info_in_html import TestGetApkInfoInHtml
from tests.test_get_apk_info_in_json import TestGetApkInfoInJson
from tests.test_launch_apk_tool import TestLaunchApkTool
from tests.test_launch_dex2jar import TestLaunchDex2Jar
from tests.test_shell_command_signature import TestShellCommandSignature
from tests.test_signature import TestSignature
from tests.test_uri_signature import TestURISignature


def get_test_suite():
    """
    Retrieve the NinjaDroid TestSuite.

    RUN: python -m unittest -v tests.test
    """
    suite = unittest.TestSuite()

    suite.addTest(TestAPK)
    suite.addTest(TestAapt)
    suite.addTest(TestAndroidManifest)
    suite.addTest(TestCert)
    suite.addTest(TestDex)
    suite.addTest(TestExtractCertificateFile)
    suite.addTest(TestExtractDexFile)
    suite.addTest(TestFile)
    suite.addTest(TestGetApkInfoInHtml)
    suite.addTest(TestGetApkInfoInJson)
    suite.addTest(TestLaunchApkTool)
    suite.addTest(TestLaunchDex2Jar)
    suite.addTest(TestSignature)
    suite.addTest(TestURISignature)
    suite.addTest(TestShellCommandSignature)

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(get_test_suite())
