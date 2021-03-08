from logging import getLogger, Logger
from xml.dom import minidom
from xml.dom.minidom import Element
from xml.parsers.expat import ExpatError
from typing import Any, Dict, List, Optional
from pyaxmlparser.axmlprinter import AXMLPrinter

from ninjadroid.aapt.aapt import Aapt
from ninjadroid.parsers.file import File, FileParser, FileParsingError


default_logger = getLogger(__name__)


class AppVersion:
    """
    AndroidManifest version information.
    """

    def __init__(self, code: Optional[int], name: str):
        self.__code= code
        self.__name = name

    def __eq__(self, other: Any):
        return isinstance(other, AppVersion) and \
               self.__code == other.get_code() and \
               self.__name == other.get_name()

    def get_code(self) -> Optional[int]:
        return self.__code

    def get_name(self) -> str:
        return self.__name

    def as_dict(self) -> Dict:
        return {
            "code": self.__code if self.__code is not None else "",
            "name": self.__name
        }


class AppSdk:
    """
    AndroidManifest SDK information.
    """

    def __init__(self, min_version: str, target_version: str, max_version: Optional[str]):
        self.__min = min_version
        self.__target = target_version
        self.__max = max_version

    def __eq__(self, other: Any):
        return isinstance(other, AppSdk) and \
               self.__min == other.get_min_version() and \
               self.__target == other.get_target_version() and \
               self.__max == other.get_max_version()

    def get_min_version(self) -> str:
        return self.__min

    def get_target_version(self) -> str:
        return self.__target

    def get_max_version(self) -> Optional[str]:
        return self.__max

    def as_dict(self) -> Dict:
        return {
            "min": self.__min,
            "target": self.__target,
            "max": self.__max if self.__max is not None else ""
        }


class AndroidManifest(File):
    """
    AndroidManifest.xml file information.
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            filename: str,
            size: str,
            md5hash: str,
            sha1hash: str,
            sha256hash: str,
            sha512hash: str,
            package_name: str,
            version: AppVersion,
            sdk: AppSdk,
            permissions: List[str],
            activities: List[Dict],
            services: List[Dict],
            receivers: List[Dict],
    ):
        super().__init__(filename, size, md5hash, sha1hash, sha256hash, sha512hash)
        self.__package_name = package_name
        self.__version = version
        self.__sdk = sdk
        self.__permissions = permissions
        self.__activities = activities
        self.__services = services
        self.__receivers = receivers

    def get_package_name(self) -> str:
        return self.__package_name

    def get_version(self) -> AppVersion:
        return self.__version

    def get_sdk(self) -> AppSdk:
        return self.__sdk

    def get_permissions(self) -> List[str]:
        return self.__permissions

    def get_activities(self) -> List[Dict]:
        return self.__activities

    def get_services(self) -> List[Dict]:
        return self.__services

    def get_broadcast_receivers(self) -> List[Dict]:
        return self.__receivers

    def as_dict(self) -> Dict:
        dump = super().as_dict()
        dump["package"] = self.__package_name
        dump["version"] = self.__version.as_dict()
        dump["sdk"] = self.__sdk.as_dict()
        dump["permissions"] = self.__permissions
        if self.__activities:
            dump["activities"] = self.__activities
        if self.__services:
            dump["services"] = self.__services
        if self.__receivers:
            dump["receivers"] = self.__receivers
        return dump


class AndroidManifestParsingError(FileParsingError):
    """
    AndroidManifest.xml file parsing error.
    """

    def __init__(self):
        FileParsingError.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an AndroidManifest.xml!"


class AndroidManifestParser:
    """
    Parser implementation for AndroidManifest.xml files.
    """

    def __init__(self, logger: Logger = default_logger):
        self.logger = logger

    def parse(
            self,
            filepath: str,
            binary: bool = False,
            apk_path: Optional[str] = None,
            extended_processing: bool = True
    ):
        """
        :param filepath: path of the AndroidManifest.xml file
        :param binary: (optional) whether the AndroidManifest.xml file is in binary format or not. False by default.
        :param apk_path: (optional) path of the APK package containing this AndroidManifest.xml file. None by default.
        :param extended_processing: (optional) whether should parse all information or only a summary. True by default.
        :return: the parsed AndroidManifest.xml file
        :raise: FileParsingError if cannot parse the file
        :raise: AndroidManifestParsingError if cannot parse the file as an AndroidManifest.xml
        """
        self.logger.debug("Parsing AndroidManifest.xml file: filepath=\"%s\"", filepath)
        file = FileParser(self.logger).parse(filepath, "AndroidManifest.xml")
        try:
            self.logger.debug("Parsing AndroidManifest.xml from DOM...")
            dom = self.parse_manifest_dom(filepath, binary)
        except AndroidManifestParsingError as error:
            self.logger.debug("Cannot parse AndroidManifest.xml from DOM!")
            if apk_path is None or apk_path == "":
                self.logger.debug("Cannot parse AndroidManifest.xml from APK!")
                raise error
            self.logger.debug("Parsing AndroidManifest.xml from APK: apk_path=%s", apk_path)
            return self.build_manifest_from_apk(file, extended_processing, apk_path)
        return self.build_manifest_from_dom(file, extended_processing, dom)

    @staticmethod
    def parse_manifest_dom(filepath: str, binary: bool) -> Element:
        dom = None
        with open(filepath, 'rb') as manifest:
            try:
                if binary:
                    raw = AXMLPrinter(manifest.read()).get_buff()
                    dom = minidom.parseString(raw)
                else:
                    dom = minidom.parse(filepath)
            except (ExpatError, IOError) as error:
                raise AndroidManifestParsingError from error
        if dom is None:
            raise AndroidManifestParsingError
        return dom.documentElement

    @staticmethod
    def build_manifest_from_dom(file: File, extended_processing: bool, dom: Element) -> AndroidManifest:
        if extended_processing:
            application = dom.getElementsByTagName("application")[0]
            activities = AndroidManifestParser.parse_activities_from_dom(application)
            services = AndroidManifestParser.parse_services_from_dom(application)
            receivers = AndroidManifestParser.parse_broadcast_receivers_from_dom(application)
        else:
            activities = []
            services = []
            receivers = []
        return AndroidManifest(
            filename=file.get_file_name(),
            size=file.get_size(),
            md5hash=file.get_md5(),
            sha1hash=file.get_sha1(),
            sha256hash=file.get_sha256(),
            sha512hash=file.get_sha512(),
            package_name=dom.getAttribute("package"),
            version=AndroidManifestParser.parse_version_from_dom(dom),
            sdk=AndroidManifestParser.parse_sdk_from_dom(dom),
            permissions=AndroidManifestParser.__parse_list_from_dom(
                dom,
                tag="uses-permission",
                attribute="android:name"
            ),
            activities=activities,
            services=services,
            receivers=receivers
        )

    @staticmethod
    def build_manifest_from_apk(file: File, extended_processing: bool, apk_path: str) -> AndroidManifest:
        apk = Aapt.get_apk_info(apk_path)
        if extended_processing:
            manifest = Aapt.get_manifest_info(apk_path)
            activities = manifest["activities"]
            services = manifest["services"]
            receivers = manifest["receivers"]
        else:
            activities = []
            services = []
            receivers = []
        return AndroidManifest(
            filename=file.get_file_name(),
            size=file.get_size(),
            md5hash=file.get_md5(),
            sha1hash=file.get_sha1(),
            sha256hash=file.get_sha256(),
            sha512hash=file.get_sha512(),
            package_name=apk["package_name"],
            version=AppVersion(code=apk["version"]["code"], name=apk["version"]["name"]),
            sdk=AppSdk(
                target_version=apk["sdk"]["target"],
                min_version=apk["sdk"]["min"],
                max_version=apk["sdk"]["max"]
            ),
            permissions=Aapt.get_app_permissions(apk_path),
            activities=activities,
            services=services,
            receivers=receivers
        )

    @staticmethod
    def parse_version_from_dom(dom: Element) -> AppVersion:
        try:
            version_code = int(dom.getAttribute("android:versionCode"))
        except ValueError:
            version_code = None
        return AppVersion(
            code=version_code,
            name=dom.getAttribute("android:versionName")
        )

    @staticmethod
    def parse_sdk_from_dom(dom: Element) -> Optional[AppVersion]:
        min_version =  "1"
        target_version =  None
        max_version =  None
        for element in dom.getElementsByTagName("uses-sdk"):
            if element.hasAttribute("android:minSdkVersion"):
                min_version = element.getAttribute("android:minSdkVersion")
            if element.hasAttribute("android:targetSdkVersion"):
                target_version = element.getAttribute("android:targetSdkVersion")
            if element.hasAttribute("android:maxSdkVersion"):
                max_version = element.getAttribute("android:maxSdkVersion")
            break
        return AppSdk(
            min_version=min_version,
            target_version=target_version if target_version is not None else min_version,
            max_version=max_version
        )

    @staticmethod
    def parse_activities_from_dom(dom: Element) -> List[Dict]:
        return AndroidManifestParser.__parse_list_of_dict_from_dom(
            dom,
            tag="activity",
            attributes={
                "name": "android:name",
                "launchMode": "android:launchMode",
                "multiprocess":"android:multiprocess",
                "noHistory":"android:noHistory",
                "parentActivityName":"android:parentActivityName",
                "meta-data": {
                    "name": "android:name",
                    "value": "android:value"
                },
                "intent-filter": {
                    "label": "android:label",
                    "priority": "android:priority",
                    "action": [
                        "android:name"
                    ],
                    "category": [
                        "android:name"
                    ],
                    "data": {
                        "scheme": "android:scheme",
                        "mimeType": "android:mimeType"
                    }
                }
            }
        )

    @staticmethod
    def parse_services_from_dom(dom: Element) -> List[Dict]:
        return AndroidManifestParser.__parse_list_of_dict_from_dom(
            dom,
            tag="service",
            attributes = {
                "name": "android:name",
                "enabled":"android:enabled",
                "exported":"android:exported",
                "process":"android:process",
                "isolatedProcess":"android:isolatedProcess",
                "meta-data": {
                    "name": "android:name",
                    "value": "android:value"
                },
                "intent-filter": {
                    "label": "android:label",
                    "priority": "android:priority",
                    "action": [
                        "android:name"
                    ],
                    "category": [
                        "android:name"
                    ],
                    "data": {
                        "scheme": "android:scheme",
                        "mimeType": "android:mimeType"
                    }
                }
            }
        )

    @staticmethod
    def parse_broadcast_receivers_from_dom(dom: Element) -> List[Dict]:
        return AndroidManifestParser.__parse_list_of_dict_from_dom(
            dom,
            tag="receiver",
            attributes = {
                "name": "android:name",
                "enabled":"android:enabled",
                "exported":"android:exported",
                "process":"android:process",
                "meta-data": {
                    "name": "android:name",
                    "value": "android:value"
                },
                "intent-filter": {
                    "label": "android:label",
                    "priority": "android:priority",
                    "action": [
                        "android:name"
                    ],
                    "category": [
                        "android:name"
                    ],
                    "data": {
                        "scheme": "android:scheme",
                        "mimeType": "android:mimeType"
                    }
                }
            }
        )

    @staticmethod
    def __parse_list_from_dom(dom: Element, tag: str, attribute: str) -> List[Any]:
        res = []
        for element in dom.getElementsByTagName(tag):
            res.append(element.getAttribute(attribute))
        return sorted(res)

    @staticmethod
    def __parse_list_of_dict_from_dom(dom: Element, tag: str, attributes: Dict[str, Any]) -> List[Any]:
        res = []
        for element in dom.getElementsByTagName(tag):
            data = {}
            for key, value in attributes.items():
                if isinstance(value, dict):
                    tmp = AndroidManifestParser.__parse_list_of_dict_from_dom(element, key, attributes[key])
                    if len(tmp) > 0:
                        data[key] = tmp
                elif isinstance(value, list):
                    tmp = AndroidManifestParser.__parse_list_from_dom(element, key, value[0])
                    if len(tmp) > 0:
                        data[key] = tmp
                else:  # isinstance(value, str)
                    if element.hasAttribute(attributes[key]):
                        data[key] = element.getAttribute(attributes[key])
            res.append(data)
        return res

    @staticmethod
    def looks_like_a_manifest(filename: str) -> bool:
        return filename == "AndroidManifest.xml"
