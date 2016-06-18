##
# Extract classes.dex file to a given output directory.
#
class ExtractDexFileInteractor(object):
    ##
    # Class constructor.
    #
    # @param apk  The APK class object.
    # @param output_directory  The directory where to save the APK entries.
    #
    def __init__(self, apk, output_directory, logger=None):
        self.apk = apk
        self.output_directory = output_directory
        self.logger = logger

    def execute(self):
        if self.logger:
            self.logger.info("Creating " + self.output_directory + "/classes.dex...")
        self.apk.extract_dex_file(self.output_directory)
