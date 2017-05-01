from concurrent.futures import Future
from logging import Logger
import os

from ninjadroid.concurrent.job_executor import JobExecutor
from ninjadroid.use_cases.use_case import UseCase


class LaunchDex2Jar(UseCase):
    """
    Dex2jar will generate a jar file from the classes.dex.
    """

    DEX2JAR = "ninjadroid/dex2jar/d2j-dex2jar.sh"

    def __init__(self, input_filepath: str, input_filename: str, output_directory: str, logger: Logger = None):
        self.input_filepath = input_filepath
        self.input_filename = input_filename
        self.output_directory = output_directory
        self.logger = logger
        self.executor = JobExecutor()

    def execute(self) -> Future:
        jarfile = self.input_filename + ".jar"
        if self.logger:
            self.logger.info("Creating " + self.output_directory + "/" + jarfile + "...")

        command = LaunchDex2Jar.DEX2JAR + " -f " + self.input_filepath + \
                  " -o " + self.output_directory + "/" + jarfile

        return self.executor.submit(os.system(command))
