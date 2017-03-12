class BuffHandle:
    """
    BuffHandle

    The original AXML parser code comes from Androguard (by Anthony Desnos).
    Link: https://github.com/kzjeef/AxmlParserPY
    """

    def __init__(self, buff):
        self.__buff = buff
        self.__idx = 0

    def read_b(self, size):
        return self.__buff[ self.__idx: self.__idx + size ]

    def read(self, size):
        buff = self.__buff[ self.__idx: self.__idx + size ]
        self.__idx += size
        return buff

    def end(self):
        return self.__idx == len(self.__buff)
