from abc import ABCMeta, abstractmethod
from typing import Dict, List, Sequence

from ninjadroid.parsers.android_manifest import AndroidManifest
from ninjadroid.parsers.cert import Cert
from ninjadroid.parsers.dex import Dex


class APKInterface(metaclass=ABCMeta):
    """
    Parser interface for Android APK package.
    """

    @staticmethod
    @abstractmethod
    def looks_like_an_apk(filename: str) -> bool:
        """
        Check whether a given file looks like an APK file.

        :param filename: The name of the file to be checked.
        :return: True if the file looks like an APK file, False otherwise.
        """
        pass

    @abstractmethod
    def dump(self) -> Dict:
        """
        Dump the APK object into a Dictionary.

        :return: A Dictionary representing the APK object.
        """
        pass

    @abstractmethod
    def get_file_list(self) -> List:
        """
        Retrieve the list of entry files in the APK package.

        :return: The list of files in the APK package.
        """
        pass

    @abstractmethod
    def get_manifest(self) -> AndroidManifest:
        """
        Retrieve the AndroidManifest object representing the AndroidManifest.xml file of the APK package.

        :return: An AndroidManifest object.
        """
        pass

    @abstractmethod
    def get_cert(self) -> Cert:
        """
        Retrieve the Cert object representing the CERT.RSA/DSA certificate file of the APK package.

        :return: A Cert object.
        """
        pass

    @abstractmethod
    def get_dex_files(self) -> Sequence[Dex]:
        """
        Retrieve the Dex object representing the classes.dex file of the APK package.

        :return: A Dex object.
        """
        pass

    @abstractmethod
    def get_app_name(self) -> str:
        """
        Retrieve the app name.

        :return: The app name.
        """
        pass
