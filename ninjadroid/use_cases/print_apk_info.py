import json

from typing import Any, Optional

from ninjadroid.parsers.apk import APK


# pylint: disable=too-few-public-methods
class PrintApkInfo:
    """
    Generate the APK report and print it to stdout.
    """

    def __init__(self):
        pass

    def execute(self, apk: APK, as_json: bool):
        if as_json:
            apk_info = json.dumps(apk.dump(), sort_keys=True, ensure_ascii=False, indent=4)
            print(apk_info)
        else:
            self.print_dictionary(apk.dump())

    @staticmethod
    def print_dictionary(info: dict, depth: int = 0):
        for key, value in info.items():
            if isinstance(value, dict):
                PrintApkInfo.print_value(key, None, depth)
                PrintApkInfo.print_dictionary(value, depth+1)
            elif isinstance(value, list):
                if len(value) > 0:
                    PrintApkInfo.print_value(key, None, depth)
                    PrintApkInfo.print_list(value, depth+1)
            else:
                PrintApkInfo.print_value(key, value, depth)

    @staticmethod
    def print_list(info: list, depth: int = 0):
        for index, value in enumerate(info):
            if isinstance(value, dict):
                if index > 0:
                    print("")
                PrintApkInfo.print_dictionary(value, depth)
            else:
                PrintApkInfo.print_value(None, value, depth)

    @staticmethod
    def print_value(key: Optional[str], value: Optional[Any], depth: int = 0):
        value = PrintApkInfo.format_value(key, value, depth)
        print(value)

    @staticmethod
    def format_value(key: Optional[str], value: Optional[Any], depth: int = 0) -> str:
        if key is None:
            output = "{0} {1}".format(("\t" * depth) + "-", value)
        else:
            key = ("\t" * depth) + key + ":"
            if value is None:
                output = key
            else:
                output = "{0:8} {1}".format(key, value)
        return output
