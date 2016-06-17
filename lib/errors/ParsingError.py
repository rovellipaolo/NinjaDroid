

##
# Generic file parsing error.
#
class ParsingError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return "Cannot parse the file!"
