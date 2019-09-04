from concurrent.futures import Future
from logging import Logger
import os
import os.path

from ninjadroid.concurrent.job_executor import JobExecutor
from ninjadroid.use_cases.use_case import UseCase


class LaunchApkTool(UseCase):
    """
    Apktool will extract the (decrypted) AndroidManifest.xml, the resources and generate the disassembled smali files.
    """

    APKTOOL_PATH = os.path.join(os.path.dirname(__file__), "..", "apktool", "apktool.jar")

    def __init__(self, input_filepath: str, output_directory: str, logger: Logger = None):
        self.input_filepath = input_filepath
        self.output_directory = output_directory
        self.logger = logger
        self.executor = JobExecutor()

    def execute(self) -> Future:
        if self.logger:
            self.logger.info("Creating " + self.output_directory + "/smali/...")
            self.logger.info("Creating " + self.output_directory + "/AndroidManifest.xml...")
            self.logger.info("Creating " + self.output_directory + "/res/...")
            self.logger.info("Creating " + self.output_directory + "/assets/...")

        command = "java -jar " + LaunchApkTool.APKTOOL_PATH + \
                  " -q d -f " + self.input_filepath + " " + self.output_directory

        return self.executor.submit(os.system(command))
