from enum import Enum
from io import BytesIO
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
        #  - has PACKED_FORMAT and PACKED_SIZE "static" members
        #  - does not have FIELD_NAMES or FIELD_TYPES members
        #  - does not have a constructor function that takes unpacked value directly
        #  - has a createFromUnpackedValues static method
        #  - returns the interpreted value directly

    BASIC_FIXED_STRUCT = 2
        # BASIC_FIXED_STRUCT: a struct that has two or more members of BASIC, 
        # BASIC_OT_SPECIAL or BASIC_FIXED_STRUCT types. Often but not always
        # used in arrays.
        # Characteristics:
        #   - have PACKED_FORMAT and PACKED_SIZE "static" members
        #   - have FIELD_NAMES or FIELD_TYPES static members
        #   - have a createFromUnpackedValues static method

    BASIC_VARIABLE_STRUCT = 3
        # BASIC_VARIABLE_STRUCT: a struct that has BASIC or BASIC_FIXED_STRUCT 
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



def _readRawBytes(fileBytesIO:BytesIO, length):
        rawbytes = fileBytesIO.read(length)
        if len(rawbytes) < length:
            raise OTCodecError("Unable to read expected number of bytes from file")
        return rawbytes

def _readTypeFromBytesIO(cls, fileBytesIO:BytesIO):
        rawbytes = _readRawBytes(fileBytesIO, cls.PACKED_SIZE)
        val, = struct.unpack(cls.PACKED_FORMAT, rawbytes)
        return cls(val)



class int8(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">b"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < -(0x80) or val > 0x7f):
            raise ValueError("int8 must be in the range %d to %d" % (-(0x80), 0x7f))
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(int8, fileBytes)


class uint8(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">B"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < 0 or val > 0xff):
            raise ValueError("uint8 must be in the range %d to %d" % (0, 0xff))
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(uint8, fileBytes)



class int16(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">h"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < -(0x8000) or val > 0x7fff):
            raise ValueError("int16 must be in the range %d to %d" % (-(0x8000), 0x7fff))
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(int16, fileBytes)



class FWord(int16):
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(FWord, fileBytes)



class uint16(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">H"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < 0 or val > 0xffff):
            raise ValueError("uint16 must be in the range %d to %d" % (0, 0xffff))
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(uint16, fileBytes)



class UFWord(uint16):
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(UFWord, fileBytes)



class Offset16(uint16):
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(Offset16, fileBytes)



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
        return _readTypeFromBytesIO(int32, fileBytes)



class uint32(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">L"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __new__(cls, val):
        if (val < 0 or val > 0xffff_ffff):
            raise ValueError("uint32 must be in the range %d to %d" % (0, 0xffff_ffff))
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(uint32, fileBytes)



class Offset32(uint32):
    
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(Offset32, fileBytes)



class int64(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">q"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < -(0x8000_0000_0000_0000) or val > 0x7fff_ffff_ffff_ffff):
            raise ValueError("int64 must be in the range %d to %d" % (-(0x8000_0000_0000_0000), 0x7fff_ffff_ffff_ffff))
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(int64, fileBytes)



class LongDateTime(int64):
    
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def readFromBytesIO(fileBytes:BytesIO):
        return _readTypeFromBytesIO(LongDateTime, fileBytes)



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
        return _readTypeFromBytesIO(uint64, fileBytes)






class tag:
    pass

