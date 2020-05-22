import logging
from logging import Logger
import os
import os.path


logger = logging.getLogger(__name__)


class LaunchDex2Jar:
    """
    Generate a JAR file from the DEX one.
    """

    __DIRECTORY = "dex2jar"
    __FILE = "d2j-dex2jar.sh"

    def __init__(self, logger: Logger = logger):  # noqa
        self.logger = logger
        self.dex2jar = os.path.join(
            os.path.dirname(__file__),
            "..",
            LaunchDex2Jar.__DIRECTORY,
            LaunchDex2Jar.__FILE
        )
        self.logger.debug("dex2jar path: %s", self.dex2jar)

    def execute(self, input_filepath: str, input_filename: str, output_directory: str):
        jarfile = input_filename + ".jar"
        self.logger.info("Executing dex2jar...")
        self.logger.info("Creating %s/%s...", output_directory, jarfile)

        command = "{} -f {} -o {}/{}".format(
            self.dex2jar,
            input_filepath,
            output_directory,
            jarfile
        )
        self.logger.debug("dex2jar command: `%s`", command)
        return os.system(command)
