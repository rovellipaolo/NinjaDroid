import logging
import os.path
import re
from subprocess import PIPE, Popen
from typing import Dict, Optional, List

global_logger = logging.getLogger(__name__)


class Aapt:
    """
    Parser for the Android Asset Packaging Tool (aapt).
    """

    __AAPT_EXEC_PATH = os.path.join(os.path.dirname(__file__), "aapt")
    __LABEL_APPLICATION = "^application: .*label='([^']*)' .*"
    __LABEL_LAUNCHABLE_ACTIVITY = "^launchable-activity: .*label='([^']*)'.*"
    __LABEL_PACKAGE_NAME = "package:(?:.*) name="
    __LABEL_PACKAGE_VERSION_CODE = "package:(?:.*) versionCode="
    __LABEL_PACKAGE_VERSION_NAME = "package:(?:.*) versionName="
    __LABEL_SDK_MAX_VERSION = "maxSdkVersion:"
    __LABEL_SDK_MIN_VERSION = "sdkVersion:"
    __LABEL_SDK_TARGET_VERSION = "targetSdkVersion:"
    __LABEL_PERMISSION_NAME = "uses-permission: name="

    def __init__(self, logger=global_logger):
        self.logger = logger
        self.logger.debug("aapt exec path: %s", self.__AAPT_EXEC_PATH)

    @classmethod
    def get_app_name(cls, filepath: str) -> Dict:
        try:
            info = cls._dump_badging(filepath)
        except RuntimeError:
            return ""
        return cls._extract_app_name(info)

    @classmethod
    def get_apk_info(cls, filepath: str) -> Dict:
        apk = {
            "package_name": "",
            "version": {
                "code": "",
                "name": "",
            },
            "sdk": {},
        }

        try:
            info = cls._dump_badging(filepath)
        except RuntimeError:
            return apk

        apk["package_name"] = cls._extract_package_name(info)
        apk["version"]["name"] = cls._extract_version_name(info)

        version_code = cls._extract_version_code(info)
        if version_code is None:
            version_code = ""
        apk["version"]["code"] = version_code

        sdk = cls._extract_sdk_target_version(info)
        if sdk != "":
            apk["sdk"]["target"] = sdk

        sdk = cls._extract_sdk_max_version(info)
        if sdk != "":
            apk["sdk"]["max"] = sdk

        sdk = Aapt._extract_sdk_min_version(info)
        if sdk != "":
            apk["sdk"]["min"] = sdk

        return apk

    @classmethod
    def get_manifest_info(cls, filepath: str) -> Dict:
        activities = []  # type: List[Dict[str, str]]
        services = []  # type: List[Dict[str, str]]
        receivers = []  # type: List[Dict[str, str]]

        try:
            xmltree = cls._dump_xmltree(filepath)
            xmltree = xmltree[xmltree.index("application"):-1]
            activities = cls._extract_activities(xmltree)
            services = cls._extract_services(xmltree)
            receivers = cls._extract_broadcast_receivers(xmltree)
        except (RuntimeError, ValueError):
            pass

        return {
            "activities": activities,
            "services": services,
            "receivers": receivers,
        }

    @classmethod
    def get_app_permissions(cls, filepath: str) -> List:
        try:
            dump = cls._dump_permissions(filepath).splitlines()
        except RuntimeError:
            return []

        permissions = []
        for line in dump:
            apk_permission_name_pattern = "^" + Aapt.__LABEL_PERMISSION_NAME + "'(.*)'$"
            permission = Aapt._extract_string_pattern(line, apk_permission_name_pattern)
            if permission != "":
                permissions.append(permission)
        permissions.sort()

        return permissions

    @classmethod
    def _dump_badging(cls, filepath: str) -> str:
        """
        Retrieve the aapt dump badging.
        """
        command = Aapt.__AAPT_EXEC_PATH + " dump badging " + filepath
        return Aapt._launch_shell_command_and_get_result(command)

    @classmethod
    def _dump_permissions(cls, filepath: str) -> str:
        """
        Retrieve the aapt dump permissions.
        """
        command = Aapt.__AAPT_EXEC_PATH + " dump permissions " + filepath
        return Aapt._launch_shell_command_and_get_result(command)

    @classmethod
    def _dump_xmltree(cls, filepath: str) -> str:
        """
        Dump the XML tree of the AndroidManifest.xml file of a given APK package.
        """
        command = cls.__AAPT_EXEC_PATH + " dump xmltree " + filepath + " AndroidManifest.xml"
        return cls._launch_shell_command_and_get_result(command)

    @classmethod
    def _launch_shell_command_and_get_result(cls, command: str) -> str:
        process = Popen(command, stdout=PIPE, stderr=None, shell=True)
        return process.communicate()[0].decode("utf-8")

    @classmethod
    def _extract_app_name(cls, info: str) -> str:
        app_name = cls._extract_string_pattern(info, cls.__LABEL_APPLICATION)
        if app_name is None or app_name  == "":
            app_name = cls._extract_string_pattern(info, cls.__LABEL_LAUNCHABLE_ACTIVITY)
        return app_name

    @classmethod
    def _extract_package_name(cls, info: str) -> str:
        apk_package_name_pattern = "^" + cls.__LABEL_PACKAGE_NAME + "'([a-zA-Z0-9\-\.]+)'"  # pylint: disable=anomalous-backslash-in-string
        return cls._extract_string_pattern(info, apk_package_name_pattern)

    @classmethod
    def _extract_version_name(cls, info: str) -> str:
        apk_version_name_pattern = "^" + cls.__LABEL_PACKAGE_VERSION_NAME + "'([a-zA-Z0-9_\-\.]+)'"  # pylint: disable=anomalous-backslash-in-string
        return cls._extract_string_pattern(info, apk_version_name_pattern)

    @classmethod
    def _extract_version_code(cls, info: str) -> Optional[int]:
        try:
            apk_version_code_pattern = "^" + cls.__LABEL_PACKAGE_VERSION_CODE + "'([0-9\.]+)'"  # pylint: disable=anomalous-backslash-in-string
            return int(cls._extract_string_pattern(info, apk_version_code_pattern))
        except ValueError:
            return None

    @classmethod
    def _extract_sdk_target_version(cls, info: str) -> str:
        apk_sdk_target_pattern = "^" + cls.__LABEL_SDK_TARGET_VERSION + "'(.+)'"
        return cls._extract_string_pattern(info, apk_sdk_target_pattern)

    @classmethod
    def _extract_sdk_max_version(cls, info: str) -> str:
        apk_sdk_max_pattern = "^" + cls.__LABEL_SDK_MAX_VERSION + "'(.+)'"
        return cls._extract_string_pattern(info, apk_sdk_max_pattern)

    @classmethod
    def _extract_sdk_min_version(cls, info: str) -> str:
        apk_sdk_min_pattern = "^" + cls.__LABEL_SDK_MIN_VERSION + "'(.+)'"
        return Aapt._extract_string_pattern(info, apk_sdk_min_pattern)

    @classmethod
    def _extract_activities(cls, xmltree: str) -> List:
        activities = []
        for offs in cls._find_all(xmltree, "activity"):
            activity = xmltree[offs:-1]
            idx = cls._find_between(activity, "android:name(", ")=\"")
            activities.append({"name": cls._find_between(activity, "android:name(" + idx + ")=\"", "\"")})
        return activities

    @classmethod
    def _extract_services(cls, xmltree: str) -> List:
        services = []
        for offs in cls._find_all(xmltree, "service"):
            service = xmltree[offs:-1]
            idx = cls._find_between(service, "android:name(", ")=\"")
            services.append({"name": cls._find_between(service, "android:name(" + idx + ")=\"", "\"")})
        return services

    @classmethod
    def _extract_broadcast_receivers(cls, xmltree: str) -> List:
        receivers = []
        for offs in cls._find_all(xmltree, "receiver"):
            receiver = xmltree[offs:-1]
            idx = cls._find_between(receiver, "android:name(", ")=\"")
            receivers.append({"name": cls._find_between(receiver, "android:name(" + idx + ")=\"", "\"")})
        return receivers

    @staticmethod
    def _extract_string_pattern(string: str, pattern: str) -> str:
        match = re.search(pattern, string, re.MULTILINE | re.IGNORECASE)
        if match and match.group(1):
            return match.group(1).strip()
        return ""

    @staticmethod
    def _find_between(string: str, prefix: str, suffix: str) -> str:
        """
        Find a substring in a string, starting after a specified prefix and ended before a specified suffix.
        """
        try:
            start = string.index(prefix) + len(prefix)
            end = string.index(suffix, start)
            return string[start:end]
        except ValueError:
            return ""

    @staticmethod
    def _find_all(haystack: str, needle: str) -> str:
        """
        Find all the substring starting position in a string.
        """
        offs = -1
        while True:
            offs = haystack.find(needle, offs+1)
            if offs == -1:
                break
            yield offs
