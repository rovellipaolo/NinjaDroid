class ParsingError(Exception):
    """
    Generic file parsing error.
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "Cannot parse the file!"
