import os
from time import sleep

from ninjadroid.use_cases.extract_certificate_file import ExtractCertificateFile
from ninjadroid.use_cases.extract_dex_file import ExtractDexFile
from ninjadroid.use_cases.launch_apk_tool import LaunchApkTool
from ninjadroid.use_cases.launch_dex2jar import LaunchDex2Jar
from ninjadroid.use_cases.use_case import UseCase


class ExtractApkEntries(UseCase):
    """
    Extract all the APK entries to a given output directory.
    """

    def __init__(self, apk, input_filepath, input_filename,  output_directory, logger=None):
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
            if self.logger:
                self.logger.info("Creating " + self.output_directory + "/...")
            os.makedirs(self.output_directory)

    def launch_apktool(self):
        launch_apk_tool_interactor = LaunchApkTool(
            self.input_filepath,
            self.output_directory,
            self.logger)
        launch_apk_tool_interactor.execute()
        # Give apktool some time:
        sleep(1)

    def launch_dex2jar(self):
        launch_dex2jar_interactor = LaunchDex2Jar(
            self.input_filepath,
            self.input_filename,
            self.output_directory,
            self.logger)
        launch_dex2jar_interactor.execute()
        # Give dex2jar some time:
        sleep(5)

    def extract_certificate_file(self):
        extract_certificate_file_interactor = ExtractCertificateFile(
            self.apk,
            self.output_directory,
            self.logger)
        extract_certificate_file_interactor.execute()

    def extract_dex_file(self):
        extract_dex_file_interactor = ExtractDexFile(
            self.apk,
            self.output_directory,
            self.logger)
        extract_dex_file_interactor.execute()
