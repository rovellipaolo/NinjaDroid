import os

from lib.reports.HtmlReport import HtmlReport


##
# Generate the HTML report file of a given APK file and save it to a given output directory.
#
class GenerateApkHtmlReportInteractor(object):
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
        apk_info = HtmlReport.generate_html_report(self.apk)
        fp.write(apk_info)
        fp.close()
