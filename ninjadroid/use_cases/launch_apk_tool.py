from ninjadroid.use_cases.launch_shell_command import LaunchShellCommand
from ninjadroid.use_cases.use_case import UseCase


class LaunchApkTool(UseCase):
    """
    Apktool will extract the (decrypted) AndroidManifest.xml, the resources and generate the disassembled smali files.
    """

    APKTOOL_PATH = "ninjadroid/apktool/apktool.jar"

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
        command = "java -jar " + LaunchApkTool.APKTOOL_PATH + \
                  " -q d -f " + self.input_filepath + " " + self.output_directory
        launch_shell_command_interactor = LaunchShellCommand(command)
        launch_shell_command_interactor.execute()
