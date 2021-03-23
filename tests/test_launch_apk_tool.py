import unittest
from unittest.mock import Mock, patch

from ninjadroid.use_cases.launch_apk_tool import LaunchApkTool


class TestLaunchApkTool(unittest.TestCase):
    """
    Test LaunchApkTool use case.
    """

    ANY_PATH = "any-path"
    ANY_DIRECTORY = "any-directory"
    ANY_APKTOOL = "apktool/apktool.jar"

    @patch('ninjadroid.use_cases.launch_apk_tool.os.path.join', Mock(return_value=ANY_APKTOOL))
    def setUp(self):
        self.sut = LaunchApkTool()

    @patch('ninjadroid.use_cases.launch_apk_tool.os')
    def test_execute(self, mock_os):
        self.sut.execute(input_filepath=TestLaunchApkTool.ANY_PATH, output_directory=TestLaunchApkTool.ANY_DIRECTORY)

        mock_os.system.assert_called_once_with(
            "java -jar {} -q decode -f {} -o {}".format(
                TestLaunchApkTool.ANY_APKTOOL,
                TestLaunchApkTool.ANY_PATH,
                TestLaunchApkTool.ANY_DIRECTORY
            )
        )


if __name__ == "__main__":
    unittest.main()
