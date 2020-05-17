import re
import struct
from io import BytesIO



class Tag(str):
    
    # Use __new__, not __init__, so we can modify the value being constructed
    def __new__(cls, tagContent):
        """ Accept bytes, bytearray or string."""

        if isinstance(tagContent, bytes) or isinstance(tagContent, bytearray):
            # take 4 bytes; if less than 4 pad with 0x00
            tmp = tagContent + bytearray([0,0,0,0])
            tmp = tmp[:4]
        elif isinstance(tagContent, str):
            # take 4 characters; if less than 4 pad with spaces
            tmp = tagContent + 4 * "\u0020"
            tmp = tmp[:4]
            # verify only 0x00 to 0xFF by trying to encode as Latin-1
            # this will raise a UnicodeError if any out of range characters
            enc = tmp.encode("Latin-1")
        else:
            raise OTCodecError("Tag can only be constructed from str, bytearray or bytes")

        return super().__new__(cls, cls._decodeIfBytes(tmp))

    @staticmethod
    def _decodeIfBytes(content):
        if isinstance(content, bytearray) or isinstance(content, bytes):
            content = content.decode("Latin-1")
        return content

    def toBytes(self):
        return self.encode("Latin-1")


    # Override __eq__, __ne__ to facilitate correct comparison of str with bytes
    def __ne__(self, other):
        """Compare to tag bytearray, bytes or string"""
        return not self.__eq__(other)

    def __eq__(self, other):
        """Compare to tag bytearray, bytes or string"""
        tmp = self._decodeIfBytes(other)
        return str.__eq__(self, self._decodeIfBytes(other))

    # Implementation of __hash__ is needed so that a Tag can be used as a dict key
    def __hash__(self):
        return str.__hash__(self)

    @staticmethod
    def validateTag(tag):
        """Check if a tag string is a valid OpenType tag. Returns an error code.

        OpenType tags must be 4 characters long. They can only include 
        ASCII 0x20 to 0x7E, and spaces can only be trailing. The sfnt
        version tag 0x0100 is the one exception to these rules, and
        b'\x00\x01\x00\x00' will be accepted. 

        The method returns an error code with flags:
            0x00: valid tag string
            0x01: wrong length
            0x02: out of range characters
            0x04: non-trailing spaces
        """

        if tag == None:
            raise OTCodecError("Invalid argument: None")

        # Recognize exceptional sfntVersion tag:
        if tag == b'\x00\x01\x00\x00':
            return 0

        errors = 0

        # Test against normal rules

        if len(tag) != 4:
            errors += 0x01
        for c in tag:
            if ord(c) < 0x20 or ord(c) > 0x7E:
                errors += 0x02

        # check for non-trailing spaces: remove all spaces and compare with rstrip
        if re.sub(" ", "", tag) != tag.rstrip():
            errors += 0x04
        
        return errors

# End of class Tag


class Fixed:

    def __init__(self, fixedBytes):
        """Construct a 16.16 Fixed value from bytearray or bytes.

        Length of the byte argument must be 4 bytes, and must be in 
        big-endian order, as would occur in a font file.
        """
        if type(fixedBytes) != bytearray and type(fixedBytes) != bytes:
            raise OTCodecError("The fixedBytes argument must be bytearray or bytes.")
        if len(fixedBytes) != 4:
            raise OTCodecError("The fixedBytes argument must be 4 bytes in length.")
        
        self._rawBytes = bytes(fixedBytes)
        val, = struct.unpack(">l", fixedBytes)
        self.value = val / (1 << 16)
        vals = struct.unpack(">hH", fixedBytes)
        self.mantissa, self.fraction = vals


    @staticmethod
    def createNewFixedFromUint32(val:int):
        """Takes an integer from 0 to 0xFFFFFFFF and returns a Fixed."""

        if val < 0 or val > 0xFFFF_FFFF:
            raise OTCodecError("The val argument must be between 0 "
                               "and 0xFFFF_FFFF (at most 8 hex digits).")
        bytes_ = struct.pack(">L", val)
        return Fixed(bytes_)


    def getFixedAsUint32(self):
        val, = struct.unpack(">L", self._rawBytes)
        return val

    @property
    def fixedTableVersion(self):
        return self.mantissa + (self.fraction >> 12) / 10

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if isinstance(other, Fixed):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == other
        else:
            return False

    def __hash__(self):
        return float.__hash__(self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    @staticmethod
    def tryReadFromBuffer(buffer:bytearray):
        """Returns a Fixed constructed from values in the buffer. Returns None 
        if the buffer is the wrong length."""
        if type(buffer) != bytearray and type(buffer) != bytes:
            raise OTCodecError("The fixedBytes argument must be bytearray or bytes.")
        if len(buffer) != 4:
            return None
        return Fixed(buffer)

    @staticmethod
    def tryReadFromFile(fileBytesIO:BytesIO):
        """Returns a Fixed read from the current position in the BytesIO stream.

        An exception may be raised if not enough bytes can be read.
        """
        from ot_file import ReadRawBytes
        # ReadRawBytes will raise exception if not enough data
        bytes_ = ReadRawBytes(fileBytesIO, 4)
        return Fixed(bytes_)

# End of class Fixed



class OTCodecError(Exception): pass
