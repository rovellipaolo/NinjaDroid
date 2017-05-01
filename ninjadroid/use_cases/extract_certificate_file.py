from concurrent.futures import Future
from logging import Logger

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
        return self.executor.submit(self.apk.extract_cert_file(self.output_directory))
