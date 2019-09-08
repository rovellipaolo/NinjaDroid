from concurrent.futures import Future
import json
import logging
from logging import Logger
import os

from ninjadroid.concurrent.job_executor import JobExecutor
from ninjadroid.parsers.apk import APK
from ninjadroid.use_cases.use_case import UseCase

logger = logging.getLogger(__name__)


class GetApkInfoInJson(UseCase):
    """
    Generate the JSON report file of a given APK file and save it to a given output directory.
    """

    __REPORT_FILENAME_PREFIX = "report-"

    def __init__(self, apk: APK, input_filename: str,  output_directory: str, logger: Logger = logger):
        self.apk = apk
        report_filename = GetApkInfoInJson.__REPORT_FILENAME_PREFIX + input_filename + ".json"
        self.filepath = os.path.join(output_directory, report_filename)
        self.logger = logger
        self.executor = JobExecutor()

    def execute(self) -> Future:
        self.logger.info("Creating " + self.filepath + "...")
        return self.executor.submit(self.job())

    def job(self):
        fp = open(os.path.join(self.filepath), "w")
        apk_info = json.dumps(self.apk.dump(), sort_keys=True, ensure_ascii=False, indent=4)
        fp.write(apk_info)
        fp.close()
