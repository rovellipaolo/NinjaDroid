from concurrent.futures import Future
import logging
from logging import Logger
import os
import shutil
from zipfile import ZipFile

from ninjadroid.concurrent.job_executor import JobExecutor
from ninjadroid.parsers.apk import APK
from ninjadroid.use_cases.use_case import UseCase

logger = logging.getLogger(__name__)


class ExtractDexFile(UseCase):
    """
    Extract classes.dex file to a given output directory.
    """

    def __init__(self, apk: APK, output_directory: str, logger: Logger = logger):
        self.apk = apk
        self.output_directory = output_directory
        self.logger = logger
        self.executor = JobExecutor()

    def execute(self) -> Future:
        self.logger.info("Extracting DEX files to %s", self.output_directory)
        return self.executor.submit(self.job(self.output_directory))

    def job(self, output_directory: str):
        """
        Extract the DEX files from the APK package.

        :param output_directory: The directory where to save the DEX files.
        """
        apk_filename = self.apk.get_file_name()
        with ZipFile(apk_filename) as package:
            for dex_file in self.apk.get_dex_files():
                dex_filename = dex_file.get_file_name()
                self.logger.debug("Extracting %s from %s", dex_filename, apk_filename)
                dex_abspath = os.path.join(output_directory, dex_filename)
                output_directory = os.path.split(dex_abspath)[0]
                os.makedirs(output_directory, exist_ok=True)

                with package.open(dex_filename) as dex:
                    with open(dex_abspath, 'wb') as fp:
                        self.logger.info("Extracting DEX %s", dex_filename)
                        shutil.copyfileobj(dex, fp)
