##
# @file APK.py
# @brief Parser for Android APK package.
# @version 1.5
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

from fnmatch import fnmatch
import os
import shutil
import tempfile
from zipfile import ZipFile, is_zipfile

from lib.Aapt import Aapt
from lib.AndroidManifest import AndroidManifest, ErrorAndroidManifestParsing
from lib.CERT import CERT, ErrorCERTParsing
from lib.Dex import Dex
from lib.File import File, ErrorFileParsing


##
# ErrorAPKParsing class.
#
class ErrorAPKParsing(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an APK!"


##
# APK class.
#
class APK(File, object):
    _TEMPORARY_DIR = ".ninjadroid"
    _CERT_FILE_RSA = "META-INF/CERT.RSA"
    _CERT_FILE_DSA = "META-INF/CERT.DSA"
    _CERT_FILE_ALT_REGEX = "META-INF/*.RSA"
    _DEX_FILE = "classes.dex"
    _MANIFEST_FILE = "AndroidManifest.xml"

    ##
    # Class constructor.
    #
    # @param filepath  The Android APK package file path.
    # @param string_processing  If set to True (dafault), the URLs and shell commands in the classes.dex will be extracted.
    #
    def __init__(self, filepath, string_processing=True):
        super(APK, self).__init__(filepath)

        # Check if the file is a ZIP (file header signature should be 0x04034b50 in little-endian):
        if not is_zipfile(filepath):
            raise ErrorAPKParsing

        # Extract the certificate file with which the APK package as been signed:
        self._files = []
        with ZipFile(filepath) as apk:
            tmpdir = tempfile.mkdtemp(APK._TEMPORARY_DIR)

            for filename in apk.namelist():
                file = apk.extract(filename, tmpdir)

                try:
                    if filename == APK._MANIFEST_FILE:
                        self._manifest = AndroidManifest(file, True, filepath)
                    elif filename == APK._CERT_FILE_RSA or filename == APK._CERT_FILE_DSA or fnmatch(filename, APK._CERT_FILE_ALT_REGEX):
                        self._cert = CERT(file, filename)
                    elif filename == APK._DEX_FILE:
                        self._dex = Dex(file, string_processing)
                    else:
                        if not os.path.isdir(file):
                            self._files.append(File(file, filename))
                except (ErrorFileParsing, ErrorAndroidManifestParsing, ErrorCERTParsing):
                    raise ErrorAPKParsing

            try:
                shutil.rmtree(tmpdir)
            except OSError:
                pass

        # Check if the file is a valid APK:
        if len(self._files) == 0 or self._cert is None:  #  or self._manifest is None or self._dex is None
            raise ErrorAPKParsing
        self._app_name = Aapt.get_app_name(filepath)

    ##
    # Dump the APK object.
    #
    # @return A Dictionary representing the APK object.
    #
    def dump(self):
        dump = super(APK, self).dump()
        dump["app_name"] = self._app_name
        dump["cert"] = self._cert.dump() if self._cert is not None else None
        dump["manifest"] = self._manifest.dump() if self._manifest is not None else None
        dump["dex"] = self._dex.dump() if self._dex is not None else None
        dump["other_files"] = []
        for file in self._files:
            dump["other_files"].append(file.dump())
        return dump

    ##
    # Retrieve the list of entry files in the APK package.
    #
    # @return The list of files in the APK package.
    #
    def get_file_list(self):
        return self._files

    ##
    # Retrieve the AndroidManifest object representing the AndroidManifest.xml file of the APK package.
    #
    # @return An AndroidManifest object.
    #
    def get_manifest(self):
        return self._manifest

    ##
    # Retrieve the CERT object representing the CERT.RSA/DSA certificate file of the APK package.
    #
    # @return A CERT object.
    #
    def get_cert(self):
        return self._cert

    ##
    # Retrieve the File object representing the classes.dex file of the APK package.
    #
    # @return A File object.
    #
    def get_dex(self):
        return self._dex

    ##
    # Retrieve the app name.
    #
    # @return The app name.
    #
    def get_app_name(self):
        return self._app_name

    ##
    # Extract the CERT.RSA/DSA certificate file of the APK package.
    #
    # @param output_dir  The directory where to save the CERT.RSA/DSA file.
    #
    def extract_cert_file(self, output_dir):
        with ZipFile(self._name) as apk:
            # Retrieve the CERT name (whether it is CERT.RSA or CERT.DSA or PACKAGE.RSA...):
            cert_name = self._cert.get_file_name()
            with apk.open(cert_name) as cert, open(os.path.join(output_dir, os.path.basename(cert_name)), 'wb') as fp:
                shutil.copyfileobj(cert, fp)

    ##
    # Extract the classes.dex file of the APK package.
    #
    # @param output_dir  The directory where to save the classes.dex file.
    #
    def extract_dex_file(self, output_dir):
        with ZipFile(self._name) as apk:
            with apk.open(APK._DEX_FILE) as dex, open(os.path.join(output_dir, APK._DEX_FILE), 'wb') as fp:
                shutil.copyfileobj(dex, fp)
