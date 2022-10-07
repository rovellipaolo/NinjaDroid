from difflib import unified_diff
import inspect
import json
from subprocess import PIPE, Popen
import sys
from typing import Any, Dict


class RegressionSuite:
    """
    Generic regression suite.
    """

    def __init__(self):
        pass

    def set_up(self):
        """
        Set up the regression test suite.
        """
        pass  # pylint: disable=unnecessary-pass

    def tear_down(self):
        """
        Tear down the regression test suite.
        """
        pass  # pylint: disable=unnecessary-pass

    @staticmethod
    def read_plain_text_file(path: str, overrides: Dict[int, str] = None) -> str:
        with open(path, "r") as file:
            plain_text = file.read()
            if overrides:
                plain_text = RegressionSuite.__get_overridden_plain_text(plain_text, overrides)
            return plain_text

    @staticmethod
    def __get_overridden_plain_text(content: str, overrides: Dict[int, str]) -> Dict:
        overridden = content.split("\n")
        for index, value in overrides.items():
            overridden[index] = value
        return "\n".join(overridden)

    @staticmethod
    def read_json_file(path: str, overrides: Dict[str, Any] = None) -> str:
        file = RegressionSuite.read_plain_text_file(path)
        file_as_json = json.loads(file)
        if overrides:
            file_as_json = RegressionSuite.__get_overridden_json(file_as_json, overrides)
        return json.dumps(file_as_json)

    @staticmethod
    def __get_overridden_json(content: Dict, overrides: Dict[str, Any]) -> Dict:
        overridden = content
        for key, value in overrides.items():
            if isinstance(value, dict):
                overridden[key] = RegressionSuite.__get_overridden_json(overridden[key], value)
            else:
                overridden[key] = value
        return overridden

    @staticmethod
    def execute_command(command: str) -> str:
        with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
            return process.communicate()[0].decode("utf-8")

    @staticmethod
    def assert_plain_text_equal(expected: str, actual: str, multiline: bool = True):
        if not multiline:
            expected = " ".join(expected.split())
            actual = " ".join(actual.split())
        equal = expected == actual
        if equal:
            print(".", end ="")
            return
        print("E", end ="")
        RegressionSuite.print_diff(expected, actual)
        sys.exit(1)

    @staticmethod
    def assert_json_equal(expected: str, actual: str):
        expected_json = json.loads(expected)
        actual_json = json.loads(actual)
        if expected_json == actual_json:
            print(".", end ="")
            return
        print("E", end ="")
        # Update expected and actual by sorting the JSON keys (needed for the diff below):
        expected = json.dumps(expected_json, indent=4, sort_keys=True)
        actual = json.dumps(actual_json, indent=4, sort_keys=True)
        RegressionSuite.print_diff(expected, actual)
        sys.exit(1)

    @staticmethod
    def print_diff(expected: str, actual: str):
        print("")
        diff = list(unified_diff(expected.split("\n"), actual.split("\n"), fromfile='before', tofile='after'))
        for line in diff:
            print(line)

    @staticmethod
    def test(function):
        """
        Decorator for regression tests (i.e. @RegressionSuite.test annotation).
        """
        def wrapped(suite: RegressionSuite):
            function(suite)
        return wrapped


def run(suite: RegressionSuite):
    """
    Simple runner for regression test suites:
      - call suite set_up()
      - call all suite methods decorated with a @RegressionSuite.test annotation
      - call suite tear_down()
    """
    suite.set_up()

    cls = type(suite)
    source = inspect.getsourcelines(cls)[0]
    for i, line in enumerate(source):
        line = line.strip()
        if line.split('(')[0].strip() == '@RegressionSuite.test':
            next_line = source[i + 1]
            name = next_line.split('def')[1].split('(')[0].strip()
            getattr(cls, name)(cls)

    suite.tear_down()
    print()
