from enum import Enum
from io import BytesIO
import math
import re
import struct


class OTCodecError(Exception): pass


class otTypeCategory(Enum):
    BASIC = 0 
        # BASIC: a built-in, non-container type -- int, float or str -- 
        # or a sub-class (e.g., int8), or one of the OT types Tag, 
        # Fixed, F2Dot14
        # Characteristics:
        #   - has PACKED_FORMAT and PACKED_SIZE "static" members
        #   - does not have FIELD_NAMES or FIELD_TYPES members
        #   - has a constructor function that takes unpacked value directly
        #   - returns the same value directly

    BASIC_OT_SPECIAL = 1
        # BASIC_OT_SPECIAL: Tag, Fixed, F2Dot14, uint24. Unpacked values
        # require some reinterpretation.
        # Characteristics:
        #  - has PACKED_FORMAT, PACKED_SIZE and NUM_PACKED_VALUES "static" members
        #  - does not have FIELD_NAMES or FIELD_TYPES members
        #  - does not have a constructor function that takes unpacked value directly
        #  - has a base type str (Tag), float (Fixed, F2Dot24) or int (uint24)
        #  - has a constructor that accepts the base type
        #  - has a createFromUnpackedValues static method
        #  - returns the base type directly

    FIXED_LENGTH_BASIC_STRUCT = 2
        # FIXED_LENGTH_BASIC_STRUCT: a struct that has two or more members of BASIC, 
        # BASIC_OT_SPECIAL or BASIC_FIXED_STRUCT types. Often but not always
        # used in arrays.
        # Characteristics:
        #   - have PACKED_FORMAT and PACKED_SIZE "static" members
        #   - have FIELD_NAMES or FIELD_TYPES static members
        #   - have a createFromUnpackedValues static method

    VAR_LENGTH_BASIC_STRUCT = 3
        # VAR_LENGTH_BASIC_STRUCT: a struct that has BASIC or BASIC_FIXED_STRUCT 
        # members and also has one or more variable-length arrays of BASIC or
        # BASIC_FIXED_STRUCT elements (records). The length of each array is 
        # indicated in one of the direct BASIC type members of the struct. The
        # offset is either indicated in one of the members or is a constant.
        # Characteristics:
        #   - have PACKED_FORMAT and PACKED_SIZE "static" members describing 
        #     header fields
        #   - have FIELD_NAMES or FIELD_TYPES static members describing header 
        #     fields
        #   - have an ARRAYS_FORMAT static member describing the arrays.
        #   - have a tryReadFromFile static method


def assertIsWellDefinedOTType(className):
    """Asserts that className is well defined according to its type category.
    
    The otTypeCategory enum establishes a classification of defined types used
    in PyOTCodec for representation of OpenType structures. The className
    class is assumed to have a TYPE_CATEGORY member with an otTypeCategory
    value. That value determines a set of expected characteristics for the
    type: a set of members (and their value types) that is required for that
    category of type in order to work with generic PyOTCodec functions used
    to parse structures.

    For example, a BASIC type must have a PACKED_FORMAT member, but is not
    required to have a FIELD_NAMES member.
    """
    
    assert hasattr(className, 'TYPE_CATEGORY')
    assert type(className.TYPE_CATEGORY) == otTypeCategory

    # all types must have PACKED_FORMAT, PACKED_SIZE
    assert hasattr(className, 'PACKED_FORMAT')
    assert (type(className.PACKED_FORMAT) == str and className.PACKED_FORMAT[0] == '>')
    assert hasattr(className, 'PACKED_SIZE')
    assert (type(className.PACKED_SIZE) == int)
    assert (className.PACKED_SIZE == struct.calcsize(className.PACKED_FORMAT))

    if className.TYPE_CATEGORY == otTypeCategory.BASIC:
        # no additional validations are feasible
        pass
    if className.TYPE_CATEGORY == otTypeCategory.BASIC_OT_SPECIAL:
        assert hasattr(className, 'NUM_PACKED_VALUES')
        assert (type(className.NUM_PACKED_VALUES) == int and className.NUM_PACKED_VALUES > 0)
        assert hasattr(className, 'createFromUnpackedValues')
        assert callable(className.createFromUnpackedValues)
        pass



def _tryReadRawBytes(fileBytesIO:BytesIO, length):
    rawbytes = fileBytesIO.read(length)
    if len(rawbytes) < length:
        raise OTCodecError("Unable to read expected number of bytes from file")
    return rawbytes

def _readBasicTypeFromBytesIO(cls, fileBytesIO:BytesIO):
    """Can be used by any otTypeCategory.BASIC type for sequential
    read from a BytesIO buffer."""
    rawbytes = _tryReadRawBytes(fileBytesIO, cls.PACKED_SIZE)
    val, = struct.unpack(cls.PACKED_FORMAT, rawbytes)
    return cls(val)



#===========================================
#  otTypeCategory.BASIC types
#===========================================

class int8(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">b"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < -(0x80) or val > 0x7f):
            raise ValueError("int8 must be in the range %d to %d" % (-(0x80), 0x7f))
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(int8, fileBytes)


class uint8(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">B"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < 0 or val > 0xff):
            raise ValueError("uint8 must be in the range %d to %d" % (0, 0xff))
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(uint8, fileBytes)



class int16(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">h"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < -(0x8000) or val > 0x7fff):
            raise ValueError("int16 must be in the range %d to %d" % (-(0x8000), 0x7fff))
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(int16, fileBytes)



class FWord(int16):
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(FWord, fileBytes)



class uint16(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">H"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < 0 or val > 0xffff):
            raise ValueError("uint16 must be in the range %d to %d" % (0, 0xffff))
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(uint16, fileBytes)



class UFWord(uint16):
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(UFWord, fileBytes)



class Offset16(uint16):
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(Offset16, fileBytes)



class int32(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">l"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < -(0x8000_0000) or val > 0x7fff_ffff):
            raise ValueError("int32 must be in the range %d to %d" % (-(0x8000_0000), 0x7fff_ffff))
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(int32, fileBytes)



class uint32(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">L"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __new__(cls, val):
        if (val < 0 or val > 0xffff_ffff):
            raise ValueError("uint32 must be in the range %d to %d" % (0, 0xffff_ffff))
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(uint32, fileBytes)



class Offset32(uint32):
    
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(Offset32, fileBytes)



class int64(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">q"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < -(0x8000_0000_0000_0000) or val > 0x7fff_ffff_ffff_ffff):
            raise ValueError("int64 must be in the range %d to %d" % (-(0x8000_0000_0000_0000), 0x7fff_ffff_ffff_ffff))
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(int64, fileBytes)



class LongDateTime(int64):
    
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(LongDateTime, fileBytes)



class uint64(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">Q"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __new__(cls, val):
        if (val < 0 or val > 0xffff_ffff_ffff_ffff):
            raise ValueError("uint64 must be in the range %d to %d" % (0, 0xffff_ffff_ffff_ffff))
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readBasicTypeFromBytesIO(uint64, fileBytes)




#-------------------------------------------------------------
#  otTypeCategory.BASIC_OT_SPECIAL types
#-------------------------------------------------------------

class uint24(int):

    TYPE_CATEGORY = otTypeCategory.BASIC_OT_SPECIAL
    PACKED_FORMAT = ">3B"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    NUM_PACKED_VALUES = 3
    
    def __new__(cls, val):
        if (val < 0 or val > 0xffff_ffff_ffff):
            raise ValueError("uint24 must be in the range %d to %d" % (0, 0xffff_ffff_ffff))
        return super().__new__(cls, val)

    @staticmethod
    def createFromUnpackedValues(*args):
        if len(args) != uint24.NUM_PACKED_VALUES:
            raise TypeError(f"expected number of arguments for createFromUnpackedValues: {uint24.NUM_PACKED_VALUES}")
        for a in args:
            if type(a) != int:
                raise TypeError("createFromUnpackedValues requires int arguments")
            if (a < 0 or a > 255):
                raise ValueError("createFromUnpackedValues arguments must be 0 to 255")
        val = (args[0] << 16) + (args[1] << 8) + args[2]
        return uint24(val)

    @staticmethod
    def tryReadFromBytesIO(fileBytesIO:BytesIO):
        bytes_ = _tryReadRawBytes(fileBytesIO, uint24.PACKED_SIZE)
        vals = struct.unpack(uint24.PACKED_FORMAT, bytes_)
        return uint24.createFromUnpackedValues(*vals)



class Fixed(float):

    TYPE_CATEGORY = otTypeCategory.BASIC_OT_SPECIAL
    PACKED_FORMAT = ">L"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    NUM_PACKED_VALUES = 1
    
    def __new__(cls, bytes_):
        """Accepts bytes or byte array and returns a Fixed."""

        if not isinstance(bytes_, (bytearray, bytes)):
            raise TypeError("The bytes_ argument must be bytearray or bytes.")
        if len(bytes_) != Fixed.PACKED_SIZE:
            raise TypeError("The bytes_ argument must be 4 bytes in length.")

        val, = struct.unpack(">l", bytes_)
        fixed_ = super().__new__(cls, (val / 0x1_0000))
        fixed_._rawBytes = bytes(bytes_)
        vals = struct.unpack(">hH", bytes_)
        fixed_.mantissa, fixed_.fraction = vals

        return fixed_

    @staticmethod
    def createFromUnpackedValues(val:int):
        return Fixed.createFixedFromUint32(val)

    @staticmethod
    def createFixedFromUint32(val:int):
        """Takes an integer from 0 to 0xFFFFFFFF and returns a Fixed."""

        if val < 0 or val > 0xFFFF_FFFF:
            raise ValueError("The val argument must be between 0 "
                               "and 0xFFFF_FFFF (at most 8 hex digits).")
        bytes_ = struct.pack(">L", val)
        return Fixed(bytes_)

    @staticmethod
    def tryReadFromBytesIO(fileBytesIO:BytesIO):
        bytes_ = _tryReadRawBytes(fileBytesIO, Fixed.PACKED_SIZE)
        return Fixed(bytes_)

    @staticmethod
    def createFixedFromFloat(val:float):
        """Takes a float between -32,768 and 32,767 and returns a Fixed. 

        Fractional values will be rounded to the nearest 1/65,536. If val is out
        of range (< -32,768 or > 32,767), an exception is raised.
        """
        if val < -32738 or val > 32767:
            raise ValueError("The val argument is out of range.")
        mant = math.floor(val)
        frac = int(math.fabs(math.modf(val)[0]) * 65536) # num of 1/65536ths
        if mant < 0:
            frac = 65536 - frac
        bytes_ = struct.pack(">hH", mant, frac)
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
        if isinstance(other, (Fixed, float)):
            return super().__eq__(other)
        elif isinstance(other, (bytearray, bytes)):
            return self._rawBytes == other
        elif isinstance(other, int):
            if other < 0x7FFF_FFFF:
                return super().__eq__(other)
            else:
                return self.getFixedAsUint32() == other
        else:
            return False



class F2Dot14(float):

    TYPE_CATEGORY = otTypeCategory.BASIC_OT_SPECIAL
    PACKED_FORMAT = ">H"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    NUM_PACKED_VALUES = 1
    
    def __new__(cls, bytes_):
        """Accepts bytes or byte array and returns an F2Dot14."""

        if not isinstance(bytes_, (bytearray, bytes)):
            raise TypeError("The bytes_ argument must be bytearray or bytes.")
        if len(bytes_) != cls.PACKED_SIZE:
            raise TypeError("The bytes_ argument must be {cls.PACKED_SIZE} bytes in length.")

        val, = struct.unpack(">h", bytes_)
        f2dot14 = super().__new__(cls, (val / (1 << 14)))
        f2dot14._rawBytes = bytes(bytes_)

        vals = struct.unpack(">2B", bytes_)
        # integer portion
        f2dot14.mantissa = vals[0] // 0x40
        if f2dot14.mantissa > 1:
            f2dot14.mantissa -= 4
        # fraction portion
        f2dot14.fraction = (vals[0] & 0x3f) * 256 + vals[1]

        return f2dot14

    @staticmethod
    def createFromUnpackedValues(val:int):
        return F2Dot14.createF2Dot14FromUint16(val)

    @staticmethod
    def createF2Dot14FromUint16(val:int):
        """Takes an integer from 0 to 0xFFFF and returns an F2Dot14.

        The integer is interpreted like a big-ending byte sequence representing
        an F2Dot14."""

        if val < 0 or val > 0xFFFF:
            raise ValueError("The val argument must be between 0 "
                               "and 65,535 (0xFFFF—at most 4 hex digits).")

        bytes_ = struct.pack(">H", val)
        return F2Dot14(bytes_)

    @staticmethod
    def tryReadFromBytesIO(fileBytesIO:BytesIO):
        bytes_ = _tryReadRawBytes(fileBytesIO, F2Dot14.PACKED_SIZE)
        return F2Dot14(bytes_)

    @staticmethod
    def createF2Dot14FromFloat(val:float):
        """Tables a float between [-2, 2) and returns an F2Dot14.

        Fractional values will be rounded to the nearest 1/2**14 (1/16384ths). 
        If val is out of range, an exception is raised.
        """

        if val < -2 or val >= 2:
            raise ValueError("The val argument is out of range.")

        mant = math.floor(val)
        frac = int(math.modf(val)[0] * 2 ** 14)
        if frac < 0:
            frac = 2 ** 14 + frac
        frac = int(math.fabs(math.modf(val)[0]) * 2 ** 14) # num of 1/16384ths
        if mant < 0:
            frac = 16384 - frac
        bytes_ = struct.pack(">h", mant * 2**14 + frac)
        return F2Dot14(bytes_)

    def getF2Dot14AsUint16(self):
        val, = struct.unpack(">H", self._rawBytes)
        return val

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if isinstance(other, (F2Dot14, float)):
            return super().__eq__(other)
        elif isinstance(other, (bytearray, bytes)):
            return self._rawBytes == other
        else:
            return False



class Tag(str):

    TYPE_CATEGORY = otTypeCategory.BASIC_OT_SPECIAL
    PACKED_FORMAT = ">4s"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    NUM_PACKED_VALUES = 1
    
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
            # verify only 0x00 to 0xFF by trying to encode as ASCII
            # this will raise a UnicodeError if any out of range characters
        else:
            raise TypeError("Tag can only be constructed from str, bytearray or bytes.")

        try:
            tag, bytes_ = cls._getTagAndBytes(tmp)
        except UnicodeEncodeError:
            raise ValueError("Tag can only have ASCII characters (byte values < 128).")
        tag = super().__new__(cls, tag)
        tag._rawBytes = bytes_

        return tag

    @staticmethod
    def _getTagAndBytes(content):
        if isinstance(content, (bytearray, bytes)):
            bytes_ = content
            tag = content.decode("ascii")
        else:
            tag = content
            bytes_ = content.encode("ascii")
        return tag, bytes_

    @staticmethod
    def createFromUnpackedValues(val):
        # more stringent validation than in constructor
        if not isinstance(val, (bytearray, bytes)) or len(val) != 4:
            raise TypeError('The val argument must be bytearray or bytes with length of four.')
        return Tag(val)

    @staticmethod
    def tryReadFromBytesIO(fileBytesIO:BytesIO):
        bytes_ = _tryReadRawBytes(fileBytesIO, Tag.PACKED_SIZE)
        return Tag(bytes_)

    def toBytes(self):
        return self._rawBytes

    def __ne__(self, other):
        """Compare to tag bytearray, bytes or string"""
        return not self.__eq__(other)

    def __eq__(self, other):
        """Compare to tag bytearray, bytes or string"""
        if isinstance(other, Tag):
            return self._rawBytes == other._rawBytes
        elif isinstance(other, (bytearray, bytes)):
            return self._rawBytes == other
        elif isinstance(other, str):
            return super().__eq__(other)
        else:
            return False

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
            raise TypeError("Invalid argument: None")

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
