##
# Parser interface for Android APK package.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

from abc import ABCMeta, abstractmethod


class APKParserInterface(object):
    __metaclass__ = ABCMeta

    ##
    # Check whether a given file looks like a CERT.RSA/DSA certificate file.
    #
    @staticmethod
    @abstractmethod
    def looks_like_an_apk(filename):
        pass

    ##
    # Dump the APK object into a Dictionary.
    #
    # @return A Dictionary representing the APK object.
    #
    @abstractmethod
    def dump(self):
        pass

    ##
    # Retrieve the list of entry files in the APK package.
    #
    # @return The list of files in the APK package.
    #
    @abstractmethod
    def get_file_list(self):
        pass

    ##
    # Retrieve the AndroidManifest object representing the AndroidManifest.xml file of the APK package.
    #
    # @return An AndroidManifest object.
    #
    @abstractmethod
    def get_manifest(self):
        pass

    ##
    # Retrieve the CERT object representing the CERT.RSA/DSA certificate file of the APK package.
    #
    # @return A CERT object.
    #
    @abstractmethod
    def get_cert(self):
        pass

    ##
    # Retrieve the Dex object representing the classes.dex file of the APK package.
    #
    # @return A File object.
    #
    @abstractmethod
    def get_dex(self):
        pass

    ##
    # Retrieve the app name.
    #
    # @return The app name.
    #
    @abstractmethod
    def get_app_name(self):
        pass
