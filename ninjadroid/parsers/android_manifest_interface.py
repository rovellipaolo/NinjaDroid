from abc import ABCMeta, abstractmethod
from typing import Dict, List


class AndroidManifestInterface(metaclass=ABCMeta):
    """
    Parser interface for AndroidManifest.xml file.
    """

    @staticmethod
    @abstractmethod
    def looks_like_a_manifest(filename: str) -> bool:
        """
        Check whether a given file looks like an AndroidManifest.xml file.

        :param filename: The name of the file to be checked.
        :return: True if the file looks like an AndroidManifest.xml file, False otherwise.
        """
        pass

    @abstractmethod
    def dump(self) -> Dict:
        """
        Dump the AndroidManifest object into a Dictionary.

        :return: A Dictionary representing the AndroidManifest object.
        """
        pass

    @abstractmethod
    def get_package_name(self) -> str:
        """
        Retrieve the package name.

        :return: The package name.
        """
        pass

    @abstractmethod
    def get_version(self) -> Dict:
        """
        Retrieve the package version.

        :return: The version as a dictionary (i.e. {"code": "...", "name": "..."}).
        """
        pass

    @abstractmethod
    def get_sdk_version(self) -> Dict:
        """
        Retrieve all the SDK versions.

        :return: The SDK versions as a dictionary (i.e. {'target': "...", 'min': "...", 'max': "..."}).
        """
        pass

    @abstractmethod
    def get_permissions(self) -> List:
        """
        Retrieve the required permissions in the AndroidManifest.xml file.

        :return: The list of required permissions.
        """
        pass

    @abstractmethod
    def get_number_of_permissions(self) -> int:
        """
        Retrieve the number of required permissions in the AndroidManifest.xml file.

        :return: The number of required permissions.
        """
        pass

    @abstractmethod
    def get_activities(self) -> List:
        """
        Retrieve the Activities declared in the AndroidManifest.xml file.

        :return: The list of Activities.
        """
        pass

    def get_number_of_activities(self) -> int:
        """
        Retrieve the number of Activities declared in the AndroidManifest.xml file.

        :return: The number of Activities.
        """
        pass

    @abstractmethod
    def get_services(self) -> List:
        """
        Retrieve the Services declared in the AndroidManifest.xml file.

        :return: The list of Services.
        """
        pass

    @abstractmethod
    def get_number_of_services(self) -> int:
        """
        Retrieve the number of Services declared in the AndroidManifest.xml file.

        :return: The number of Services.
        """
        pass

    @abstractmethod
    def get_broadcast_receivers(self) -> List:
        """
        Retrieve the BroadcastReceivers declared in the AndroidManifest.xml file.

        :return: The list of BroadcastReceivers.
        """
        pass

    @abstractmethod
    def get_number_of_broadcast_receivers(self) -> int:
        """
        Retrieve the number of BroadcastReceivers declared in the AndroidManifest.xml file.

        :return: The number of BroadcastReceivers.
        """
        pass
