from ninjadroid.errors.parsing_error import ParsingError


class AndroidManifestParsingError(ParsingError):
    """
    AndroidManifest.xml file parsing error.
    """

    def __init__(self):
        ParsingError.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an AndroidManifest.xml!"
