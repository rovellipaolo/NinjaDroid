import os

from lib.GenerateApkHtmlReportInteractor import GenerateApkHtmlReportInteractor
from lib.GenerateApkJsonReportInteractor import GenerateApkJsonReportInteractor


##
# Generate the JSON and HTML report files of a given APK file and save it to a given output directory.
#
class GenerateApkReportsInteractor(object):
    REPORT_FILENAME_PREFIX = "report-"

    ##
    # Class constructor.
    #
    # @param apk  The APK class object.
    # @param input_filename  The target APK file name.
    # @param output_directory  The directory where to save the APK entries and info.
    #
    def __init__(self, apk, input_filename,  output_directory, logger=None):
        self.apk = apk
        self.input_filename = input_filename
        self.output_directory = output_directory
        self.logger = logger

    def execute(self):
        self.generate_json_report()
        self.generate_html_report()

    def generate_json_report(self):
        report_filename = GenerateApkReportsInteractor.REPORT_FILENAME_PREFIX + self.input_filename + ".json"
        report_filepath = os.path.join(self.output_directory, report_filename)
        generate_apk_json_report_interactor = GenerateApkJsonReportInteractor(self.apk, report_filepath, self.logger)
        generate_apk_json_report_interactor.execute()

    def generate_html_report(self):
        report_filename = GenerateApkReportsInteractor.REPORT_FILENAME_PREFIX + self.input_filename + ".html"
        report_filepath = os.path.join(self.output_directory, report_filename)
        generate_apk_html_report_interactor = GenerateApkHtmlReportInteractor(self.apk, report_filepath, self.logger)
        generate_apk_html_report_interactor.execute()
