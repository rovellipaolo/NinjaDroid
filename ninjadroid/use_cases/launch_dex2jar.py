from ninjadroid.use_cases.launch_shell_command import LaunchShellCommand
from ninjadroid.use_cases.use_case import UseCase


class LaunchDex2Jar(UseCase):
    """
    Dex2jar will generate a jar file from the classes.dex.
    """

    DEX2JAR = "ninjadroid/dex2jar/d2j-dex2jar.sh"

    def __init__(self, input_filepath, input_filename, output_directory, logger=None):
        self.input_filepath = input_filepath
        self.input_filename = input_filename
        self.output_directory = output_directory
        self.logger = logger

    def execute(self):
        jarfile = self.input_filename + ".jar"
        if self.logger:
            self.logger.info("Creating " + self.output_directory + "/" + jarfile + "...")
        command = LaunchDex2Jar.DEX2JAR + " -f " + self.input_filepath + \
                  " -o " + self.output_directory + "/" + jarfile
        launch_shell_command_interactor = LaunchShellCommand(command)
        launch_shell_command_interactor.execute()
