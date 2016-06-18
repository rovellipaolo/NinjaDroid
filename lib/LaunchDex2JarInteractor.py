from lib.LaunchShellCommandInteractor import LaunchShellCommandInteractor


##
# Launch dex2jar.
# Dex2jar will generate a jar file from the classes.dex.
#
class LaunchDex2JarInteractor(object):
    DEX2JAR = "lib/dex2jar-0.0.9.15/d2j-dex2jar.sh"

    ##
    # Class constructor.
    #
    # @param input_filepath  The target APK file path.
    # @param input_filename  The target APK file name.
    # @param output_directory  The directory where to save the APK entries.
    #
    def __init__(self, input_filepath, input_filename, output_directory, logger=None):
        self.input_filepath = input_filepath
        self.input_filename = input_filename
        self.output_directory = output_directory
        self.logger = logger

    def execute(self):
        jarfile = self.input_filename + ".jar"
        if self.logger:
            self.logger.info("Creating " + self.output_directory + "/" + jarfile + "...")
        command = LaunchDex2JarInteractor.DEX2JAR + " -f " + self.input_filepath + \
                  " -o " + self.output_directory + "/" + jarfile
        launch_shell_command_interactor = LaunchShellCommandInteractor(command)
        launch_shell_command_interactor.execute()
