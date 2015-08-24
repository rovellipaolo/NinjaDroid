##
# @file Aapt.py
# @brief Parser for the Android Asset Packaging Tool (aapt).
# @version 1.0
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

import subprocess
import re


##
# Aapt class.
#
class Aapt:
    __AAPT_EXEC_PATH = "lib/aapt/aapt"
    __LABEL_APP_NAME = "application-label:"
    __LABEL_PACKAGE_NAME = "package:(?:.*) name="
    __LABEL_PACKAGE_VERSION_CODE = "package:(?:.*) versionCode="
    __LABEL_PACKAGE_VERSION_NAME = "package:(?:.*) versionName="
    __LABEL_SDK_MAX_VERSION = "maxSdkVersion:"
    __LABEL_SDK_MIN_VERSION = "sdkVersion:"
    __LABEL_SDK_TARGET_VERSION = "targetSdkVersion:"
    __LABEL_PERMISSION_NAME = "uses-permission: name="

    ##
    # Class constructor.
    #
    def __init__(self):
        pass

    ##
    # Extract the value of a given pattern from a given string.
    #
    # @param string  The string to be searched.
    # @param pattern  The pattern to extract.
    # @return The extracted pattern if any is found, an empty string otherwise.
    #
    @staticmethod
    def _extract_string_pattern(string, pattern):
        match = re.search(pattern, string, re.MULTILINE | re.IGNORECASE)
        if match and match.group(1):
            return match.group(1).strip()
        else:
            return ""

    ##
    # Find a substring in a string, starting after a specified prefix and ended before a specified suffix.
    #
    # @param s  the string.
    # @param prefix  the prefix of the file name to be deleted.
    # @param suffix  the suffix of the file name to be deleted.
    # @return the substring starting after prefix and ended before suffix.
    #
    @staticmethod
    def _find_between(s, prefix, suffix):
        try:
            start = s.index(prefix) + len(prefix)
            end = s.index(suffix, start)
            return s[start:end]
        except ValueError:
            return ""

    ##
    # Find all the substring starting position in a string.
    #
    # @param haystack  The string.
    # @param needle  The substring to be found.
    # @return The substring starting after prefix and ended before suffix.
    #
    @staticmethod
    def _find_all(haystack, needle):
        offs = -1
        while True:
            offs = haystack.find(needle, offs+1)
            if offs == -1:
                break
            else:
                yield offs

    ##
    # Retrieve the aapt dump badging.
    #
    # @param filepath  The APK package file path.
    # @return The APK dump badging.
    #
    @classmethod
    def _dump_badging(cls, filepath):
        ##
        # $ aapt dump badging test/data/Example.apk
        # package: name='com.example.app' versionCode='1' versionName='1.0' platformBuildVersionName='4.2.2-576024'
        # sdkVersion:'10'
        # maxSdkVersion:'20'
        # targetSdkVersion:'20'
        # uses-permission: name='android.permission.INTERNET'
        # uses-permission: name='android.permission.READ_EXTERNAL_STORAGE'
        # uses-permission: name='android.permission.RECEIVE_BOOT_COMPLETED'
        # uses-permission: name='android.permission.WRITE_EXTERNAL_STORAGE'
        # application-label:'Example'
        # application-icon-120:'res/drawable-ldpi-v4/ic_launcher.png'
        # application-icon-160:'res/drawable-mdpi-v4/ic_launcher.png'
        # application-icon-240:'res/drawable-hdpi-v4/ic_launcher.png'
        # application-icon-320:'res/drawable-xhdpi-v4/ic_launcher.png'
        # application: label='Example' icon='res/drawable-mdpi-v4/ic_launcher.png'
        # launchable-activity: name='com.example.app.HomeActivity'  label='Example' icon=''
        # feature-group: label=''
        #   uses-feature: name='android.hardware.touchscreen'
        #   uses-implied-feature: name='android.hardware.touchscreen' reason='default feature for all apps'
        # main
        # other-activities
        # other-receivers
        # other-services
        # supports-screens: 'small' 'normal' 'large' 'xlarge'
        # supports-any-density: 'true'
        # locales: '--_--'
        # densities: '120' '160' '240' '320'
        #
        process = subprocess.Popen(Aapt.__AAPT_EXEC_PATH + " dump badging " + filepath, stdout=subprocess.PIPE, stderr=None, shell=True)
        return process.communicate()[0].decode("utf-8")


    ##
    # Retrieve the aapt dump permissions.
    #
    # @param filepath  The APK package file path.
    # @return The APK dump badging.
    #
    @classmethod
    def _dump_permissions(cls, filepath):
        ##
        # $ aapt dump permissions test/data/Example.apk
        # package: com.example.app
        # uses-permission: name='android.permission.INTERNET'
        # uses-permission: name='android.permission.READ_EXTERNAL_STORAGE'
        # uses-permission: name='android.permission.RECEIVE_BOOT_COMPLETED'
        # uses-permission: name='android.permission.WRITE_EXTERNAL_STORAGE'
        #
        process = subprocess.Popen(Aapt.__AAPT_EXEC_PATH + " dump permissions " + filepath, stdout=subprocess.PIPE, stderr=None, shell=True)
        return process.communicate()[0].decode("utf-8")

    ##
    # Dump the XML tree of the AndroidManifest.xml file of a given APK package.
    #
    # @param filepath  The APK package file path.
    # @return The XML tree.
    #
    @classmethod
    def _dump_manifest_xmltree(cls, filepath):
        ##
        # $ aapt dump xmltree test/data/Example.apk AndroidManifest.xml
        # N: android=http://schemas.android.com/apk/res/android
        #   E: manifest (line=2)
        #     A: android:versionCode(0x0101021b)=(type 0x10)0x1
        #     A: android:versionName(0x0101021c)="1.0" (Raw: "1.0")
        #     A: package="com.example.app" (Raw: "com.example.app")
        #     A: platformBuildVersionCode=(type 0x10)0x11 (Raw: "17")
        #     A: platformBuildVersionName="4.2.2-576024" (Raw: "4.2.2-576024")
        #     E: uses-sdk (line=3)
        #       A: android:minSdkVersion(0x0101020c)=(type 0x10)0xa
        #       A: android:targetSdkVersion(0x01010270)=(type 0x10)0x14
        #       A: android:maxSdkVersion(0x01010271)=(type 0x10)0x14
        #     E: uses-permission (line=4)
        #       A: android:name(0x01010003)="android.permission.INTERNET" (Raw: "android.permission.INTERNET")
        #     E: uses-permission (line=5)
        #       A: android:name(0x01010003)="android.permission.READ_EXTERNAL_STORAGE" (Raw: "android.permission.READ_EXTERNAL_STORAGE")
        #     E: uses-permission (line=6)
        #       A: android:name(0x01010003)="android.permission.RECEIVE_BOOT_COMPLETED" (Raw: "android.permission.RECEIVE_BOOT_COMPLETED")
        #     E: uses-permission (line=7)
        #       A: android:name(0x01010003)="android.permission.WRITE_EXTERNAL_STORAGE" (Raw: "android.permission.WRITE_EXTERNAL_STORAGE")
        #     E: application (line=8)
        #       A: android:label(0x01010001)=@0x7f040000
        #       A: android:icon(0x01010002)=@0x7f020000
        #       A: android:logo(0x010102be)=@0x7f020001
        #       A: android:largeHeap(0x0101035a)=(type 0x12)0xffffffff
        #       E: activity (line=9)
        #         A: android:label(0x01010001)=@0x7f040000
        #         A: android:name(0x01010003)="com.example.app.HomeActivity" (Raw: "com.example.app.HomeActivity")
        #         A: android:launchMode(0x0101001d)=(type 0x10)0x1
        #         A: android:configChanges(0x0101001f)=(type 0x11)0x480
        #         E: intent-filter (line=10)
        #           E: action (line=11)
        #             A: android:name(0x01010003)="android.intent.action.MAIN" (Raw: "android.intent.action.MAIN")
        #           E: category (line=12)
        #             A: android:name(0x01010003)="android.intent.category.LAUNCHER" (Raw: "android.intent.category.LAUNCHER")
        #       E: activity (line=15)
        #         A: android:label(0x01010001)=@0x7f040001
        #         A: android:name(0x01010003)="com.example.app.OtherActivity" (Raw: "com.example.app.OtherActivity")
        #         A: android:launchMode(0x0101001d)=(type 0x10)0x1
        #         A: android:noHistory(0x0101022d)=(type 0x12)0xffffffff
        #         A: android:parentActivityName(0x010103a7)="com.example.app.HomeActivity" (Raw: "com.example.app.HomeActivity")
        #         E: meta-data (line=16)
        #           A: android:name(0x01010003)="android.support.PARENT_ACTIVITY" (Raw: "android.support.PARENT_ACTIVITY")
        #           A: android:value(0x01010024)="com.example.app.HomeActivity" (Raw: "com.example.app.HomeActivity")
        #         E: intent-filter (line=17)
        #           E: action (line=18)
        #             A: android:name(0x01010003)="android.intent.action.VIEW" (Raw: "android.intent.action.VIEW")
        #           E: category (line=19)
        #             A: android:name(0x01010003)="android.intent.category.DEFAULT" (Raw: "android.intent.category.DEFAULT")
        #           E: data (line=20)
        #             A: android:scheme(0x01010027)="content" (Raw: "content")
        #           E: data (line=21)
        #             A: android:scheme(0x01010027)="file" (Raw: "file")
        #           E: data (line=22)
        #             A: android:mimeType(0x01010026)="application/vnd.android.package-archive" (Raw: "application/vnd.android.package-archive")
        #       E: service (line=25)
        #         A: android:name(0x01010003)="com.example.app.ExampleService" (Raw: "com.example.app.ExampleService")
        #       E: service (line=26)
        #         A: android:name(0x01010003)="com.example.app.ExampleService2" (Raw: "com.example.app.ExampleService2")
        #         A: android:enabled(0x0101000e)=(type 0x12)0x0
        #         A: android:exported(0x01010010)=(type 0x12)0xffffffff
        #         A: android:isolatedProcess(0x010103a9)=(type 0x12)0xffffffff
        #       E: service (line=27)
        #         A: android:name(0x01010003)="com.example.app.ExampleService3" (Raw: "com.example.app.ExampleService3")
        #         A: android:enabled(0x0101000e)=(type 0x12)0xffffffff
        #         A: android:exported(0x01010010)=(type 0x12)0x0
        #         A: android:isolatedProcess(0x010103a9)=(type 0x12)0x0
        #       E: receiver (line=28)
        #         A: android:name(0x01010003)="com.example.app.ExampleBrodcastReceiver" (Raw: "com.example.app.ExampleBrodcastReceiver")
        #       E: receiver (line=29)
        #         A: android:name(0x01010003)="com.example.app.ExampleBrodcastReceiver2" (Raw: "com.example.app.ExampleBrodcastReceiver2")
        #         A: android:exported(0x01010010)=(type 0x12)0x0
        #         E: intent-filter (line=30)
        #           A: android:priority(0x0101001c)=(type 0x10)0x3e8
        #           E: action (line=31)
        #             A: android:name(0x01010003)="android.intent.action.BOOT_COMPLETED" (Raw: "android.intent.action.BOOT_COMPLETED")
        #           E: action (line=32)
        #             A: android:name(0x01010003)="android.intent.action.MY_PACKAGE_REPLACED" (Raw: "android.intent.action.MY_PACKAGE_REPLACED")
        #       E: receiver (line=35)
        #         A: android:name(0x01010003)="com.example.app.ExampleBrodcastReceiver3" (Raw: "com.example.app.ExampleBrodcastReceiver3")
        #         A: android:enabled(0x0101000e)=(type 0x12)0xffffffff
        #         A: android:exported(0x01010010)=(type 0x12)0x0
        #         E: intent-filter (line=36)
        #           A: android:priority(0x0101001c)=(type 0x10)0x320
        #           E: action (line=37)
        #             A: android:name(0x01010003)="android.intent.action.PACKAGE_ADDED" (Raw: "android.intent.action.PACKAGE_ADDED")
        #           E: action (line=38)
        #             A: android:name(0x01010003)="android.intent.action.PACKAGE_REPLACED" (Raw: "android.intent.action.PACKAGE_REPLACED")
        #           E: action (line=39)
        #             A: android:name(0x01010003)="android.intent.action.BROADCAST_PACKAGE_REMOVED" (Raw: "android.intent.action.BROADCAST_PACKAGE_REMOVED")
        #           E: data (line=40)
        #             A: android:scheme(0x01010027)="package" (Raw: "package")
        #       E: receiver (line=43)
        #         A: android:name(0x01010003)="com.example.app.ExampleBrodcastReceiver4" (Raw: "com.example.app.ExampleBrodcastReceiver4")
        #         A: android:enabled(0x0101000e)=(type 0x12)0x0
        #         A: android:exported(0x01010010)=(type 0x12)0xffffffff
        #
        process = subprocess.Popen(Aapt.__AAPT_EXEC_PATH + " dump xmltree " + filepath + " AndroidManifest.xml", stdout=subprocess.PIPE, stderr=None, shell=True)
        return process.communicate()[0].decode("utf-8")

    ##
    # Retrieve the app name of an APK package.
    #
    # @param filepath  The APK package file path.
    # @return The app name.
    #
    @classmethod
    def get_app_name(cls, filepath):
        return Aapt._extract_string_pattern(cls._dump_badging(filepath), "^" + Aapt.__LABEL_APP_NAME + "'(.+)'$")

    ##
    # Retrieve the APK info.
    #
    # @param filepath  The APK package file path.
    # @return The APK info as a dictionary (i.e. {"package_name":"...", "version":{"code":1, "name":"1.0"}m "sdk":{"target": "...", max: "...", min: "..."}}).
    #
    @classmethod
    def get_apk_info(cls, filepath):
        info = cls._dump_badging(filepath)
        apk = {
            "package_name": cls._extract_string_pattern(info, "^" + cls.__LABEL_PACKAGE_NAME + "'([a-zA-Z0-9\-\.]+)'"),
            "version": {
                "code": "",
                "name": cls._extract_string_pattern(info, "^" + cls.__LABEL_PACKAGE_VERSION_NAME + "'([a-zA-Z0-9_\-\.]+)'"),
            },
            "sdk": {},
        }

        try:
            apk["version"]["code"] = int(cls._extract_string_pattern(info, "^" + cls.__LABEL_PACKAGE_VERSION_CODE + "'([0-9\.]+)'"))
        except ValueError:
            pass

        sdk = cls._extract_string_pattern(info, "^" + cls.__LABEL_SDK_TARGET_VERSION + "'(.+)'")
        if sdk != "":
            apk["sdk"]["target"] = sdk
        sdk = cls._extract_string_pattern(info, "^" + cls.__LABEL_SDK_MAX_VERSION + "'(.+)'")
        if sdk != "":
            apk["sdk"]["max"] = sdk
        sdk = Aapt._extract_string_pattern(info, "^" + cls.__LABEL_SDK_MIN_VERSION + "'(.+)'")
        if sdk != "":
            apk["sdk"]["min"] = sdk

        return apk

    ##
    # Retrieve the AndroidManifest.xml info.
    #
    # @param filepath  The APK package file path.
    # @return The list of Activities, Services and BroadcastReceivers as a dictionary.
    #
    @classmethod
    def get_manifest_info(cls, filepath):
        xmltree = cls._dump_manifest_xmltree(filepath)
        # @TODO: Refactor this code...
        try:
            # Extract only from the <application> tag:
            xmltree = xmltree[xmltree.index("application"):-1]

            activities = []
            services = []
            receivers = []

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
        except ValueError:  # the <application> TAG has not been found...
            pass
        
        return {
            "activities": activities,
            "services": services,
            "receivers": receivers,
        }

    ##
    # Retrieve the permissions from the AndroidManifest.xml file of a given APK package.
    #
    # @param filepath  The APK package file path.
    # @return The list of required permissions.
    #
    @classmethod
    def get_app_permissions(cls, filepath):
        dump = cls._dump_permissions(filepath).splitlines()

        permissions = []
        for line in dump:
            perm = Aapt._extract_string_pattern(line, "^" + Aapt.__LABEL_PERMISSION_NAME + "'(.*)'$")
            if perm != "":
                permissions.append(perm)
        permissions.sort()

        return permissions
