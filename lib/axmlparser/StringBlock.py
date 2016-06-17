from struct import unpack

from lib.axmlparser.AXMLConstants import *


##
# StringBlock
#
# @author Anthony Desnos <desnos at t0t0.fr>
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#
# The original AXML parser code comes from Androguard (by Anthony Desnos).
# Link: https://github.com/kzjeef/AxmlParserPY
#
class StringBlock:
    def __init__(self, buff):
        self.chunk_size = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0]
        self.string_count = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0]
        self.style_offset_count = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0]

        # unused value ?
        buff.read(4)

        self.strings_offset = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0]
        self.styles_offset = unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0]

        self._string_offsets = []
        self._style_offsets = []
        self._strings = []
        self._styles = []

        for i in range(0, self.string_count):
            self._string_offsets.append(unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0])

        for i in range(0, self.style_offset_count):
            self._style_offsets.append(unpack(UNPACK_FORMAT_LITTLEENDIAN_LONG, buff.read(4))[0])

        size = self.chunk_size - self.strings_offset
        if self.styles_offset != 0:
            size = self.styles_offset - self.strings_offset

        # FIXME
        if (size % 4) != 0:
            pass

        for i in range(0, int(size / 4)):
            self._strings.append(unpack(UNPACK_FORMAT_NATIVE_LONG, buff.read(4))[0])

        if self.styles_offset != 0:
            size = self.chunk_size - self.strings_offset

            # FIXME
            if (size % 4) != 0:
                pass

            for i in range(0, size / 4):
                self._styles.append(unpack(UNPACK_FORMAT_NATIVE_LONG, buff.read(4))[0])

    def get_raw(self, idx):
        if idx < 0 or self._string_offsets == [] or idx >= len(self._string_offsets):
            return None

        offset = self._string_offsets[idx]
        length = self.get_short(self._strings, offset)

        data = ""

        while length > 0:
            offset += 2
            # Unicode character
            # unichr in Python2...
            data += chr(self.get_short(self._strings, offset))

            # FIXME
            if data[-1] == "&":
                data = data[:-1]

            length -= 1

        return data

    def get_short(self, array, offset):
        value = array[int(offset / 4)]
        if ((offset % 4) / 2) == 0:
            return value & 0xFFFF
        else:
            return value >> 16

