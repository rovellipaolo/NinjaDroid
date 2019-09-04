from concurrent.futures import Future
import logging
from logging import Logger
import os
import shutil
from zipfile import ZipFile

from ninjadroid.concurrent.job_executor import JobExecutor
from ninjadroid.parsers.apk import APK
from ninjadroid.use_cases.use_case import UseCase

logger = logging.getLogger(__name__)


class ExtractCertificateFile(UseCase):
    """
    Extract CERT.RSA/DSA file to a given output directory.
    """

    def __init__(self, apk: APK, output_directory: str, logger: Logger = logger):
        self.apk = apk
        self.output_directory = output_directory
        self.logger = logger
        self.executor = JobExecutor()

    def execute(self) -> Future:
        self.logger.info("Extracting certificate to %s...", self.output_directory)
        return self.executor.submit(self.job(self.output_directory))

    def job(self, output_directory: str):
        """
        Extract the certificate file of the APK package (whether its name is CERT.RSA or CERT.DSA or PACKAGE.RSA).

        :param output_directory: The directory where to save the CERT.RSA/DSA file.
        """
        with ZipFile(self.apk.get_file_name()) as package:
            cert = self.apk.get_cert().get_file_name()
            self.logger.info("Extracting %s", cert)

            cert_abspath = os.path.join(output_directory, os.path.basename(cert))
            with package.open(cert) as cert, open(cert_abspath, 'wb') as fp:
                shutil.copyfileobj(cert, fp)
