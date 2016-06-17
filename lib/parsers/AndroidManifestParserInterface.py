from abc import ABCMeta, abstractmethod


##
# Parser interface for AndroidManifest.xml file.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#
class AndroidManifestParserInterface(object):
    __metaclass__ = ABCMeta

    ##
    # Check whether a given file looks like an AndroidManifest.xml file.
    #
    @staticmethod
    @abstractmethod
    def looks_like_a_manifest(filename):
        pass

    ##
    # Dump the AndroidManifest object into a Dictionary.
    #
    # @return A Dictionary representing the AndroidManifest object.
    #
    @abstractmethod
    def dump(self):
        pass

    ##
    # Retrieve the package name.
    #
    # @return The package name.
    #
    @abstractmethod
    def get_package_name(self):
        pass

    ##
    # Retrieve the package version.
    #
    # @return The version as a dictionary (i.e. {"code": "...", "name": "..."}).
    #
    @abstractmethod
    def get_version(self):
        pass

    ##
    # Retrieve all the SDK versions.
    #
    # @return The SDK versions as a dictionary (i.e. {'target': "...", 'min': "...", 'max': "..."}).
    #
    @abstractmethod
    def get_sdk_version(self):
        pass

    ##
    # Retrieve the required permissions in the AndroidManifest.xml file.
    #
    # @return The list of required permissions.
    #
    @abstractmethod
    def get_permissions(self):
        pass

    ##
    # Retrieve the number of required permissions in the AndroidManifest.xml file.
    #
    # @return The number of required permissions.
    #
    @abstractmethod
    def get_number_of_permissions(self):
        pass

    ##
    # Retrieve the Activities declared in the AndroidManifest.xml file.
    #
    # @return The list of Activities.
    #
    @abstractmethod
    def get_activities(self):
        pass

    ##
    # Retrieve the number of Activities declared in the AndroidManifest.xml file.
    #
    # @return The number of Activities.
    #
    def get_number_of_activities(self):
        return len(self._activities)

    ##
    # Retrieve the Services declared in the AndroidManifest.xml file.
    #
    # @return The list of Services.
    #
    @abstractmethod
    def get_services(self):
        pass

    ##
    # Retrieve the number of Services declared in the AndroidManifest.xml file.
    #
    # @return The number of Services.
    #
    @abstractmethod
    def get_number_of_services(self):
        pass

    ##
    # Retrieve the BroadcastReceivers declared in the AndroidManifest.xml file.
    #
    # @return The list of BroadcastReceivers.
    #
    @abstractmethod
    def get_broadcast_receivers(self):
        pass

    ##
    # Retrieve the number of BroadcastReceivers declared in the AndroidManifest.xml file.
    #
    # @return The number of BroadcastReceivers.
    #
    @abstractmethod
    def get_number_of_broadcast_receivers(self):
        pass
