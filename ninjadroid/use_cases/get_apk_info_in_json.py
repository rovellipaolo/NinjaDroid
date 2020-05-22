import json
import logging
from logging import Logger
import os

from ninjadroid.parsers.apk import APK

logger = logging.getLogger(__name__)


class GetApkInfoInJson:
    """
    Generate the JSON report file.
    """

    __REPORT_FILENAME_PREFIX = "report-"

    def __init__(self, logger: Logger = logger):  # noqa
        self.logger = logger

    def execute(self, apk: APK, input_filename: str,  output_directory: str):
        self.logger.info("Generating JSON report file...")
        report_filename = GetApkInfoInJson.__REPORT_FILENAME_PREFIX + input_filename + ".json"
        self.logger.info("Creating %s/%s...", output_directory, report_filename)
        with open(os.path.join(output_directory, report_filename), "w") as fp:
            apk_info = json.dumps(apk.dump(), sort_keys=True, ensure_ascii=False, indent=4)
            fp.write(apk_info)
