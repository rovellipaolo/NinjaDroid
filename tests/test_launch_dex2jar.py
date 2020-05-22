import unittest
from unittest.mock import Mock, patch

from ninjadroid.use_cases.launch_dex2jar import LaunchDex2Jar


class TestLaunchDex2Jar(unittest.TestCase):
    """
    UnitTest for launch_dex2jar.py.

    RUN: python -m unittest -v tests.test_launch_dex2jar
    """

    ANY_PATH = "any-path"
    ANY_FILE = "any-file"
    ANY_DIRECTORY = "any-directory"
    ANY_DEX2JAR = "dex2jar/d2j-dex2jar.sh"

    @patch('ninjadroid.use_cases.launch_dex2jar.os.path.join', Mock(return_value=ANY_DEX2JAR))
    def setUp(self):
        self.sut = LaunchDex2Jar()

    @patch('ninjadroid.use_cases.launch_dex2jar.os')
    def test_execute(self, mock_os):
        self.sut.execute(
            input_filepath=TestLaunchDex2Jar.ANY_PATH,
            input_filename=TestLaunchDex2Jar.ANY_FILE,
            output_directory=TestLaunchDex2Jar.ANY_DIRECTORY
        )

        mock_os.system.assert_called_once_with(
            "{} -f {} -o {}/{}.jar".format(
                TestLaunchDex2Jar.ANY_DEX2JAR,
                TestLaunchDex2Jar.ANY_PATH,
                TestLaunchDex2Jar.ANY_DIRECTORY,
                TestLaunchDex2Jar.ANY_FILE
            )
        )


if __name__ == "__main__":
    unittest.main()
