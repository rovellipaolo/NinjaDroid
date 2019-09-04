from xml.dom import minidom
from xml.parsers.expat import ExpatError
import json
import os.path
from typing import Any, Dict, List

from ninjadroid.aapt.aapt import Aapt
from ninjadroid.axmlparser.axml_printer import AXMLPrinter
from ninjadroid.parsers.android_manifest_interface import AndroidManifestInterface
from ninjadroid.parsers.file import File
from ninjadroid.errors.android_manifest_parsing_error import AndroidManifestParsingError


class AndroidManifest(File, AndroidManifestInterface):
    __FILE_NAME_ANDROIDMANIFEST_XML = "AndroidManifest.xml"
    __MANIFEST_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "manifest.json")

    def __init__(self, filepath: str, binary: bool = False, apk_path: str = ""):
        super(AndroidManifest, self).__init__(filepath, "AndroidManifest.xml")

        # Load the AndroidManifest.xml structure:
        with open(AndroidManifest.__MANIFEST_CONFIG_FILE, 'r') as config:
            cfg = json.load(config)

        with open(filepath, 'rb') as fp:
            try:
                if binary:
                    self._raw = AXMLPrinter(fp.read()).get_buff()
                    xml = minidom.parseString(self._raw)
                else:
                    xml = minidom.parse(filepath)
            except ExpatError:
                if apk_path != "":
                    apk = Aapt.get_apk_info(apk_path)
                    self._package_name = apk["package_name"]
                    self._version = apk["version"]
                    self._sdk = apk["sdk"]
                    self._permissions = Aapt.get_app_permissions(apk_path)
                    man = Aapt.get_manifest_info(apk_path)
                    self._activities = man["activities"]
                    self._services = man["services"]
                    self._receivers = man["receivers"]
                else:
                    raise AndroidManifestParsingError
            except IOError:
                raise AndroidManifestParsingError
            else:
                manifest = xml.documentElement

                # Extract the package info:
                self._package_name = manifest.getAttribute(cfg['package']['name'])
                self._version = {"code": "", "name": ""}
                try:
                    self._version['code'] = int(manifest.getAttribute(cfg['package']['version']['code']))
                except ValueError:
                    pass
                self._version['name'] = manifest.getAttribute(cfg['package']['version']['name'])

                # Extract the SDK info:
                sdk = self._parse_element_to_list_of_dict(manifest, cfg['uses-sdk'], "uses-sdk")
                if len(sdk) > 0:
                    self._sdk = sdk[0]
                else:
                    self._sdk = {}

                # Extract the permissions info:
                self._permissions = AndroidManifest._parse_element_to_simple_list(manifest,
                                                                                  "uses-permission",
                                                                                  cfg['uses-permission'][0])

                # Extract the application info:
                application = manifest.getElementsByTagName(cfg['application']['tag'])
                application = application[0]
                self._activities = AndroidManifest._parse_element_to_list_of_dict(application,
                                                                                  cfg['application']['activity'],
                                                                                  "activity")
                self._services = AndroidManifest._parse_element_to_list_of_dict(application,
                                                                                cfg['application']['service'],
                                                                                "service")
                self._receivers = AndroidManifest._parse_element_to_list_of_dict(application,
                                                                                 cfg['application']['receiver'],
                                                                                 "receiver")

    @staticmethod
    def looks_like_a_manifest(filename: str) -> bool:
        return filename == AndroidManifest.__FILE_NAME_ANDROIDMANIFEST_XML

    @staticmethod
    def _parse_element_to_simple_list(root: minidom.Element, tag: str, attribute: str) -> List[Any]:
        """
        Parse the simple application elements (i.e. only the "android:name").

        :param root: The XML element.
        :param tag: The root element tag to look for (e.g. "uses-permission", "action", "category", ...).
        :param attribute: The unique tag attribute name (e.g. "android:name").
        :return: The list of attribute values.
        """
        res = []

        for element in root.getElementsByTagName(tag):
            res.append(element.getAttribute(attribute))

        if len(res) > 0:
            res.sort()

        return res

    @staticmethod
    def _parse_element_to_list_of_dict(root: minidom.Element, component: Dict[str, Any], tag: str) -> List[Any]:
        """
        Parse the complex application elements (i.e. parse also the "meta-data" and "intent-filter" information).

        :param root: The XML element.
        :param component: The XML element (dictionary of tag and attributes).
        :param tag: The root element tag (e.g. 'activity', 'service' or 'receiver').
        :return: The list of attribute values.
        """
        res = []

        for element in root.getElementsByTagName(tag):
            data = {}

            for key, value in component.items():
                if type(value) is dict:
                    tmp = AndroidManifest._parse_element_to_list_of_dict(element, component[key], key)
                    if len(tmp) > 0:
                        data[key] = tmp
                elif type(value) is list:
                    tmp = AndroidManifest._parse_element_to_simple_list(element, key, value[0])
                    if len(tmp) > 0:
                        tmp.sort()
                        data[key] = tmp
                else:  # type(value) is str (in Python 2.7 this will be unicode)
                    if element.hasAttribute(component[key]):
                        data[key] = element.getAttribute(component[key])

            res.append(data)

        return res

    def dump(self) -> Dict:
        dump = super(AndroidManifest, self).dump()
        dump["package_name"] = self._package_name
        dump["version"] = self._version
        dump["sdk"] = self._sdk
        dump["permissions"] = self._permissions
        dump["activities"] = self._activities
        dump["services"] = self._services
        dump["receivers"] = self._receivers
        return dump

    def get_package_name(self) -> str:
        return self._package_name

    def get_version(self) -> Dict:
        return self._version

    def get_sdk_version(self) -> Dict:
        return self._sdk

    def get_permissions(self) -> List:
        return self._permissions

    def get_number_of_permissions(self) -> int:
        return len(self._permissions)

    def get_activities(self) -> List:
        return self._activities

    def get_number_of_activities(self) -> int:
        return len(self._activities)

    def get_services(self) -> List:
        return self._services

    def get_number_of_services(self) -> int:
        return len(self._services)

    def get_broadcast_receivers(self) -> List:
        return self._receivers

    def get_number_of_broadcast_receivers(self) -> int:
        return len(self._receivers)
