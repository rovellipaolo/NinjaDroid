from lib.errors.ParsingError import ParsingError


##
# Android CERT.RSA/DSA certificate file parsing error.
#
class CERTParsingError(ParsingError):
    def __init__(self):
        ParsingError.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an Android CERT!"
