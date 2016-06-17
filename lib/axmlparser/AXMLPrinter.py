from struct import pack, unpack

from lib.axmlparser.AXMLConstants import *
from lib.axmlparser.AXMLParser import AXMLParser


##
# AXMLPrinter
#
# @author Anthony Desnos <desnos at t0t0.fr>
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#
# The original AXML parser code comes from Androguard (by Anthony Desnos).
# Link: https://github.com/kzjeef/AxmlParserPY
#
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
                self.buff += "<%s%s\n" % (self.__get_prefix(self.axml.get_prefix()), self.axml.get_name())

                # FIXME: use namespace
                if self.xmlns == False:
                    self.buff += "xmlns:%s=\"%s\"\n" % (self.axml.get_namespace_prefix(0),
                                                        self.axml.get_namespace_uri(0))
                    self.xmlns = True

                for i in range(0, self.axml.get_attribute_count()):
                    self.buff += "%s%s=\"%s\"\n" % (self.__get_prefix(self.axml.get_attribute_prefix(i)),
                                                    self.axml.get_attribute_name(i), self.__get_attribute_value(i))

                self.buff += ">\n"
            elif _type == END_TAG:
                self.buff += "</%s%s>\n" % (self.__get_prefix(self.axml.get_prefix()), self.axml.get_name())
            elif _type == TEXT:
                self.buff += "%s\n" % self.axml.get_text()
            elif _type == END_DOCUMENT:
                break

    ##
    # Return the entire XML encoded in UTF-8.
    #
    def get_buff(self):
        return self.buff.encode("utf-8")

    def __get_prefix(self, prefix):
        if prefix == None or len(prefix) == 0:
            return ""

        return prefix + ":"

    def __get_attribute_value(self, index):
        _type = self.axml.get_attribute_value_type(index)
        _data = self.axml.get_attribute_value_data(index)

        #print _type, _data
        if _type == TYPE_STRING:
            return self.axml.get_attribute_value(index)
        elif _type == TYPE_ATTRIBUTE:
            return "?%s%08X" % (self.get_package(_data), _data)
        elif _type == TYPE_REFERENCE:
            return "@%s%08X" % (self.get_package(_data), _data)
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
            return "%f%s" % (self.complex_to_float(_data), DIMENSION_UNITS[_data & COMPLEX_UNIT_MASK])
        elif _type == TYPE_FRACTION:
            return "%f%s" % (self.complex_to_float(_data), FRACTION_UNITS[_data & COMPLEX_UNIT_MASK])
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

    def complex_to_float(self, xcomplex):
        return (float)(xcomplex & 0xFFFFFF00) * RADIX_MULTS[(xcomplex>>4) & 3];

    def get_package(self, id):
        if id >> 24 == 1:
            return "android:"
        return ""
