from lib.errors.ParsingError import ParsingError


##
# Android APK package parsing error.
#
class APKParsingError(ParsingError):
    def __init__(self):
        ParsingError.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an APK!"
