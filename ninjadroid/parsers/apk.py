from logging import getLogger, Logger
from shutil import rmtree
from tempfile import mkdtemp
from typing import Dict, List, Optional, Union
from zipfile import ZipFile

from ninjadroid.aapt.aapt import Aapt
from ninjadroid.parsers.manifest import AndroidManifest, AndroidManifestParser, AndroidManifestParsingError
from ninjadroid.parsers.cert import Cert, CertParser, CertParsingError
from ninjadroid.parsers.dex import Dex, DexParser
from ninjadroid.parsers.file import File, FileParser, FileParsingError


default_logger = getLogger(__name__)


class APK(File):
    """
    Android APK package information.
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            filename: str,
            size: str,
            md5hash: str,
            sha1hash: str,
            sha256hash: str,
            sha512hash: str,
            app_name: str,
            cert: Cert,
            manifest: AndroidManifest,
            dex_files: List[Dex],
            other_files: List[File]
    ):
        super().__init__(filename, size, md5hash, sha1hash, sha256hash, sha512hash)
        self.__app_name = app_name
        self.__cert = cert
        self.__manifest = manifest
        self.__dex = dex_files
        self.__other = other_files

    def get_app_name(self) -> str:
        return self.__app_name

    def get_cert(self) -> Union[Cert,File]:
        return self.__cert

    def get_manifest(self) -> Union[AndroidManifest,File]:
        return self.__manifest

    def get_dex_files(self) -> List[Union[Dex,File]]:
        return self.__dex

    def get_other_files(self) -> List[File]:
        return self.__other

    def as_dict(self) -> Dict:
        dump = super().as_dict()
        dump["name"] = self.__app_name
        dump["cert"] = self.__cert.as_dict()
        dump["manifest"] = self.__manifest.as_dict()
        dump["dex"] = [dex.as_dict() for dex in self.__dex]
        dump["other"] = [file.as_dict() for file in self.__other]
        return dump



class ApkParsingError(FileParsingError):
    """
    Android APK package parsing error.
    """

    def __init__(self):
        FileParsingError.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an APK!"


class ApkParser:
    """
    Parser implementation for Android APK packages.
    """

    __TEMPORARY_DIR = ".ninjadroid"

    def __init__(self, logger: Logger = default_logger):
        self.logger = logger
        self.file_parser = FileParser(logger)
        self.manifest_parser = AndroidManifestParser(logger)
        self.cert_parser = CertParser(logger)
        self.dex_parser = DexParser(logger)

    def parse(self, filepath: str, extended_processing: bool = True):
        """
        :param filepath: path of the APK file
        :param extended_processing: (optional) whether should parse all information or only a summary. True by default.
        :return: the parsed APK file
        :raise: ApkParsingError if cannot parse the file as an APK
        """
        self.logger.debug("Parsing APK file: filepath=\"%s\"", filepath)
        if not self.looks_like_apk(filepath):
            raise ApkParsingError

        file = self.file_parser.parse(filepath)
        cert = None
        manifest = None
        dex_files = []
        other_files = []

        with ZipFile(filepath) as apk:
            tmpdir = self.__create_temporary_directory(ApkParser.__TEMPORARY_DIR)
            for filename in apk.namelist():
                entry_filepath = apk.extract(filename, tmpdir)
                self.logger.debug("Extracting APK resource %s to %s", filename, entry_filepath)
                try:
                    if AndroidManifestParser.looks_like_manifest(filename):
                        self.logger.debug("%s looks like an AndroidManifest.xml file", filename)
                        manifest = self.manifest_parser.parse(entry_filepath, True, filepath, extended_processing)
                    elif CertParser.looks_like_cert(filename):
                        self.logger.debug("%s looks like a CERT file", filename)
                        cert = self.__parse_cert(entry_filepath, filename, extended_processing)
                    elif DexParser.looks_like_dex(filename):
                        self.logger.debug("%s looks like a dex file", filename)
                        dex = self.__parse_dex(entry_filepath, filename, extended_processing)
                        dex_files.append(dex)
                    else:
                        self.logger.debug("%s looks like a generic file", filename)
                        entry = self.__parse_file(entry_filepath, filename, extended_processing)
                        if entry is not None:
                            other_files.append(entry)
                except (AndroidManifestParsingError, CertParsingError, FileParsingError) as error:
                    self.__remove_directory(tmpdir)
                    raise ApkParsingError from error
            self.__remove_directory(tmpdir)

        if manifest is None or cert is None or not dex_files:
            raise ApkParsingError

        return APK(
            filename=file.get_file_name(),
            size=file.get_size(),
            md5hash=file.get_md5(),
            sha1hash=file.get_sha1(),
            sha256hash=file.get_sha256(),
            sha512hash=file.get_sha512(),
            app_name=Aapt.get_app_name(filepath),
            cert=cert,
            manifest=manifest,
            dex_files=dex_files,
            other_files=other_files
        )

    def __parse_cert(self, filepath: str, filename: str, extended_processing: bool) -> Union[Cert,File]:
        if extended_processing:
            return self.cert_parser.parse(filepath, filename)
        return self.file_parser.parse(filepath, filename)

    def __parse_dex(self, filepath: str, filename: str, extended_processing: bool) -> Union[Dex,File]:
        if extended_processing:
            return self.dex_parser.parse(filepath, filename)
        return self.file_parser.parse(filepath, filename)

    def __parse_file(self, filepath: str, filename: str, extended_processing: bool) -> Optional[File]:
        if extended_processing and not FileParser.is_directory(filepath):
            try:
                return self.file_parser.parse(filepath, filename)
            except FileParsingError:
                self.logger.error("Could not parse file '%s'!", filename)
        return None

    @staticmethod
    def __create_temporary_directory(path: str) -> str:
        return mkdtemp(path)

    @staticmethod
    def __remove_directory(path: str):
        try:
            rmtree(path)
        except OSError:
            pass

    @staticmethod
    def looks_like_apk(filename: str) -> bool:
        return FileParser.is_zip_file(filename)
