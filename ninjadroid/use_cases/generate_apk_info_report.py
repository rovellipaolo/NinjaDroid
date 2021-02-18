import json
from logging import getLogger, Logger
import os

from ninjadroid.parsers.apk import APK

default_logger = getLogger(__name__)


# pylint: disable=too-few-public-methods
class GenerateApkInfoReport:
    """
    Generate the APK report and store it a JSON file.
    """

    __REPORT_FILENAME_PREFIX = "report-"

    def __init__(self, logger: Logger = default_logger):
        self.logger = logger

    def execute(self, apk: APK, input_filename: str,  output_directory: str):
        self.logger.info("Generating JSON report file...")
        report_filename = GenerateApkInfoReport.__REPORT_FILENAME_PREFIX + input_filename + ".json"
        self.logger.info("Creating %s/%s...", output_directory, report_filename)
        with open(os.path.join(output_directory, report_filename), "w") as file:
            apk_info = json.dumps(apk.dump(), sort_keys=True, ensure_ascii=False, indent=4)
            file.write(apk_info)
