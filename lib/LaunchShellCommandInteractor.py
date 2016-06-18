import subprocess


##
# Launch a given shell command.
#
class LaunchShellCommandInteractor(object):
    ##
    # Class constructor.
    #
    # @param command  The command to be executed.
    #
    def __init__(self, command):
        self.command = command

    def execute(self):
        subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=None, shell=True)
