from ninjadroid.use_cases.use_case import UseCase


class ExtractDexFile(UseCase):
    """
    Extract classes.dex file to a given output directory.
    """

    def __init__(self, apk, output_directory, logger=None):
        self.apk = apk
        self.output_directory = output_directory
        self.logger = logger

    def execute(self):
        if self.logger:
            self.logger.info("Creating " + self.output_directory + "/classes.dex...")
        self.apk.extract_dex_file(self.output_directory)
