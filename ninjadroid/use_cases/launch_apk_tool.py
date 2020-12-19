from logging import getLogger, Logger
import os
import os.path


default_logger = getLogger(__name__)


# pylint: disable=too-few-public-methods
class LaunchApkTool:
    """
    Extract the (decrypted) AndroidManifest.xml, the resources and generate the disassembled smali files.
    """

    __DIRECTORY = "apktool"
    __FILE = "apktool.jar"

    def __init__(self, logger: Logger = default_logger):
        self.logger = logger
        self.apktool = os.path.join(
            os.path.dirname(__file__),
            "..",
            LaunchApkTool.__DIRECTORY,
            LaunchApkTool.__FILE
        )
        self.logger.debug("apktool path: %s", self.apktool)

    def execute(self, input_filepath: str, output_directory: str):
        self.logger.info("Executing apktool...")
        self.logger.info("Creating %s/smali/...", output_directory)
        self.logger.info("Creating %s/AndroidManifest.xml...", output_directory)
        self.logger.info("Creating %s/res/...", output_directory)
        self.logger.info("Creating %s/assets/...", output_directory)

        command = "java -jar {} -q decode -f {} -o {}".format(
            self.apktool,
            input_filepath,
            output_directory
        )
        self.logger.debug("apktool command: `%s`", command)
        return os.system(command)
