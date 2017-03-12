import json
import os

from ninjadroid.use_cases.use_case import UseCase


class GenerateApkJsonReport(UseCase):
    """
    Generate the JSON report file of a given APK file and save it to a given output directory.
    """

    __REPORT_FILENAME_PREFIX = "report-"

    def __init__(self, apk, input_filename,  output_directory, logger=None):
        self.apk = apk
        report_filename = GenerateApkJsonReport.__REPORT_FILENAME_PREFIX + input_filename + ".json"
        self.filepath = os.path.join(output_directory, report_filename)
        self.logger = logger

    def execute(self):
        if self.logger:
            self.logger.info("Creating " + self.filepath + "...")
        fp = open(os.path.join(self.filepath), "w")
        apk_info = json.dumps(self.apk.dump(), sort_keys=True, ensure_ascii=False, indent=4)
        fp.write(apk_info)
        fp.close()

