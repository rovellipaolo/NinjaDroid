##
# @file AXMLParser.py
# @brief AXML parser.
# @author Anthony Desnos <desnos at t0t0.fr>
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#
# The original AXML parser code comes from Androguard (by Anthony Desnos).
# Link: https://github.com/kzjeef/AxmlParserPY
#


from struct import pack, unpack


TYPE_NULL = 0
TYPE_REFERENCE = 1
TYPE_ATTRIBUTE = 2
TYPE_STRING = 3
TYPE_FLOAT = 4
TYPE_DIMENSION = 5
TYPE_FRACTION = 6
TYPE_FIRST_INT = 16
TYPE_INT_DEC = 16
TYPE_INT_BOOLEAN = 18
TYPE_FIRST_COLOR_INT = 28
TYPE_INT_COLOR_ARGB4 = 30
TYPE_INT_COLOR_ARGB8 = 28
TYPE_INT_COLOR_RGB4 = 31
TYPE_INT_COLOR_RGB8 = 29
TYPE_INT_DEC = 16
TYPE_INT_HEX = 17
TYPE_LAST_COLOR_INT = 31
TYPE_LAST_INT = 31

RADIX_MULTS = [0.00390625, 3.051758E-005, 1.192093E-007, 4.656613E-010]
DIMENSION_UNITS = ["px","dip","sp","pt","in","mm","",""]
FRACTION_UNITS = ["%","%p","","","","","",""]

COMPLEX_UNIT_MASK = 15

ATTRIBUTE_IX_NAMESPACE_URI = 0
ATTRIBUTE_IX_NAME = 1
ATTRIBUTE_IX_VALUE_STRING = 2
ATTRIBUTE_IX_VALUE_TYPE = 3
ATTRIBUTE_IX_VALUE_DATA = 4
ATTRIBUTE_LENGTH = 5

CHUNK_AXML_FILE = 0x00080003
CHUNK_RESOURCEIDS = 0x00080180
CHUNK_XML_FIRST = 0x00100100
CHUNK_XML_START_NAMESPACE = 0x00100100
CHUNK_XML_END_NAMESPACE = 0x00100101
CHUNK_XML_START_TAG = 0x00100102
CHUNK_XML_END_TAG = 0x00100103
CHUNK_XML_TEXT = 0x00100104
CHUNK_XML_LAST = 0x00100104

START_DOCUMENT = 0
END_DOCUMENT = 1
START_TAG = 2
END_TAG = 3
TEXT = 4

# little-endian (<) unsigned long (L)
UNPACK_FORMAT_LITTLEENDIAN_LONG = "<L"
# native (=) unsigned long (L)
UNPACK_FORMAT_NATIVE_LONG = "=L"


class AXMLPrinter:
    ##
    # Class constructor.
    #
    # @param raw  The raw buffer of an binary XML file.
    #
    def __init__(self, raw):
        self.axml = AXMLParser(raw)
        self.xmlns = False

        self.buff = ""

        while 1:
            _type = self.axml.next()

            if _type == START_DOCUMENT:
                self.buff += "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
            elif _type == START_TAG:
                self.buff += "<%s%s\n" % (self.__getPrefix(self.axml.getPrefix()), self.axml.getName())

                # FIXME: use namespace
                if self.xmlns == False:
                    self.buff += "xmlns:%s=\"%s\"\n" % (self.axml.getNamespacePrefix(0), self.axml.getNamespaceUri(0))
                    self.xmlns = True

                for i in range(0, self.axml.getAttributeCount()):
                    self.buff += "%s%s=\"%s\"\n" % (self.__getPrefix(self.axml.getAttributePrefix(i)), self.axml.getAttributeName(i), self.__getAttributeValue(i))

                self.buff += ">\n"
            elif _type == END_TAG:
                self.buff += "</%s%s>\n" % (self.__getPrefix(self.axml.getPrefix()), self.axml.getName())
            elif _type == TEXT:
                self.buff += "%s\n" % self.axml.getText()
            elif _type == END_DOCUMENT:
                break

    ##
    # Return the entire XML encoded in UTF-8.
    #
    def getBuff(self):
        return self.buff.encode("utf-8")

    def __getPrefix(self, prefix):
        if prefix == None or len(prefix) == 0:
            return ""

        return prefix + ":"

    ##
    # Retrieve an attribute value.
    #
    def __getAttributeValue(self, index):
        _type = self.axml.getAttributeValueType(index)
        _data = self.axml.getAttributeValueData(index)

        #print _type, _data
        if _type == TYPE_STRING:
            return self.axml.getAttributeValue(index)
        elif _type == TYPE_ATTRIBUTE:
            return "?%s%08X" % (self.getPackage(_data), _data)
        elif _type == TYPE_REFERENCE:
            return "@%s%08X" % (self.getPackage(_data), _data)
        # WIP
        elif _type == TYPE_FLOAT:
            return "%f" % unpack("=f", pack("=L", _data))[0]
        elif _type == TYPE_INT_HEX:
            return "0x%08X" % _data
        elif _type == TYPE_INT_BOOLEAN:
            if _data == 0:
                return "false"
            return "true"
        elif _type == TYPE_DIMENSION:
            return "%f%s" % (self.complexToFloat(_data), DIMENSION_UNITS[_data & COMPLEX_UNIT_MASK])
        elif _type == TYPE_FRACTION:
            return "%f%s" % (self.complexToFloat(_data), FRACTION_UNITS[_data & COMPLEX_UNIT_MASK])
        elif _type >= TYPE_FIRST_COLOR_INT and _type <= TYPE_LAST_COLOR_INT:
            return "#%08X" % _data
        elif _type >= TYPE_FIRST_INT and _type <= TYPE_LAST_INT:
            if _data > 0x7fffffff:
                _data = (0x7fffffff & _data) - 0x80000000
                return "%d" % _data
            elif _type == TYPE_INT_DEC:
                return "%d" % _data

        # raise exception here?
        return "<0x%X, type 0x%02X>" % (_data, _type)

    def complexToFloat(self, xcomplex):
        return (float)(xcomplex & 0xFFFFFF00) * RADIX_MULTS[(xcomplex>>4) & 3];

    def getPackage(self, id):
        if id >> 24 == 1:
            return "android:"
        return ""


class AXMLParser:

    def __init__(self, raw_buff):
        self.reset()

        self.buff = BuffHandle(raw_buff)

        self.buff.read(12)

        self.sb = StringBlock(self.buff)

        self.m_resourceIDs = []
        self.m_prefixuri = {}
        self.m_uriprefix = {}
        self.m_prefixuriL = []

    def reset(self):
        self.m_event = -1
        self.m_lineNumber = -1
        self.m_name = -1
        self.m_namespaceUri = -1
        self.m_attributes = []
        self.m_idAttribute = -1
        self.m_classAttribute = -1
        self.m_styleAttribute = -1

    def next(self):
        self.doNext()
        return self.m_event

    def doNext(self):
        if self.m_event == END_DOCUMENT:
            return

        event = self.m_event

        self.reset()

        while 1:
            chunkType = -1

            # Fake END_DOCUMENT event.
            if event == END_TAG:
                pass

            # START_DOCUMENT
            if event == START_DOCUMENT:
                chunkType = CHUNK_XML_START_TAG
            else:
                if self.buff.end() == True:
                    self.m_event = END_DOCUMENT
                    break
                chunkType = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]

            if chunkType == CHUNK_RESOURCEIDS:
                chunkSize = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                # FIXME
                if chunkSize < 8 or chunkSize%4 != 0:
                    raise("ooo")

                for i in range(0, int(chunkSize/4-2)):
                    self.m_resourceIDs.append(unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0])

                continue

            # FIXME
            if chunkType < CHUNK_XML_FIRST or chunkType > CHUNK_XML_LAST:
                raise("ooo")

            # Fake START_DOCUMENT event.
            if chunkType == CHUNK_XML_START_TAG and event == -1:
                self.m_event = START_DOCUMENT
                break

            self.buff.read(4) #/*chunkSize*/
            lineNumber = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
            self.buff.read(4) #0xFFFFFFFF

            if chunkType == CHUNK_XML_START_NAMESPACE or chunkType == CHUNK_XML_END_NAMESPACE:
                if chunkType == CHUNK_XML_START_NAMESPACE:
                    prefix = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                    uri = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]

                    self.m_prefixuri[ prefix ] = uri
                    self.m_uriprefix[ uri ] = prefix
                    self.m_prefixuriL.append((prefix, uri))
                else:
                    self.buff.read(4)
                    self.buff.read(4)
                    (prefix, uri) = self.m_prefixuriL.pop()
                    #del self.m_prefixuri[ prefix ]
                    #del self.m_uriprefix[ uri ]

                continue

            self.m_lineNumber = lineNumber

            if chunkType == CHUNK_XML_START_TAG:
                self.m_namespaceUri = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                self.m_name = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]

                # FIXME
                self.buff.read(4) #flags

                attributeCount = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                self.m_idAttribute = (attributeCount>>16) - 1
                attributeCount = attributeCount & 0xFFFF
                self.m_classAttribute = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                self.m_styleAttribute = (self.m_classAttribute>>16) - 1

                self.m_classAttribute = (self.m_classAttribute & 0xFFFF) - 1

                for i in range(0, attributeCount * ATTRIBUTE_LENGTH):
                    self.m_attributes.append(unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0])

                for i in range(ATTRIBUTE_IX_VALUE_TYPE, len(self.m_attributes), ATTRIBUTE_LENGTH):
                    self.m_attributes[i] = (self.m_attributes[i]>>24)

                self.m_event = START_TAG
                break

            if chunkType == CHUNK_XML_END_TAG:
                self.m_namespaceUri = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                self.m_name = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                self.m_event = END_TAG
                break

            if chunkType == CHUNK_XML_TEXT:
                self.m_name = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]

                # FIXME
                self.buff.read(4) #?
                self.buff.read(4) #?

                self.m_event = TEXT
                break

    def getPrefixByUri(self, uri):
        try:
            return self.m_uriprefix[ uri ]
        except KeyError:
            return -1

    def getPrefix(self):
        try:
            return self.sb.getRaw(self.m_prefixuri[ self.m_namespaceUri ])
        except KeyError:
            return ""

    def getName(self):
        if self.m_name == -1 or (self.m_event != START_TAG and self.m_event != END_TAG):
            return ""

        return self.sb.getRaw(self.m_name)

    def getText(self):
        if self.m_name == -1 or self.m_event != TEXT:
            return ""

        return self.sb.getRaw(self.m_name)

    def getNamespacePrefix(self, pos):
        prefix = self.m_prefixuriL[ pos ][0]
        return self.sb.getRaw(prefix)

    def getNamespaceUri(self, pos):
        uri = self.m_prefixuriL[ pos ][1]
        return self.sb.getRaw(uri)

    def getNamespaceCount(self, pos):
        pass

    def getAttributeOffset(self, index):
        # FIXME
        if self.m_event != START_TAG:
            raise("Current event is not START_TAG.")

        offset = index * 5
        # FIXME
        if offset >= len(self.m_attributes):
            raise("Invalid attribute index")

        return offset

    def getAttributeCount(self):
        if self.m_event != START_TAG:
            return -1

        return int(len(self.m_attributes) / ATTRIBUTE_LENGTH)

    def getAttributePrefix(self, index):
        offset = self.getAttributeOffset(index)
        uri = self.m_attributes[offset + ATTRIBUTE_IX_NAMESPACE_URI]

        prefix = self.getPrefixByUri(uri)
        if prefix == -1:
            return ""

        return self.sb.getRaw(prefix)

    def getAttributeName(self, index):
        offset = self.getAttributeOffset(index)
        name = self.m_attributes[offset + ATTRIBUTE_IX_NAME]

        if name == -1:
            return ""

        return self.sb.getRaw(name)

    def getAttributeValueType(self, index):
        offset = self.getAttributeOffset(index)
        return self.m_attributes[offset + ATTRIBUTE_IX_VALUE_TYPE]

    def getAttributeValueData(self, index):
        offset = self.getAttributeOffset(index)
        return self.m_attributes[offset + ATTRIBUTE_IX_VALUE_DATA]

    def getAttributeValue(self, index):
        offset = self.getAttributeOffset(index)
        valueType = self.m_attributes[offset + ATTRIBUTE_IX_VALUE_TYPE]
        if valueType == TYPE_STRING:
            valueString = self.m_attributes[offset + ATTRIBUTE_IX_VALUE_STRING]
            return self.sb.getRaw(valueString)
        # WIP
        return ""
        #int valueData=m_attributes[offset+ATTRIBUTE_IX_VALUE_DATA];
        #return TypedValue.coerceToString(valueType,valueData);


class BuffHandle:
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

##
# axml format translated from:
# http://code.google.com/p/android4me/source/browse/src/android/content/res/AXmlResourceParser.java
#
class StringBlock:
    def __init__(self, buff):
        self.chunkSize = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0]
        self.stringCount = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0]
        self.styleOffsetCount = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0]

        # unused value ?
        buff.read(4)

        self.stringsOffset = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0]
        self.stylesOffset = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0]

        self.m_stringOffsets = []
        self.m_styleOffsets = []
        self.m_strings = []
        self.m_styles = []

        for i in range(0, self.stringCount):
            self.m_stringOffsets.append(unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0])

        for i in range(0, self.styleOffsetCount):
            self.m_stylesOffsets.append(unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0])

        size = self.chunkSize - self.stringsOffset
        if self.stylesOffset != 0:
            size = self.stylesOffset - self.stringsOffset

        # FIXME
        if (size % 4) != 0:
            pass

        for i in range(0, int(size / 4)):
            self.m_strings.append(unpack(UNPACK_FORMAT_NATIVE_LONG, buff.read(4))[0])

        if self.stylesOffset != 0:
            size = self.chunkSize - self.stringsOffset

            # FIXME
            if (size % 4) != 0:
                pass

            for i in range(0, size / 4):
                self.m_styles.append(unpack(UNPACK_FORMAT_NATIVE_LONG, buff.read(4))[0])

    def getRaw(self, idx):
        if idx < 0 or self.m_stringOffsets == [] or idx >= len(self.m_stringOffsets):
            return None

        offset = self.m_stringOffsets[idx]
        length = self.getShort(self.m_strings, offset)

        data = ""

        while length > 0:
            offset += 2
            # Unicode character
            # unichr in Python2...
            data += chr(self.getShort(self.m_strings, offset))

            # FIXME
            if data[-1] == "&":
                data = data[:-1]

            length -= 1

        return data

    def getShort(self, array, offset):
        value = array[int(offset / 4)]
        if ((offset % 4) / 2) == 0:
            return value & 0xFFFF
        else:
            return value >> 16
