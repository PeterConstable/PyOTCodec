from collections import OrderedDict
from enum import Enum
from io import BytesIO
import math
import re
import struct


class OTCodecError(Exception): pass


class otTypeCategory(Enum):
    BASIC = 0 
        # BASIC: a defined sub-class of int (e.g., int8).
        #
        # Characteristics:
        #  - has PACKED_FORMAT and PACKED_SIZE "static" members
        #  - does not have FIELDS, ARRAYS or SUBTABLES members
        #  - has a constructor function that takes unpacked value directly,
        #    and that value is an instance of the base class
        #  - has a tryReadFromBytesIO static method

    BASIC_OT_SPECIAL = 1
        # BASIC_OT_SPECIAL: Tag, Fixed, F2Dot14, uint24. Type is not directly
        # supported by struct module, and so unpacked values require some
        # reinterpretation.
        #
        # Characteristics:
        #  - has a base type str (Tag), float (Fixed, F2Dot24) or int (uint24)
        #  - has PACKED_FORMAT and PACKED_SIZE "static" members
        #  - does not have FIELDS, ARRAYS or SUBTABLES members
        #  - has a constructor function that takes unpacked value directly
        #  - constructor might or might NOT accept the base type
        #  - has a tryReadFromBytesIO static method

    FIXED_LENGTH_BASIC_STRUCT = 2
        # FIXED_LENGTH_BASIC_STRUCT: a struct that has two or more members of BASIC 
        # or BASIC_OT_SPECIAL types. These can be read without requiring recursion.
        #
        # Characteristics:
        #  - has PACKED_FORMAT and PACKED_SIZE "static" members
        #  - has FIELDS static member, an ordered dict: 
        #    - keys are str
        #    - values are BASIC or BASIC_OT_SPECIAL types
        #  - does NOT have ARRAYS or SUBTABLES members
        #  - has constructor that takes arguments as per FIELDs
        #  - constructor does not take unpacked values directly

    FIXED_LENGTH_COMPLEX_STRUCT = 3
        # FIXED_LENGTH_COMPLEX_STRUCT: a struct that has members of BASIC,
        # BASIC_OT_SPECIAL, FIXED_LENGTH_BASIC_STRUCT or FIXED_LENGTH_COMPLEX_STRUCT
        # types. Reading requires recursion to parse the embedded structs.
        #
        # Characteristics:
        #  - has PACKED_FORMAT and PACKED_SIZE "static" members
        #  - has FIELDS static member, an ordered dict:
        #    - keys are str
        #    - values are BASIC, BASIC_OT_SPECIAL, FIXED_LENGTH_BASIC_STRUCT or
        #      FIXED_LENGTH_COMPLEX_STRUCT types
        #  - does NOT have ARRAYS or SUBTABLES members
        #  - has constructor that takes arguments as per FIELDs
        #  - constructor does not take unpacked values directly

    VAR_LENGTH_STRUCT = 4
        # VAR_LENGTH_STRUCT: a struct that has a header with members of the 
        # above types and also has one or more variable-length arrays of 
        # FIXED_LENGTH_BASIC_STRUCT or FIXED_LENGTH_COMPLEX_STRUCT
        # elements (records). The length of each array is either fixed or is
        # indicated in one of the header fields. The offset to the array is
        # either a constant or is indicated in one of the header fields.
        #
        # Characteristics:
        #  - has PACKED_FORMAT and PACKED_SIZE "static" members
        #  - has FIELDS static member
        #  - FIELDS, PACKED_FORMAT, etc. only describe a header that doesn't
        #    include any array
        #  - has an ARRAYS static member describing the arrays
        #  - does NOT have SUBTABLES member
        #  - has an ALL_FIELD_NAMES static member, a list of all field names:
        #    header fields, then array fields
        #  - has constructor that takes positional arguments for members in 
        #    ALL_FIELD_NAMES (header, then arrays)
        #  - constructor does not take unpacked values directly

    VAR_LENGTH_STRUCT_WITH_SUBTABLES = 5
        # VAR_LENGTH_STRUCT_WITH_SUBTABLES: a struct that has a header with
        # members of types BASIC to FIXED_LENGTH_COMPLEX_STRUCT, that may
        # have one or more record arrays (as for VAR_LENGTH_STRUCT), and
        # that has one or more subtables referenced by offsets. The offset
        # is either a constant or is indicated in one of the header fields.
        #
        # Characteristics:
        #  - has PACKED_FORMAT and PACKED_SIZE "static" members
        #    static members that describe header (no arrays or subtables)
        #  - MAY have an ARRAYS static member describing arrays
        #  - has a SUBTABLES static member describing the subtable member
        #  - has an ALL_FIELD_NAMES static member, a list of all field names:
        #    header fields, then array fields, then subtable fields
        #  - has constructor that takes positional arguments for members in 
        #    ALL_FIELD_NAMES (header, then arrays, then subtables)
        #  - constructor does not take unpacked values directly

    VERSIONED_TABLE = 6
        # VERSIONED_TABLE: Table that starts with a version field (or fields) 
        # and that has alternate formats according to the version.
        #
        # Characteristics:
        #  - has FORMATS member that describes the alternate formats.
        #  - does NOT have PACKED_FORMAT, etc. members directly. (These
        #    details are contained, for alternate formats, in the FORMATS
        #    member.


"""
TYPE_CATEGORY: One of the above enum values. This is the first static field 
in a struct class definition.

Note: All BASIC and BASIC_OT_SPECIAL types are defined in this module.

FIELDS: Used in FIXED_LENGTH_BASIC_STRUCT or more-complex types. This is
the second static field in a struct class definition. It is an OrderedDict
with field name / field type as key-value pairs. For example:

    FIELDS = OrderedDict([
        ("field1", uint8),
        ("field2", uint16)
        ])

The fields include all struct members up to but not including any record 
array.

PACKED_FORMAT: This is specified in this module for all basic types — int8 
to uint64, Offset16, etc.; uint24, Fixed, F2Dot14, Tag. For all other types,
these should derived from the FIELDS definition using
getPackedFormatFromFieldsDef(FIELDS). This must follow the FIELDS definition.

PACKED_SIZE: This is always calcuated using struct.calcsize(). Follows after
PACKED_FORMAT.

ARRAYS: This is a list of dicts, each of which has four entries:

  - "field": The field name (str) in the parent table for the array.
  - "type": The struct type (type) for the records in the array.
  - "count": The number of records—either a constant (int) or the name of a header 
     field (str) that holds the count.
  - "offset": The location of the start of the array relative to the parent
     table—either a constant (int) or the name of a header field (str) that has
     the offset. For arrays that immediately follow header fields, use PACKED_SIZE.

Example:

    ARRAYS = [
        {"field": "records", 
         "type": testClassRecord, 
         "count": "numRecs", 
         "offset": "arrayOffset"}
        ]


SUBTABLES: This is a list of dicts, each of which has four entries, as for
arrays: "field", "type", "count", "offset". But note certain differences in
format.

- "type": The value is either a type or is a dict describing alternate subtable
  formats. Formatted subtables always have format as the first field in the struct.
  
  When a dict is used, it has two entries:
  - "formatFieldType": the type of the format field; must be uint8, uint16, uint32
    or FIXED.
  - "subtableFormats": a dict with format values as keys and format types as values.

  For example:

        "type": {
            "formatFieldType": uint16,
            "subtableFormats": {1: testClassFormat1, 2: testClassFormat2}
            }, 

- "count": Must be 1 or else the name of a record field (str). Count is 1 if and 
  only if offset is constant or taken from a header field. Count is the name of a
  header field if and only if offset is obtained from a record field within an 
  array.

- "offset": Either a constant (int), a name of a header field (str), or a
  dict that describes how offsets are obtained from an array. The dict has
  one or two entries.

  - 1 entry: "parentField" is the parent field for an offsets array. The array
    entries are positive integer types, normally Offset16 or Offset32.
  - 2 entries:
    - "parentField": The name of a parent field for an array of records.
    - "recordField": The name of the field within the records for the table offset.

"""

class otVersionType(Enum):
    UINT16_MINOR = 0
    UINT16_MAJOR_MINOR = 1
    UINT32_MINOR = 2
    UINT32_SFNT = 3


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
    required to have a FIELDS member.
    """

    assert hasattr(className, 'TYPE_CATEGORY')
    assert type(className.TYPE_CATEGORY) == otTypeCategory

    # all types must have PACKED_FORMAT, PACKED_SIZE
    if className.TYPE_CATEGORY != otTypeCategory.VERSIONED_TABLE:
        assert hasattr(className, 'PACKED_FORMAT')
        assert (type(className.PACKED_FORMAT) == str and className.PACKED_FORMAT[0] == '>')
        assert hasattr(className, 'PACKED_SIZE')
        assert (type(className.PACKED_SIZE) == int)
        assert (className.PACKED_SIZE == struct.calcsize(className.PACKED_FORMAT))

    if className.TYPE_CATEGORY == otTypeCategory.BASIC:
        assert int in className.__mro__

    if className.TYPE_CATEGORY == otTypeCategory.BASIC_OT_SPECIAL:
        assert (int in className.__mro__
                or str in className.__mro__
                or float in className.__mro__)

    if className.TYPE_CATEGORY in (
            otTypeCategory.BASIC,
            otTypeCategory.BASIC_OT_SPECIAL
            ):
        assert not hasattr(className, 'FIELDS')
        assert hasattr(className, 'tryReadFromBytesIO')
        assert callable(className.tryReadFromBytesIO)

    if className.TYPE_CATEGORY in (
            otTypeCategory.FIXED_LENGTH_BASIC_STRUCT,
            otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT,
            otTypeCategory.VAR_LENGTH_STRUCT,
            otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
            ):
        assert hasattr(className, 'FIELDS')
        assert (type(className.FIELDS) == OrderedDict and len(className.FIELDS) > 0)
        for field in className.FIELDS:
            assert type(field) == str

    if className.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT:
        for type_ in className.FIELDS.values():
            assert type_.TYPE_CATEGORY in (
                otTypeCategory.BASIC, otTypeCategory.BASIC_OT_SPECIAL)

    if className.TYPE_CATEGORY in (
            otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT,
            otTypeCategory.VAR_LENGTH_STRUCT,
            otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
            ):
        for type_ in className.FIELDS.values():
            assert type_.TYPE_CATEGORY in (
                otTypeCategory.BASIC, otTypeCategory.BASIC_OT_SPECIAL,
                otTypeCategory.FIXED_LENGTH_BASIC_STRUCT,
                otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
                )
            assertIsWellDefinedOTType(type_)

    if className.TYPE_CATEGORY in (
            otTypeCategory.BASIC,
            otTypeCategory.BASIC_OT_SPECIAL,
            otTypeCategory.FIXED_LENGTH_BASIC_STRUCT,
            otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
            ):
        assert not hasattr(className, 'ARRAYS')
        assert not hasattr(className, 'SUBTABLES')

    if className.TYPE_CATEGORY in (
            otTypeCategory.VAR_LENGTH_STRUCT,
            ):
        assert hasattr(className, 'ARRAYS')
        assert not hasattr(className, 'SUBTABLES')

    if hasattr(className, 'ARRAYS'):
        assert (type(className.ARRAYS) == list and len(className.ARRAYS) > 0)
        for a in className.ARRAYS:
            assert (type(a) == dict and len(a) == 4)
            assert "field" in a
            assert type(a["field"]) == str
            assert "type" in a
            assert type(a["type"]) == type
            assertIsWellDefinedOTType(a["type"])
            assert "count" in a
            assert isinstance(a["count"], (int, str))
            assert "offset" in a
            assert isinstance(a["offset"], (int, str))
        assert hasattr(className, 'ALL_FIELD_NAMES')
        assert type(className.ALL_FIELD_NAMES) == list
        if hasattr(className, 'SUBTABLES'):
            assert len(className.ALL_FIELD_NAMES) == (
                len(className.FIELDS) + len(className.ARRAYS) + len(className.SUBTABLES)
                )
        else:
            assert len(className.ALL_FIELD_NAMES) == (
                len(className.FIELDS) + len(className.ARRAYS)
                )
    
    if className.TYPE_CATEGORY == otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES:
        assert hasattr(className, 'SUBTABLES')
        assert (type(className.SUBTABLES) == list and len(className.SUBTABLES) > 0)
        for s in className.SUBTABLES:
            assert (type(s) == dict and len(s) == 4)
            assert "field" in s
            assert type(s["field"]) == str
            assert "type" in s
            # Support variant-format subtables
            assert isinstance(s["type"], (type, dict))
            if type(s["type"]) == type:
                assertIsWellDefinedOTType(s["type"])
            else:
                assert len(s["type"]) == 2
                assert "formatFieldType" in s["type"]
                assert s["type"]["formatFieldType"] in (uint8, uint16, uint32, Fixed)
                assert "subtableFormats" in s["type"]
                for k in s["type"]["subtableFormats"].keys():
                    assert type(k) in s["type"]["formatFieldType"].__mro__
                for t in s["type"]["subtableFormats"].values():
                    assertIsWellDefinedOTType(t)
            assert "count" in s
            assert isinstance(s["count"], (int, str))
            assert "offset" in s
            assert isinstance(s["offset"], (int, str, dict))
            if isinstance(s["offset"], (int, str)):
                assert s["count"] == 1
            else:
                assert type(s["count"]) == str and s["count"] in className.FIELDS
                assert len(s["offset"]) in (1, 2)
                assert "parentField" in s["offset"] and type(s["offset"]["parentField"]) == str
                if len(s["offset"]) == 2:
                    assert "recordField" in s["offset"] and type(s["offset"]["recordField"]) == str
        assert hasattr(className, 'ALL_FIELD_NAMES')
        assert type(className.ALL_FIELD_NAMES) == list
        if hasattr(className, 'ARRAYS'):
            assert len(className.ALL_FIELD_NAMES) == (
                len(className.FIELDS) + len(className.ARRAYS) + len(className.SUBTABLES)
                )
        else:
            assert len(className.ALL_FIELD_NAMES) == (
                len(className.FIELDS) + len(className.SUBTABLES)
                )
                    

    pass



def isBasicType(class_):
    if not hasattr(class_, 'TYPE_CATEGORY'):
        return False
    if class_.TYPE_CATEGORY in (otTypeCategory.BASIC, otTypeCategory.BASIC_OT_SPECIAL):
        return True
    else:
        return False



def concatFormatStrings(*args):
    """Combines struct format strings."""
    assert len(args) > 0
    assert type(args[0]) == str
    if args[0][0] in "@=<!":
        raise OTCodecError("Only big-endian format strings are supported.")
    if len(args) == 1:
        return args[0]
    result = args[0]
    for arg in args[1:]:
        assert type(arg) == str
        if arg[0] in "@=<!":
            raise OTCodecError("Only big-endian format strings are supported.")
        if arg[0] == '>':
            result += arg[1:]
        else:
            result += arg
    return result



def _tryReadRawBytes(fileBytesIO:BytesIO, length):
    rawbytes = fileBytesIO.read(length)
    if len(rawbytes) < length:
        raise OTCodecError("Unable to read expected number of bytes from file")
    return rawbytes

def readBasicTypeFromBytesIO(cls, fileBytesIO:BytesIO):
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
        return readBasicTypeFromBytesIO(int8, fileBytes)


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
        return readBasicTypeFromBytesIO(uint8, fileBytes)



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
        return readBasicTypeFromBytesIO(int16, fileBytes)



class FWord(int16):
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return readBasicTypeFromBytesIO(FWord, fileBytes)



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
        return readBasicTypeFromBytesIO(uint16, fileBytes)



class UFWord(uint16):
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return readBasicTypeFromBytesIO(UFWord, fileBytes)



class Offset16(uint16):
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return readBasicTypeFromBytesIO(Offset16, fileBytes)



class int32(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">l"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __new__(cls, val):
        if (val < -(0x8000_0000) or val > 0x7fff_ffff):
            raise ValueError("int32 must be in the range %d to %d" % (-(0x8000_0000), 0x7fff_ffff))
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return readBasicTypeFromBytesIO(int32, fileBytes)



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
        return readBasicTypeFromBytesIO(uint32, fileBytes)



class Offset32(uint32):
    
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return readBasicTypeFromBytesIO(Offset32, fileBytes)



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
        return readBasicTypeFromBytesIO(int64, fileBytes)



class LongDateTime(int64):
    
    def __new__(cls, val):
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return readBasicTypeFromBytesIO(LongDateTime, fileBytes)



class uint64(int):

    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">Q"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __new__(cls, val):
        if (val < 0 or val > 0xffff_ffff_ffff_ffff):
            raise ValueError("uint64 must be in the range %d to %d" % (0, 0xffff_ffff_ffff_ffff))
        return super().__new__(cls, val)

    @staticmethod
    def tryReadFromBytesIO(fileBytes:BytesIO):
        return readBasicTypeFromBytesIO(uint64, fileBytes)




#-------------------------------------------------------------
#  otTypeCategory.BASIC_OT_SPECIAL types
#-------------------------------------------------------------

class uint24(int):

    TYPE_CATEGORY = otTypeCategory.BASIC_OT_SPECIAL
    PACKED_FORMAT = ">3s"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __new__(cls, val):
        """Accepts bytearray, bytes or int (in range 0 to 0xffff_ffff_ffff)."""
        if not isinstance(val, (bytearray, bytes, int)):
            raise TypeError("val argument must be bytearray, bytes or int.")

        if isinstance(val, int):
            if (val < 0 or val > 0xffff_ffff_ffff):
                raise ValueError("uint24 must be in the range %d to %d" % (0, 0xffff_ffff_ffff))
            intval = val
        else:
            if len(val) != cls.PACKED_SIZE:
                raise TypeError("val argument byte sequence must be 3 bytes long.")
            intval = (val[0] << 16) + (val[1] << 8) + val[2]
        return super().__new__(cls, intval)

    @staticmethod
    def tryReadFromBytesIO(fileBytesIO:BytesIO):
        bytes_ = _tryReadRawBytes(fileBytesIO, uint24.PACKED_SIZE)
        return uint24(bytes_)



class Fixed(float):

    TYPE_CATEGORY = otTypeCategory.BASIC_OT_SPECIAL
    PACKED_FORMAT = ">4s"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
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
    PACKED_FORMAT = ">2s"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
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
