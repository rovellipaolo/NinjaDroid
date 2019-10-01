import logging
import os.path
import subprocess
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class Aapt:
    """
    Parser for the Android Asset Packaging Tool (aapt).
    """

    __AAPT_EXEC_PATH = os.path.join(os.path.dirname(__file__), "aapt")
    __LABEL_APP_NAME = "^application: .*label='([^']*)' .*"
    __LABEL_LAUNCHABLE_ACTIVITY = "^launchable-activity: .*label='([^']*)'.*"
    __LABEL_PACKAGE_NAME = "package:(?:.*) name="
    __LABEL_PACKAGE_VERSION_CODE = "package:(?:.*) versionCode="
    __LABEL_PACKAGE_VERSION_NAME = "package:(?:.*) versionName="
    __LABEL_SDK_MAX_VERSION = "maxSdkVersion:"
    __LABEL_SDK_MIN_VERSION = "sdkVersion:"
    __LABEL_SDK_TARGET_VERSION = "targetSdkVersion:"
    __LABEL_PERMISSION_NAME = "uses-permission: name="

    def __init__(self, logger=logger):
        self.logger = logger
        self.logger.debug("aapt exec path: %s", self.__AAPT_EXEC_PATH)
        pass

    @staticmethod
    def _extract_string_pattern(string: str, pattern: str) -> str:
        match = re.search(pattern, string, re.MULTILINE | re.IGNORECASE)
        if match and match.group(1):
            return match.group(1).strip()
        else:
            return ""

    @staticmethod
    def _find_between(s: str, prefix: str, suffix: str) -> str:
        """
        Find a substring in a string, starting after a specified prefix and ended before a specified suffix.
        """
        try:
            start = s.index(prefix) + len(prefix)
            end = s.index(suffix, start)
            return s[start:end]
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
            else:
                yield offs

    @classmethod
    def _dump_badging(cls, filepath: str) -> str:
        """
        Retrieve the aapt dump badging.

        Example:
            $ aapt dump badging tests/data/Example.apk
            package: name='com.example.app' versionCode='1' versionName='1.0' platformBuildVersionName='4.2.2-576024'
            sdkVersion:'10'
            maxSdkVersion:'20'
            targetSdkVersion:'20'
            uses-permission: name='android.permission.INTERNET'
            uses-permission: name='android.permission.READ_EXTERNAL_STORAGE'
            uses-permission: name='android.permission.RECEIVE_BOOT_COMPLETED'
            uses-permission: name='android.permission.WRITE_EXTERNAL_STORAGE'
            application-label:'Example'
            application-icon-120:'res/drawable-ldpi-v4/ic_launcher.png'
            application-icon-160:'res/drawable-mdpi-v4/ic_launcher.png'
            application-icon-240:'res/drawable-hdpi-v4/ic_launcher.png'
            application-icon-320:'res/drawable-xhdpi-v4/ic_launcher.png'
            application: label='Example' icon='res/drawable-mdpi-v4/ic_launcher.png'
            launchable-activity: name='com.example.app.HomeActivity'  label='Example' icon=''
            feature-group: label=''
              uses-feature: name='android.hardware.touchscreen'
              uses-implied-feature: name='android.hardware.touchscreen' reason='default feature for all apps'
            main
            other-activities
            other-receivers
            other-services
            supports-screens: 'small' 'normal' 'large' 'xlarge'
            supports-any-density: 'true'
            locales: '--_--'
            densities: '120' '160' '240' '320'
        """
        command = Aapt.__AAPT_EXEC_PATH + " dump badging " + filepath
        return Aapt._launch_shell_command_and_get_result(command)

    @classmethod
    def _dump_permissions(cls, filepath: str) -> str:
        """
        Retrieve the aapt dump permissions.

        Example:
            $ aapt dump permissions tests/data/Example.apk
            package: com.example.app
            uses-permission: name='android.permission.INTERNET'
            uses-permission: name='android.permission.READ_EXTERNAL_STORAGE'
            uses-permission: name='android.permission.RECEIVE_BOOT_COMPLETED'
            uses-permission: name='android.permission.WRITE_EXTERNAL_STORAGE'
        """
        command = Aapt.__AAPT_EXEC_PATH + " dump permissions " + filepath
        return Aapt._launch_shell_command_and_get_result(command)

    @classmethod
    def _dump_manifest_xmltree(cls, filepath: str) -> str:
        """
        Dump the XML tree of the AndroidManifest.xml file of a given APK package.

        Example:
            $ aapt dump xmltree tests/data/Example.apk AndroidManifest.xml
            N: android=http://schemas.android.com/apk/res/android
              E: manifest (line=2)
                A: android:versionCode(0x0101021b)=(type 0x10)0x1
                A: android:versionName(0x0101021c)="1.0" (Raw: "1.0")
                A: package="com.example.app" (Raw: "com.example.app")
                A: platformBuildVersionCode=(type 0x10)0x11 (Raw: "17")
                A: platformBuildVersionName="4.2.2-576024" (Raw: "4.2.2-576024")
                E: uses-sdk (line=3)
                  A: android:minSdkVersion(0x0101020c)=(type 0x10)0xa
                  A: android:targetSdkVersion(0x01010270)=(type 0x10)0x14
                  A: android:maxSdkVersion(0x01010271)=(type 0x10)0x14
                E: uses-permission (line=4)
                  A: android:name(0x01010003)="android.permission.INTERNET" (Raw: "...")
                E: uses-permission (line=5)
                  A: android:name(0x01010003)="android.permission.READ_EXTERNAL_STORAGE" (Raw: "...")
                E: uses-permission (line=6)
                  A: android:name(0x01010003)="android.permission.RECEIVE_BOOT_COMPLETED" (Raw: "...")
                E: uses-permission (line=7)
                  A: android:name(0x01010003)="android.permission.WRITE_EXTERNAL_STORAGE" (Raw: "...")
                E: application (line=8)
                  A: android:label(0x01010001)=@0x7f040000
                  A: android:icon(0x01010002)=@0x7f020000
                  A: android:logo(0x010102be)=@0x7f020001
                  A: android:largeHeap(0x0101035a)=(type 0x12)0xffffffff
                  E: activity (line=9)
                    A: android:label(0x01010001)=@0x7f040000
                    A: android:name(0x01010003)="com.example.app.HomeActivity" (Raw: "...")
                    A: android:launchMode(0x0101001d)=(type 0x10)0x1
                    A: android:configChanges(0x0101001f)=(type 0x11)0x480
                    E: intent-filter (line=10)
                      E: action (line=11)
                        A: android:name(0x01010003)="android.intent.action.MAIN" (Raw: "...")
                      E: category (line=12)
                        A: android:name(0x01010003)="android.intent.category.LAUNCHER" (Raw: "...")
                  E: activity (line=15)
                    A: android:label(0x01010001)=@0x7f040001
                    A: android:name(0x01010003)="com.example.app.OtherActivity" (Raw: "...")
                    A: android:launchMode(0x0101001d)=(type 0x10)0x1
                    A: android:noHistory(0x0101022d)=(type 0x12)0xffffffff
                    A: android:parentActivityName(0x010103a7)="com.example.app.HomeActivity" (Raw: "...")
                    E: meta-data (line=16)
                      A: android:name(0x01010003)="android.support.PARENT_ACTIVITY" (Raw: "...")
                      A: android:value(0x01010024)="com.example.app.HomeActivity" (Raw: "...")
                    E: intent-filter (line=17)
                      E: action (line=18)
                        A: android:name(0x01010003)="android.intent.action.VIEW" (Raw: "...")
                      E: category (line=19)
                        A: android:name(0x01010003)="android.intent.category.DEFAULT" (Raw: "...")
                      E: data (line=20)
                        A: android:scheme(0x01010027)="content" (Raw: "content")
                      E: data (line=21)
                        A: android:scheme(0x01010027)="file" (Raw: "file")
                      E: data (line=22)
                        A: android:mimeType(0x01010026)="application/vnd.android.package-archive" (Raw: "...")
                  E: service (line=25)
                    A: android:name(0x01010003)="com.example.app.ExampleService" (Raw: "...")
                  ...
                  E: receiver (line=28)
                    A: android:name(0x01010003)="com.example.app.ExampleBrodcastReceiver" (Raw: "...")
                  ...
        """
        command = Aapt.__AAPT_EXEC_PATH + " dump xmltree " + filepath + " AndroidManifest.xml"
        return Aapt._launch_shell_command_and_get_result(command)

    @classmethod
    def _launch_shell_command_and_get_result(cls, command: str) -> str:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        return process.communicate()[0].decode("utf-8")

    @classmethod
    def get_app_name(cls, filepath: str) -> str:
        badging = cls._dump_badging(filepath)
        return (
            Aapt._extract_string_pattern(badging, Aapt.__LABEL_APP_NAME)
            or Aapt._extract_string_pattern(badging, Aapt.__LABEL_LAUNCHABLE_ACTIVITY)
        )

    @classmethod
    def get_apk_info(cls, filepath: str) -> Dict:
        info = cls._dump_badging(filepath)

        apk_package_name_pattern = "^" + cls.__LABEL_PACKAGE_NAME + "'([a-zA-Z0-9\-\.]+)'"
        apk_version_name_pattern = "^" + cls.__LABEL_PACKAGE_VERSION_NAME + "'([a-zA-Z0-9_\-\.]+)'"

        apk = {
            "package_name": cls._extract_string_pattern(info, apk_package_name_pattern),
            "version": {
                "code": "",
                "name": cls._extract_string_pattern(info, apk_version_name_pattern),
            },
            "sdk": {},
        }

        try:
            apk_version_code_pattern = "^" + cls.__LABEL_PACKAGE_VERSION_CODE + "'([0-9\.]+)'"
            apk["version"]["code"] = int(cls._extract_string_pattern(info, apk_version_code_pattern))
        except ValueError:
            pass

        apk_sdk_target_pattern = "^" + cls.__LABEL_SDK_TARGET_VERSION + "'(.+)'"
        sdk = cls._extract_string_pattern(info, apk_sdk_target_pattern)
        if sdk != "":
            apk["sdk"]["target"] = sdk

        apk_sdk_max_pattern = "^" + cls.__LABEL_SDK_MAX_VERSION + "'(.+)'"
        sdk = cls._extract_string_pattern(info, apk_sdk_max_pattern)
        if sdk != "":
            apk["sdk"]["max"] = sdk

        apk_sdk_min_pattern = "^" + cls.__LABEL_SDK_MIN_VERSION + "'(.+)'"
        sdk = Aapt._extract_string_pattern(info, apk_sdk_min_pattern)
        if sdk != "":
            apk["sdk"]["min"] = sdk

        return apk

    @classmethod
    def get_manifest_info(cls, filepath: str) -> Dict:
        activities = []  # type: List[Dict[str, str]]
        services = []  # type: List[Dict[str, str]]
        receivers = []  # type: List[Dict[str, str]]

        xmltree = cls._dump_manifest_xmltree(filepath)
        # @TODO: Refactor this code...
        try:
            # Extract only from the <application> tag:
            xmltree = xmltree[xmltree.index("application"):-1]

            for offs in cls._find_all(xmltree, "activity"):
                activity = xmltree[offs:-1]
                idx = cls._find_between(activity, "android:name(", ")=\"")
                activities.append({"name": cls._find_between(activity, "android:name(" + idx + ")=\"", "\"")})

            for offs in cls._find_all(xmltree, "service"):
                service = xmltree[offs:-1]
                idx = cls._find_between(service, "android:name(", ")=\"")
                services.append({"name": cls._find_between(service, "android:name(" + idx + ")=\"", "\"")})

            for offs in cls._find_all(xmltree, "receiver"):
                receiver = xmltree[offs:-1]
                idx = cls._find_between(receiver, "android:name(", ")=\"")
                receivers.append({"name": cls._find_between(receiver, "android:name(" + idx + ")=\"", "\"")})
        except ValueError:
            # The <application> TAG has not been found...
            pass

        return {
            "activities": activities,
            "services": services,
            "receivers": receivers,
        }

    @classmethod
    def get_app_permissions(cls, filepath: str) -> List:
        dump = cls._dump_permissions(filepath).splitlines()

        permissions = []
        for line in dump:
            apk_permission_name_pattern = "^" + Aapt.__LABEL_PERMISSION_NAME + "'(.*)'$"
            perm = Aapt._extract_string_pattern(line, apk_permission_name_pattern)
            if perm != "":
                permissions.append(perm)
        permissions.sort()

        return permissions
