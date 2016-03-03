##
# Parser for AndroidManifest.xml file.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

from xml.dom import minidom
from xml.parsers.expat import ExpatError
import json

from lib.Aapt import Aapt
from lib.AXMLParser import AXMLPrinter
from lib.parsers.AndroidManifestParserInterface import AndroidManifestParserInterface
from lib.parsers.File import File
from lib.errors.AndroidManifestParsingError import AndroidManifestParsingError


class AndroidManifest(File, AndroidManifestParserInterface):
    __FILE_NAME_ANDROIDMANIFEST_XML = "AndroidManifest.xml"
    __MANIFEST_CONFIG_FILE = "etc/manifest.json"

    ##
    # Class constructor.
    #
    # @param filepath  The AndroidManifest.xml file path.
    # @param binary  true if the AndroidManifest.xml file is in binary format, false otherwise.
    # @param apk_path  The Android APK package (to which the AndroidManifest.xml belongs) file path. This is used (by Aapt) as a fall back mechanism.
    #
    def __init__(self, filepath, binary=False, apk_path=""):
        super(AndroidManifest, self).__init__(filepath, "AndroidManifest.xml")

        # Load the AndroidManifest.xml structure:
        with open(AndroidManifest.__MANIFEST_CONFIG_FILE, 'r') as config:
            cfg = json.load(config)

        with open(filepath, 'rb') as fp:
            try:
                if binary:
                    self._raw = AXMLPrinter(fp.read()).getBuff()
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
                self._permissions = AndroidManifest._parse_element_to_simple_list(manifest, "uses-permission", cfg['uses-permission'][0])

                # Extract the application info:
                application = manifest.getElementsByTagName(cfg['application']['tag'])
                application = application[0]
                self._activities = AndroidManifest._parse_element_to_list_of_dict(application, cfg['application']['activity'], "activity")
                self._services = AndroidManifest._parse_element_to_list_of_dict(application, cfg['application']['service'], "service")
                self._receivers = AndroidManifest._parse_element_to_list_of_dict(application, cfg['application']['receiver'], "receiver")

    @staticmethod
    def looks_like_a_manifest(filename):
        return filename == AndroidManifest.__FILE_NAME_ANDROIDMANIFEST_XML

    ##
    # Parse the simple application elements (i.e. only the "android:name").
    #
    # @param root  The XML element.
    # @param tag  The root element tag to look for (e.g. "uses-permission", "action", "category", ...).
    # @param attribute  The unique tag attribute name (e.g. "android:name").
    # @return The list of attribute values.
    #
    @staticmethod
    def _parse_element_to_simple_list(root, tag, attribute):
        res = []

        for element in root.getElementsByTagName(tag):
            res.append(element.getAttribute(attribute))

        if len(res) > 0:
            res.sort()

        return res

    ##
    # Parse the complex application elements (i.e. parse also the "meta-data" and "intent-filter" information).
    #
    # @param root  The XML element.
    # @param component  The XML element (dictionary of tag and attributes).
    # @param tag  The root element tag (e.g. 'activity', 'service' or 'receiver').
    # @return The list of attribute values.
    #
    @staticmethod
    def _parse_element_to_list_of_dict(root, component, tag):
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

    def dump(self):
        dump = super(AndroidManifest, self).dump()
        dump["package_name"] = self._package_name
        dump["version"] = self._version
        dump["sdk"] = self._sdk
        dump["permissions"] = self._permissions
        dump["activities"] = self._activities
        dump["services"] = self._services
        dump["receivers"] = self._receivers
        return dump

    def get_package_name(self):
        return self._package_name

    def get_version(self):
        return self._version

    def get_sdk_version(self):
        return self._sdk

    def get_permissions(self):
        return self._permissions

    def get_number_of_permissions(self):
        return len(self._permissions)

    def get_activities(self):
        return self._activities

    def get_number_of_activities(self):
        return len(self._activities)

    def get_services(self):
        return self._services

    def get_number_of_services(self):
        return len(self._services)

    def get_broadcast_receivers(self):
        return self._receivers

    def get_number_of_broadcast_receivers(self):
        return len(self._receivers)
