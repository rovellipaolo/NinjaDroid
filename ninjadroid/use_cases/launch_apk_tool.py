from concurrent.futures import Future
import logging
from logging import Logger
import os
import os.path

from ninjadroid.concurrent.job_executor import JobExecutor
from ninjadroid.use_cases.use_case import UseCase

logger = logging.getLogger(__name__)


class LaunchApkTool(UseCase):
    """
    Apktool will extract the (decrypted) AndroidManifest.xml, the resources and generate the disassembled smali files.
    """

    APKTOOL_PATH = os.path.join(os.path.dirname(__file__), "..", "apktool", "apktool.jar")

    def __init__(self, input_filepath: str, output_directory: str, logger: Logger = logger):
        self.input_filepath = input_filepath
        self.output_directory = output_directory
        self.logger = logger
        self.executor = JobExecutor()
        self.logger.debug("apktool path: %s", self.APKTOOL_PATH)

    def execute(self) -> Future:
        self.logger.info("Executing apktool...")
        self.logger.info("Creating " + self.output_directory + "/smali/...")
        self.logger.info("Creating " + self.output_directory + "/AndroidManifest.xml...")
        self.logger.info("Creating " + self.output_directory + "/res/...")
        self.logger.info("Creating " + self.output_directory + "/assets/...")

        command = "java -jar {} -q decode -f {} -o {}".format(
            LaunchApkTool.APKTOOL_PATH,
            self.input_filepath,
            self.output_directory
        )
        self.logger.debug("apktool command: `%s`", command)

        return self.executor.submit(os.system(command))
