from ninjadroid.errors.parsing_error import ParsingError


class APKParsingError(ParsingError):
    """
    Android APK package parsing error.
    """

    def __init__(self):
        ParsingError.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an APK!"
