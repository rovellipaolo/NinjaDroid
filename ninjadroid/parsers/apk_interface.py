from abc import ABCMeta, abstractmethod


class APKInterface(metaclass=ABCMeta):
    """
    Parser interface for Android APK package.
    """

    @staticmethod
    @abstractmethod
    def looks_like_an_apk(filename):
        """
        Check whether a given file looks like an APK file.

        :param filename: The name of the file to be checked.
        :return: True if the file looks like an APK file, False otherwise.
        """
        pass

    @abstractmethod
    def dump(self):
        """
        Dump the APK object into a Dictionary.

        :return: A Dictionary representing the APK object.
        """
        pass

    @abstractmethod
    def get_file_list(self):
        """
        Retrieve the list of entry files in the APK package.

        :return: The list of files in the APK package.
        """
        pass

    @abstractmethod
    def get_manifest(self):
        """
        Retrieve the AndroidManifest object representing the AndroidManifest.xml file of the APK package.

        :return: An AndroidManifest object.
        """
        pass

    @abstractmethod
    def get_cert(self):
        """
        Retrieve the CERT object representing the CERT.RSA/DSA certificate file of the APK package.

        :return: A CERT object.
        """
        pass

    @abstractmethod
    def get_dex(self):
        """
        Retrieve the Dex object representing the classes.dex file of the APK package.

        :return: A File object.
        """
        pass

    @abstractmethod
    def get_app_name(self):
        """
        Retrieve the app name.

        :return: The app name.
        """
        pass
