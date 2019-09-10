from concurrent.futures import Future
import logging
from logging import Logger
import os

from ninjadroid.parsers.apk import APK
from ninjadroid.use_cases.extract_certificate_file import ExtractCertificateFile
from ninjadroid.use_cases.extract_dex_file import ExtractDexFile
from ninjadroid.use_cases.launch_apk_tool import LaunchApkTool
from ninjadroid.use_cases.launch_dex2jar import LaunchDex2Jar
from ninjadroid.use_cases.use_case import UseCase

logger = logging.getLogger(__name__)


class ExtractApkEntries(UseCase):
    """
    Extract all the APK entries to a given output directory.
    """

    def __init__(self,
                 apk: APK,
                 input_filepath: str,
                 input_filename: str,
                 output_directory: str,
                 logger: Logger = logger):
        self.apk = apk
        self.input_filepath = input_filepath
        self.input_filename = input_filename
        self.output_directory = output_directory
        self.logger = logger

    def execute(self):
        self.create_output_directory_if_needed()
        self.launch_apktool()
        self.launch_dex2jar()
        self.extract_certificate_file()
        self.extract_dex_file()

    def create_output_directory_if_needed(self):
        if not os.path.exists(self.output_directory):
            self.logger.info("Creating " + self.output_directory + "/...")
            os.makedirs(self.output_directory)

    def launch_apktool(self) -> Future:
        return LaunchApkTool(self.input_filepath, self.output_directory, self.logger).execute()

    def launch_dex2jar(self) -> Future:
        return LaunchDex2Jar(self.input_filepath, self.input_filename, self.output_directory, self.logger).execute()

    def extract_certificate_file(self) -> Future:
        return ExtractCertificateFile(self.apk, self.output_directory, self.logger).execute()

    def extract_dex_file(self) -> Future:
        return ExtractDexFile(self.apk, self.output_directory, self.logger).execute()
