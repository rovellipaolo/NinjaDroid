import logging
from logging import Logger
import os
import shutil
from zipfile import ZipFile

from ninjadroid.parsers.apk import APK


logger = logging.getLogger(__name__)


class ExtractDexFile:
    """
    Extract the DEX files.
    """

    def __init__(self, logger: Logger = logger):  # noqa
        self.logger = logger

    def execute(self, apk: APK, output_directory: str):
        self.logger.info("Extracting DEX files...")
        apk_filename = apk.get_file_name()
        with ZipFile(apk_filename) as package:
            for dex_file in apk.get_dex_files():
                dex_filename = dex_file.get_file_name()
                self.logger.info("Creating %s/%s...", output_directory, dex_filename)
                dex_abspath = os.path.join(output_directory, dex_filename)
                output_directory = os.path.split(dex_abspath)[0]
                os.makedirs(output_directory, exist_ok=True)
                with package.open(dex_filename) as dex, open(dex_abspath, "wb") as fp:
                    shutil.copyfileobj(dex, fp)
