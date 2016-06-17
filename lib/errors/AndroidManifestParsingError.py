from lib.errors.ParsingError import ParsingError


##
# AndroidManifest.xml file parsing error.
#
class AndroidManifestParsingError(ParsingError):
    def __init__(self):
        ParsingError.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an AndroidManifest.xml!"
