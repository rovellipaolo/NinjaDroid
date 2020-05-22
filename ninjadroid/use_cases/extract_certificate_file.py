import logging
from logging import Logger
import os
import shutil
from zipfile import ZipFile

from ninjadroid.parsers.apk import APK


logger = logging.getLogger(__name__)


class ExtractCertificateFile:
    """.
    Extract the certificate file (whether its name is CERT.RSA or CERT.DSA or PACKAGE.RSA).
    """

    def __init__(self, logger: Logger = logger):  # noqa
        self.logger = logger

    def execute(self, apk: APK, output_directory: str):
        self.logger.info("Extracting certificate file...")
        with ZipFile(apk.get_file_name()) as package:
            cert = apk.get_cert().get_file_name()
            self.logger.info("Creating %s/%s...", output_directory, cert)
            cert_abspath = os.path.join(output_directory, os.path.basename(cert))
            with package.open(cert) as cert, open(cert_abspath, "wb") as fp:
                shutil.copyfileobj(cert, fp)
