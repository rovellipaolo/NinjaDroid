from logging import getLogger, Logger
import os
import shutil
import tempfile
from typing import Dict, List, Sequence, Union
from zipfile import ZipFile, is_zipfile

from ninjadroid.aapt.aapt import Aapt
from ninjadroid.errors.apk_parsing_error import APKParsingError
from ninjadroid.errors.android_manifest_parsing_error import AndroidManifestParsingError
from ninjadroid.errors.cert_parsing_error import CertParsingError
from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.android_manifest import AndroidManifest
from ninjadroid.parsers.cert import Cert
from ninjadroid.parsers.dex import Dex
from ninjadroid.parsers.file import File


global_logger = getLogger(__name__)


class APK(File):
    """
    Parser implementation for Android APK package.
    """

    _TEMPORARY_DIR = ".ninjadroid"

    def __init__(self, filepath: str, extended_processing: bool = True, logger: Logger = global_logger):
        super().__init__(filepath)
        self.logger = logger

        if not self.looks_like_an_apk(filepath):
            raise APKParsingError

        self._files = []  # type: List
        self._dex_files = []  # type: List[Union[Dex,File]]
        self._extract_and_set_entries(extended_processing)
        if self._manifest is None or self._cert is None:
            raise APKParsingError

        self._app_name = Aapt.get_app_name(filepath)

    def _extract_and_set_entries(self, extended_processing: bool):
        """
        Extract the APK package entries (e.g. AndroidManifest.xml, CERT.RSA, classes.dex, ...) and
        set the corresponding attributes.

        :param extended_processing: If True (default), the URLs and shell commands in the classes.dex will be extracted.
        :return: If one of the APK entries is invalid.
        :raise APKParsingError:
        """
        exists_invalid_entry = False

        apk_filepath = self.get_file_path()
        with ZipFile(apk_filepath) as apk:
            tmpdir = tempfile.mkdtemp(APK._TEMPORARY_DIR)

            for filename in apk.namelist():
                entry_filepath = apk.extract(filename, tmpdir)
                self.logger.debug("Extracting APK resource %s to %s", filename, entry_filepath)

                try:
                    if AndroidManifest.looks_like_a_manifest(filename):
                        self.logger.debug("%s looks like a manifest", filename)
                        self._manifest = AndroidManifest(entry_filepath, True, apk_filepath, extended_processing)
                    elif Cert.looks_like_a_cert(filename):
                        self.logger.debug("%s looks like a certificate", filename)
                        self._cert = self._extract_cert(entry_filepath, filename, extended_processing)
                    elif Dex.looks_like_a_dex(filename):
                        self.logger.debug("%s looks like a DEX", filename)
                        dex = self._extract_dex(entry_filepath, filename, extended_processing)
                        self._dex_files.append(dex)
                    else:
                        self.logger.debug("%s looks like a general resource", filename)
                        if extended_processing and not os.path.isdir(entry_filepath):
                            self._files.append(File(entry_filepath, filename))
                except (ParsingError, AndroidManifestParsingError, CertParsingError):
                    exists_invalid_entry = True

            try:
                shutil.rmtree(tmpdir)
            except OSError:
                pass

            if exists_invalid_entry:
                raise APKParsingError

    @classmethod
    def _extract_cert(cls, filepath: str, filename: str, extended_processing: bool) -> bool:
        if extended_processing:
            return Cert(filepath, filename)
        return File(filepath, filename)

    @classmethod
    def _extract_dex(cls, filepath: str, filename: str, extended_processing: bool) -> bool:
        if extended_processing:
            return Dex(filepath, filename)
        return File(filepath, filename)

    @staticmethod
    def looks_like_an_apk(filename: str) -> bool:
        return File.is_a_file(filename) and is_zipfile(filename)

    def dump(self) -> Dict:
        dump = super().dump()
        dump["name"] = self._app_name
        dump["cert"] = self._cert.dump() if self._cert is not None else None
        dump["manifest"] = self._manifest.dump() if self._manifest is not None else None
        dump["dex"] = [dex.dump() for dex in self._dex_files]
        dump["other"] = []
        for file in self._files:
            dump["other"].append(file.dump())
        return dump

    def get_app_name(self) -> str:
        return self._app_name

    def get_files(self) -> List:
        """
        :return: All files except for AndroidManifest.xml, CERT.DSA/RSA and classes.dex files.
        """
        return self._files

    def get_manifest(self) -> Union[AndroidManifest,File]:
        return self._manifest

    def get_cert(self) -> Union[Cert,File]:
        return self._cert

    def get_dex_files(self) -> Sequence[Union[Dex,File]]:
        return self._dex_files
