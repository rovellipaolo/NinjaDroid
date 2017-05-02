from concurrent.futures import Future
from logging import Logger
import os
import shutil
from zipfile import ZipFile

from ninjadroid.concurrent.job_executor import JobExecutor
from ninjadroid.parsers.apk import APK
from ninjadroid.use_cases.use_case import UseCase


class ExtractCertificateFile(UseCase):
    """
    Extract CERT.RSA/DSA file to a given output directory.
    """

    def __init__(self, apk: APK, output_directory: str, logger: Logger = None):
        self.apk = apk
        self.output_directory = output_directory
        self.logger = logger
        self.executor = JobExecutor()

    def execute(self) -> Future:
        if self.logger:
            self.logger.info("Creating " + self.output_directory + "/CERT.RSA...")
        return self.executor.submit(self.job(self.output_directory))

    def job(self, output_directory: str):
        """
        Extract the certificate file of the APK package (whether its name is CERT.RSA or CERT.DSA or PACKAGE.RSA).

        :param output_directory: The directory where to save the CERT.RSA/DSA file.
        """
        with ZipFile(self.apk.get_file_name()) as package:
            cert = self.apk.get_cert().get_file_name()
            cert_abspath = os.path.join(output_directory, os.path.basename(cert))
            with package.open(cert) as cert, open(cert_abspath, 'wb') as fp:
                shutil.copyfileobj(cert, fp)
