from lib.LaunchShellCommandInteractor import LaunchShellCommandInteractor


##
# Launch apktool.
# Apktool will extract the (decrypted) AndroidManifest.xml, the resources and to generate the disassembled smali files.
#
class LaunchApkToolInteractor(object):
    APKTOOL_PATH = "lib/apktool1.5.2/apktool.jar"

    ##
    # Class constructor.
    #
    # @param input_filepath  The target APK file path.
    # @param output_directory  The directory where to save the APK entries.
    #
    def __init__(self, input_filepath, output_directory, logger=None):
        self.input_filepath = input_filepath
        self.output_directory = output_directory
        self.logger = logger

    def execute(self):
        if self.logger:
            self.logger.info("Creating " + self.output_directory + "/smali/...")
            self.logger.info("Creating " + self.output_directory + "/AndroidManifest.xml...")
            self.logger.info("Creating " + self.output_directory + "/res/...")
            self.logger.info("Creating " + self.output_directory + "/assets/...")
        command = "java -jar " + LaunchApkToolInteractor.APKTOOL_PATH + \
                  " -q d -f " + self.input_filepath + " " + self.output_directory
        launch_shell_command_interactor = LaunchShellCommandInteractor(command)
        launch_shell_command_interactor.execute()
