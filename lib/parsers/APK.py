import os
import shutil
import tempfile
from zipfile import ZipFile, is_zipfile

from lib.aapt.Aapt import Aapt
from lib.errors.APKParsingError import APKParsingError
from lib.errors.AndroidManifestParsingError import AndroidManifestParsingError
from lib.errors.CERTParsingError import CERTParsingError
from lib.errors.ParsingError import ParsingError
from lib.parsers.APKParserInterface import APKParserInterface
from lib.parsers.AndroidManifest import AndroidManifest
from lib.parsers.Dex import Dex
from lib.parsers.CERT import CERT
from lib.parsers.File import File


##
# Parser implementation for Android APK package.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#
class APK(File, APKParserInterface):
    _TEMPORARY_DIR = ".ninjadroid"

    ##
    # Class constructor.
    #
    # @param filepath  The path of the APK package.
    # @param string_processing  If True (default), the URLs and shell commands in the classes.dex will be extracted.
    # @throw APKParsingError  If it is not a valid APK package.
    #
    def __init__(self, filepath, string_processing=True):
        super(APK, self).__init__(filepath)

        if not self.looks_like_an_apk(filepath):
            raise APKParsingError

        self._files = []
        self._extract_and_set_entries(string_processing)

        if len(self._files) == 0 or self._cert is None:
            raise APKParsingError

        self._app_name = Aapt.get_app_name(filepath)

    ##
    # Extract the APK package entries (e.g. AndroidManifest.xml, CERT.RSA, classes.dex, ...) and
    # set the correspondent attributes.
    #
    # @param string_processing  If True (default), the URLs and shell commands in the classes.dex will be extracted.
    # @throw APKParsingError  If one of the APK entries is invalid.
    #
    def _extract_and_set_entries(self, string_processing):
        exists_invalid_entry = False

        apk_filepath = self.get_file_path()
        with ZipFile(apk_filepath) as apk:
            tmpdir = tempfile.mkdtemp(APK._TEMPORARY_DIR)

            for filename in apk.namelist():
                entry_filepath = apk.extract(filename, tmpdir)

                try:
                    if AndroidManifest.looks_like_a_manifest(filename):
                        self._manifest = AndroidManifest(entry_filepath, True, apk_filepath)
                    elif CERT.looks_like_a_cert(filename):
                        self._cert = CERT(entry_filepath, filename)
                    elif Dex.looks_like_a_dex(filename):
                        self._dex = Dex(entry_filepath, string_processing)
                    else:
                        if not os.path.isdir(entry_filepath):
                            self._files.append(File(entry_filepath, filename))
                except (ParsingError, AndroidManifestParsingError, CERTParsingError):
                    exists_invalid_entry = True

            try:
                shutil.rmtree(tmpdir)
            except OSError:
                pass

            if exists_invalid_entry:
                raise APKParsingError

    @staticmethod
    def looks_like_an_apk(filepath):
        return File.is_a_file(filepath) and is_zipfile(filepath)

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

    def get_file_list(self):
        return self._files

    def get_manifest(self):
        return self._manifest

    def get_cert(self):
        return self._cert

    def get_dex(self):
        return self._dex

    def get_app_name(self):
        return self._app_name

    ##
    # Extract the certificate file of the APK package (whether its name is CERT.RSA or CERT.DSA or PACKAGE.RSA...).
    #
    # @param output_directory  The directory where to save the CERT.RSA/DSA file.
    #
    def extract_cert_file(self, output_directory):
        with ZipFile(self._name) as apk:
            cert_file_name = self._cert.get_file_name()
            cert_abspath = os.path.join(output_directory, os.path.basename(cert_file_name))
            with apk.open(cert_file_name) as cert, open(cert_abspath, 'wb') as fp:
                shutil.copyfileobj(cert, fp)

    ##
    # Extract the classes.dex file of the APK package.
    #
    # @param output_directory  The directory where to save the classes.dex file.
    #
    def extract_dex_file(self, output_directory):
        with ZipFile(self._name) as apk:
            dex_file_name = self._dex.get_file_name()
            dex_abspath = os.path.join(output_directory, dex_file_name)
            with apk.open(dex_file_name) as dex, open(dex_abspath, 'wb') as fp:
                shutil.copyfileobj(dex, fp)
