from concurrent.futures import Future
from logging import Logger
import os
import shutil
from zipfile import ZipFile

from ninjadroid.concurrent.job_executor import JobExecutor
from ninjadroid.parsers.apk import APK
from ninjadroid.use_cases.use_case import UseCase


class ExtractDexFile(UseCase):
    """
    Extract classes.dex file to a given output directory.
    """

    def __init__(self, apk: APK, output_directory: str, logger: Logger = None):
        self.apk = apk
        self.output_directory = output_directory
        self.logger = logger
        self.executor = JobExecutor()

    def execute(self) -> Future:
        if self.logger:
            self.logger.info("Creating " + self.output_directory + "/classes.dex...")
        return self.executor.submit(self.job(self.output_directory))

    def job(self, output_directory: str):
        """
        Extract the classes.dex file of the APK package.

        :param output_directory: The directory where to save the classes.dex file.
        """
        with ZipFile(self.apk.get_file_name()) as package:
            dex = self.apk.get_dex().get_file_name()
            dex_abspath = os.path.join(output_directory, dex)
            with package.open(dex) as dex, open(dex_abspath, 'wb') as fp:
                shutil.copyfileobj(dex, fp)
