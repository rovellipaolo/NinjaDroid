from subprocess import PIPE
from unittest.mock import ANY, Mock

def any_popen(response: str) -> Mock:
    popen = Mock()
    popen.communicate.return_value = (response, "")
    popen.__enter__ = lambda self: self
    popen.__exit__ = lambda self, type, value, traceback: self.kill()
    return popen

def assert_popen_called_once(popen: Mock):
    popen.assert_called_once_with(ANY, stdout=PIPE, stderr=None, shell=True)

def assert_popen_called_once_with(popen: Mock, command: str):
    popen.assert_called_once_with(command, stdout=PIPE, stderr=None, shell=True)
