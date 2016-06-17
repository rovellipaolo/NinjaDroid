from struct import unpack

from lib.axmlparser.AXMLConstants import *
from lib.axmlparser.BuffHandle import BuffHandle
from lib.axmlparser.StringBlock import StringBlock


##
# AXMLParser
#
# @author Anthony Desnos <desnos at t0t0.fr>
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#
# The original AXML parser code comes from Androguard (by Anthony Desnos).
# Link: https://github.com/kzjeef/AxmlParserPY
#
class AXMLParser:
    ##
    # Class constructor.
    #
    # @param raw_buff  The raw buffer of an binary XML file.
    #
    def __init__(self, raw_buff):
        self.reset()
        self.buff = BuffHandle(raw_buff)
        self.buff.read(12)
        self.string_block = StringBlock(self.buff)
        self._resource_ids = []
        self._prefixuri = {}
        self._uriprefix = {}
        self._prefixuril = []

    def reset(self):
        self._event = -1
        self._line_number = -1
        self._name = -1
        self._namespace_uri = -1
        self._attributes = []
        self._id_attribute = -1
        self._class_attribute = -1
        self._style_attribute = -1

    def next(self):
        self.do_next()
        return self._event

    def do_next(self):
        if self._event == END_DOCUMENT:
            return

        event = self._event

        self.reset()

        while 1:
            chunk_type = -1

            # Fake END_DOCUMENT event.
            if event == END_TAG:
                pass

            # START_DOCUMENT
            if event == START_DOCUMENT:
                chunk_type = CHUNK_XML_START_TAG
            else:
                if self.buff.end() == True:
                    self._event = END_DOCUMENT
                    break
                chunk_type = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]

            if chunk_type == CHUNK_RESOURCEIDS:
                chunk_size = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                # FIXME
                if chunk_size < 8 or chunk_size%4 != 0:
                    raise("ooo")

                for i in range(0, int(chunk_size/4-2)):
                    self._resource_ids.append(unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0])

                continue

            # FIXME
            if chunk_type < CHUNK_XML_FIRST or chunk_type > CHUNK_XML_LAST:
                raise("ooo")

            # Fake START_DOCUMENT event.
            if chunk_type == CHUNK_XML_START_TAG and event == -1:
                self._event = START_DOCUMENT
                break

            self.buff.read(4) #/*chunk_size*/
            line_number = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
            self.buff.read(4) #0xFFFFFFFF

            if chunk_type == CHUNK_XML_START_NAMESPACE or chunk_type == CHUNK_XML_END_NAMESPACE:
                if chunk_type == CHUNK_XML_START_NAMESPACE:
                    prefix = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                    uri = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]

                    self._prefixuri[ prefix ] = uri
                    self._uriprefix[ uri ] = prefix
                    self._prefixuril.append((prefix, uri))
                else:
                    self.buff.read(4)
                    self.buff.read(4)
                    (prefix, uri) = self._prefixuril.pop()
                    #del self.m_prefixuri[ prefix ]
                    #del self.m_uriprefix[ uri ]
                continue

            self._line_number = line_number

            if chunk_type == CHUNK_XML_START_TAG:
                self._namespace_uri = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                self._name = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]

                # FIXME
                self.buff.read(4) #flags

                attributeCount = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                self._id_attribute = (attributeCount>>16) - 1
                attributeCount = attributeCount & 0xFFFF
                self._class_attribute = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                self._style_attribute = (self._class_attribute>>16) - 1

                self._class_attribute = (self._class_attribute & 0xFFFF) - 1

                for i in range(0, attributeCount * ATTRIBUTE_LENGTH):
                    self._attributes.append(unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0])

                for i in range(ATTRIBUTE_IX_VALUE_TYPE, len(self._attributes), ATTRIBUTE_LENGTH):
                    self._attributes[i] = (self._attributes[i]>>24)

                self._event = START_TAG
                break

            if chunk_type == CHUNK_XML_END_TAG:
                self._namespace_uri = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                self._name = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]
                self._event = END_TAG
                break

            if chunk_type == CHUNK_XML_TEXT:
                self._name = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, self.buff.read(4))[0]

                # FIXME
                self.buff.read(4) #?
                self.buff.read(4) #?

                self._event = TEXT
                break

    def get_prefix_by_uri(self, uri):
        try:
            return self._uriprefix[ uri ]
        except KeyError:
            return -1

    def get_prefix(self):
        try:
            return self.string_block.get_raw(self._prefixuri[ self._namespace_uri ])
        except KeyError:
            return ""

    def get_name(self):
        if self._name == -1 or (self._event != START_TAG and self._event != END_TAG):
            return ""

        return self.string_block.get_raw(self._name)

    def get_text(self):
        if self._name == -1 or self._event != TEXT:
            return ""

        return self.string_block.get_raw(self._name)

    def get_namespace_prefix(self, pos):
        prefix = self._prefixuril[ pos ][0]
        return self.string_block.get_raw(prefix)

    def get_namespace_uri(self, pos):
        uri = self._prefixuril[ pos ][1]
        return self.string_block.get_raw(uri)

    def get_attribute_offset(self, index):
        # FIXME
        if self._event != START_TAG:
            raise("Current event is not START_TAG.")

        offset = index * 5
        # FIXME
        if offset >= len(self._attributes):
            raise("Invalid attribute index")

        return offset

    def get_attribute_count(self):
        if self._event != START_TAG:
            return -1

        return int(len(self._attributes) / ATTRIBUTE_LENGTH)

    def get_attribute_prefix(self, index):
        offset = self.get_attribute_offset(index)
        uri = self._attributes[offset + ATTRIBUTE_IX_NAMESPACE_URI]

        prefix = self.get_prefix_by_uri(uri)
        if prefix == -1:
            return ""

        return self.string_block.get_raw(prefix)

    def get_attribute_name(self, index):
        offset = self.get_attribute_offset(index)
        name = self._attributes[offset + ATTRIBUTE_IX_NAME]

        if name == -1:
            return ""

        return self.string_block.get_raw(name)

    def get_attribute_value_type(self, index):
        offset = self.get_attribute_offset(index)
        return self._attributes[offset + ATTRIBUTE_IX_VALUE_TYPE]

    def get_attribute_value_data(self, index):
        offset = self.get_attribute_offset(index)
        return self._attributes[offset + ATTRIBUTE_IX_VALUE_DATA]

    def get_attribute_value(self, index):
        offset = self.get_attribute_offset(index)
        value_type = self._attributes[offset + ATTRIBUTE_IX_VALUE_TYPE]
        if value_type == TYPE_STRING:
            value_string = self._attributes[offset + ATTRIBUTE_IX_VALUE_STRING]
            return self.string_block.get_raw(value_string)
        # WIP
        return ""
        #int value_data=_attributes[offset+ATTRIBUTE_IX_VALUE_DATA];
        #return TypedValue.coerceToString(value_type,valueData);
