from concurrent.futures import Future
import logging
from logging import Logger
import os
import os.path

from ninjadroid.concurrent.job_executor import JobExecutor
from ninjadroid.use_cases.use_case import UseCase

logger = logging.getLogger(__name__)


class LaunchDex2Jar(UseCase):
    """
    Dex2jar will generate a jar file from the classes.dex.
    """

    DEX2JAR = os.path.join(os.path.dirname(__file__), "..", "dex2jar", "d2j-dex2jar.sh")

    def __init__(self, input_filepath: str, input_filename: str, output_directory: str, logger: Logger = logger):
        self.input_filepath = input_filepath
        self.input_filename = input_filename
        self.output_directory = output_directory
        self.logger = logger
        self.executor = JobExecutor()

    def execute(self) -> Future:
        jarfile = self.input_filename + ".jar"
        self.logger.info(
            "Running dex2jar on %s, creating %s/%s...",
            self.input_filepath,
            self.output_directory,
            jarfile
        )

        command = LaunchDex2Jar.DEX2JAR + " -f " + self.input_filepath + \
                  " -o " + self.output_directory + "/" + jarfile

        return self.executor.submit(os.system(command))
