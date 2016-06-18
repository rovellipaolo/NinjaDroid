##
# Extract CERT.RSA/DSA file to a given output directory.
#
class ExtractCertificateFileInteractor(object):
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
            self.logger.info("Creating " + self.output_directory + "/CERT.RSA...")
        self.apk.extract_cert_file(self.output_directory)
