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


class AppComponent:
    """
    AndroidManifest generic component (i.e. activity, service or broadcast-receiver) information.
    """

    def __init__(self, name: str, metadata: Optional[List[Dict]] = None, intent_filters: Optional[List[Dict]] = None):
        self.__name = name
        self.__metadata = metadata if metadata is not None else []
        self.__intent_filters = intent_filters if intent_filters is not None else []

    def __eq__(self, other: Any):
        return isinstance(other, AppComponent) and \
               self.__name == other.get_name() and \
               self.__metadata == other.get_metadata() and \
               self.__intent_filters == other.get_intent_filters()

    def get_name(self) -> str:
        return self.__name

    def get_metadata(self) -> Dict:
        return self.__metadata

    def get_intent_filters(self) -> Dict:
        return self.__intent_filters

    def as_dict(self) -> Dict:
        dump = {"name": self.__name}
        if self.__metadata:
            dump["meta-data"] = self.__metadata
        if self.__intent_filters:
            dump["intent-filter"] = self.__intent_filters
        return dump


class AppActivity(AppComponent):
    """
    AndroidManifest activity information.
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            name: str,
            metadata: Optional[List[Dict]] = None,
            intent_filters: Optional[List[Dict]] = None,
            parent_name: Optional[str] = None,
            launch_mode: Optional[str] = None,
            no_history: Optional[bool] = None
    ):
        super().__init__(name, metadata, intent_filters)
        self.__parent_name = parent_name
        self.__launch_mode = launch_mode
        self.__no_history = no_history

    def __eq__(self, other: Any):
        return isinstance(other, AppActivity) and \
               self.get_name() == other.get_name() and \
               self.get_metadata() == other.get_metadata() and \
               self.get_intent_filters() == other.get_intent_filters() and \
               self.__parent_name == other.get_parent_name() and \
               self.__launch_mode == other.get_launch_mode() and \
               self.has_history() == other.has_history()

    def get_parent_name(self) -> str:
        return self.__parent_name

    def get_launch_mode(self) -> Optional[str]:
        return self.__launch_mode

    def has_history(self) -> bool:
        return self.__no_history is not None and not self.__no_history

    def as_dict(self) -> Dict:
        dump = super().as_dict()
        if self.__parent_name is not None:
            dump["parentActivityName"] = self.__parent_name
        if self.__launch_mode is not None:
            dump["launchMode"] = self.__launch_mode
        if self.__no_history is not None:
            dump["noHistory"] = self.__no_history
        return dump


class AppService(AppComponent):
    """
    AndroidManifest service information.
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            name: str,
            metadata: Optional[List[Dict]] = None,
            intent_filters: Optional[List[Dict]] = None,
            enabled: Optional[bool] = None,
            exported: Optional[bool] = None,
            process: Optional[str] = None,
            isolated_process: Optional[bool] = None
    ):
        super().__init__(name, metadata, intent_filters)
        self.__enabled = enabled
        self.__exported = exported
        self.__process = process
        self.__isolated_process = isolated_process

    def __eq__(self, other: Any):
        return isinstance(other, AppService) and \
               self.get_name() == other.get_name() and \
               self.get_metadata() == other.get_metadata() and \
               self.get_intent_filters() == other.get_intent_filters() and \
               self.is_enabled() == other.is_enabled() and \
               self.is_exported() == other.is_exported() and \
               self.__process == other.get_process() and \
               self.is_isolated_process() == other.is_isolated_process()

    def is_enabled(self) -> bool:
        return self.__enabled is not None and self.__enabled

    def is_exported(self) -> bool:
        return self.__exported is not None and self.__exported

    def get_process(self) -> Optional[str]:
        return self.__process

    def is_isolated_process(self) -> bool:
        return self.__isolated_process is not None and self.__isolated_process

    def as_dict(self) -> Dict:
        dump = super().as_dict()
        if self.__enabled is not None:
            dump["enabled"] = self.__enabled
        if self.__exported is not None:
            dump["exported"] = self.__exported
        if self.__process is not None:
            dump["process"] = self.__process
        if self.__isolated_process is not None:
            dump["isolatedProcess"] = self.__isolated_process
        return dump


class AppBroadcastReceiver(AppComponent):
    """
    AndroidManifest broadcast-receiver information.
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            name: str,
            metadata: Optional[List[Dict]] = None,
            intent_filters: Optional[List[Dict]] = None,
            enabled: Optional[bool] = None,
            exported: Optional[bool] = None
    ):
        super().__init__(name, metadata, intent_filters)
        self.__enabled = enabled
        self.__exported = exported

    def __eq__(self, other: Any):
        return isinstance(other, AppBroadcastReceiver) and \
               self.get_name() == other.get_name() and \
               self.get_metadata() == other.get_metadata() and \
               self.get_intent_filters() == other.get_intent_filters() and \
               self.is_enabled() == other.is_enabled() and \
               self.is_exported() == other.is_exported()

    def is_enabled(self) -> bool:
        return self.__enabled is not None and self.__enabled

    def is_exported(self) -> bool:
        return self.__exported is not None and self.__exported

    def as_dict(self) -> Dict:
        dump = super().as_dict()
        if self.__enabled is not None:
            dump["enabled"] = self.__enabled
        if self.__exported is not None:
            dump["exported"] = self.__exported
        return dump


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
            activities: List[AppActivity],
            services: List[AppService],
            receivers: List[AppBroadcastReceiver],
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

    def get_activities(self) -> List[AppActivity]:
        return self.__activities

    def get_services(self) -> List[AppService]:
        return self.__services

    def get_broadcast_receivers(self) -> List[AppBroadcastReceiver]:
        return self.__receivers

    def as_dict(self) -> Dict:
        dump = super().as_dict()
        dump["package"] = self.__package_name
        dump["version"] = self.__version.as_dict()
        dump["sdk"] = self.__sdk.as_dict()
        dump["permissions"] = self.__permissions
        if self.__activities:
            dump["activities"] = [activity.as_dict() for activity in self.__activities]
        if self.__services:
            dump["services"] = [service.as_dict() for service in self.__services]
        if self.__receivers:
            dump["receivers"] = [receiver.as_dict() for receiver in self.__receivers]
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
        activities = []
        services = []
        receivers = []
        if extended_processing:
            manifest = Aapt.get_manifest_info(apk_path)
            activities = [AppActivity(name=activity) for activity in manifest["activities"]]
            services = [AppService(name=service) for service in manifest["services"]]
            receivers = [AppBroadcastReceiver(name=receiver) for receiver in manifest["receivers"]]
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
            target_version = AndroidManifestParser.__parse_str_from_dom(element, "android:targetSdkVersion")
            max_version = AndroidManifestParser.__parse_str_from_dom(element, "android:maxSdkVersion")
            break
        return AppSdk(
            min_version=min_version,
            target_version=target_version if target_version is not None else min_version,
            max_version=max_version
        )

    @staticmethod
    def parse_activities_from_dom(dom: Element) -> List[AppActivity]:
        activities = []
        for element in dom.getElementsByTagName("activity"):
            activity = AppActivity(
                name=element.getAttribute("android:name"),
                metadata=AndroidManifestParser.__parse_metadata_from_dom(element),
                intent_filters=AndroidManifestParser.__parse_intent_filters_from_dom(element),
                parent_name=AndroidManifestParser.__parse_str_from_dom(element, "android:parentActivityName"),
                launch_mode=AndroidManifestParser.__parse_str_from_dom(element, "android:launchMode"),
                no_history=AndroidManifestParser.__parse_str_from_dom(element, "android:noHistory")
            )
            activities.append(activity)
        return activities

    @staticmethod
    def parse_services_from_dom(dom: Element) -> List[Dict]:
        services = []
        for element in dom.getElementsByTagName("service"):
            service = AppService(
                name=element.getAttribute("android:name"),
                metadata=AndroidManifestParser.__parse_metadata_from_dom(element),
                intent_filters=AndroidManifestParser.__parse_intent_filters_from_dom(element),
                enabled=AndroidManifestParser.__parse_bool_from_dom(element, "android:enabled"),
                exported=AndroidManifestParser.__parse_bool_from_dom(element, "android:exported"),
                process=AndroidManifestParser.__parse_str_from_dom(element, "android:process"),
                isolated_process=AndroidManifestParser.__parse_bool_from_dom(element, "android:isolatedProcess")
            )
            services.append(service)
        return services

    @staticmethod
    def parse_broadcast_receivers_from_dom(dom: Element) -> List[Dict]:
        receivers = []
        for element in dom.getElementsByTagName("receiver"):
            receiver = AppBroadcastReceiver(
                name=element.getAttribute("android:name"),
                metadata=AndroidManifestParser.__parse_metadata_from_dom(element),
                intent_filters=AndroidManifestParser.__parse_intent_filters_from_dom(element),
                enabled=AndroidManifestParser.__parse_bool_from_dom(element, "android:enabled"),
                exported=AndroidManifestParser.__parse_bool_from_dom(element, "android:exported")
            )
            receivers.append(receiver)
        return receivers

    @staticmethod
    def __parse_metadata_from_dom(dom: Element) -> List[Dict]:
        metadata = []
        for element in dom.getElementsByTagName("meta-data"):
            data = AndroidManifestParser.__parse_dict_from_dom(
                element,
                attributes={
                    "name": "android:name",
                    "value": "android:value"
                }
            )
            metadata.append(data)
        return metadata

    @staticmethod
    def __parse_intent_filters_from_dom(dom: Element) -> List[Dict]:
        intent_filters = []
        for element in dom.getElementsByTagName("intent-filter"):
            intent_filter = AndroidManifestParser.__parse_dict_from_dom(
                element,
                attributes={
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
            )
            intent_filters.append(intent_filter)
        return intent_filters

    @staticmethod
    def __parse_str_from_dom(dom: Element, attribute: str) -> Optional[str]:
        if dom.hasAttribute(attribute):
            return dom.getAttribute(attribute)
        return None

    @staticmethod
    def __parse_bool_from_dom(dom: Element, attribute: str) -> Optional[str]:
        attribute = AndroidManifestParser.__parse_str_from_dom(dom, attribute)
        return attribute == "true" if attribute is not None else None

    @staticmethod
    def __parse_dict_from_dom(dom: Element, attributes: Dict[str, Any]) -> Dict:
        res = {}
        for key, value in attributes.items():
            if isinstance(value, dict):
                tmp = []
                for element in dom.getElementsByTagName(key):
                    tmp.append(AndroidManifestParser.__parse_dict_from_dom(element, attributes[key]))
                if tmp:
                    res[key] = tmp
            elif isinstance(value, list):
                tmp = AndroidManifestParser.__parse_list_from_dom(dom, key, value[0])
                if tmp:
                    res[key] = tmp
            else:
                if dom.hasAttribute(attributes[key]):
                    res[key] = dom.getAttribute(attributes[key])
        return res

    @staticmethod
    def __parse_list_from_dom(dom: Element, tag: str, attribute: str) -> List[str]:
        res = []
        for element in dom.getElementsByTagName(tag):
            res.append(element.getAttribute(attribute))
        return sorted(res)

    @staticmethod
    def looks_like_manifest(filename: str) -> bool:
        return filename == "AndroidManifest.xml"
