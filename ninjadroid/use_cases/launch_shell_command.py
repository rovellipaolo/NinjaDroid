import subprocess

from ninjadroid.use_cases.use_case import UseCase


class LaunchShellCommand(UseCase):
    def __init__(self, command):
        self.command = command

    def execute(self):
        subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=None, shell=True)
