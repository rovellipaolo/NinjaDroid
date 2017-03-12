from ninjadroid.errors.parsing_error import ParsingError


class CERTParsingError(ParsingError):
    """
    Android CERT.RSA/DSA certificate file parsing error.
    """

    def __init__(self):
        ParsingError.__init__(self)

    def __str__(self):
        return "Cannot parse the file as an Android CERT!"
