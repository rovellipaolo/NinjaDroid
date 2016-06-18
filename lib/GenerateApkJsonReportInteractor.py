import json
import os


##
# Generate the JSON report file of a given APK file and save it to a given output directory.
#
class GenerateApkJsonReportInteractor(object):
    ##
    # Class constructor.
    #
    # @param apk  The APK class object.
    # @param filepath  The absolute file path where to save the APK info.
    #
    def __init__(self, apk, filepath, logger=None):
        self.apk = apk
        self.filepath = filepath
        self.logger = logger

    def execute(self):
        if self.logger:
            self.logger.info("Creating " + self.filepath + "...")
        fp = open(os.path.join(self.filepath), "w")
        apk_info = json.dumps(self.apk.dump(), sort_keys=True, ensure_ascii=False, indent=4)
        fp.write(apk_info)
        fp.close()

