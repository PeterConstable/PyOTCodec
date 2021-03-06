import math
import re
import struct
import itertools
from io import BytesIO



class Tag(str):
    
    _packedFormat = ">4s" # Use this to unpack from file before calling constructor.
    _packedSize = struct.calcsize(_packedFormat)
    _numPackedValues = 1


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
    """Representation of OpenType Fixed type.

    Fixed is described in the OT spec as "32-bit signed fixed-point number (16.16)". 
         
    In practice, prior to OT version 1.8.x, Fixed was used inconsistently as the specified type
    for fields in several tables. In particular, the fractional portion of OT Fixed values
    had been treated in two different ways. 
         
    As defined, the fractional portion should represent fractional units of 1/65536. Fixed is
    used in this way in several tables; for example, in VariationAxisRecords in the 'fvar'
    table, and the italicAngle field in the 'post' table.
         
    But Fixed has also been used for the version field of several tables with the fractional
    portion interpreted as as though the hex value is read as a literal with an implicit ".".
    This has occurred for the 'maxp', 'post' and 'vhea' tables, all of which include a non-
    integer version. For instance, there is a version "0.5" 'maxp' table, and the "Fixed" data
    representation for that is 0x00005000.
    
    (Some Apple-specific tables have only integer versions but are documented as using Fixed
    as the type for the version field.)
         
    (In this alternate usage, Only the first (high-order) nibble of the fractional portion is 
    ever used. Thus, the fractional portion could be shifted right by 12 bits and interpreted 
    as 10ths. When a minor version of the GDEF table -- version 1.2 -- was added in OT 1.6, the 
    value 0x00010002 was used and the type was changed from FIXED to ULONG, apparently in
    recognition of the confusion from prior use of "Fixed" in relation to minor versions.)
         
    Note: This usage in version fields with minor versions has led to some incorrect usage in 
    other non-version fields. For instance, in the fontRevision field of the 'head' table, a 
    value of "5.01" would normally be stored as 0x0005028F (0x28F = 655 decimal, = 65536 / 100).
    However, in some fonts such a fontRevision value would be represented as 0x00050100.
    """

    # Use the following to unpack bytes from a file before calling 
    # interpretUnpackedValues() or createFixedFromUint32().
    _packedFormat = ">L"
    _packedSize = struct.calcsize(_packedFormat)
    _numPackedValues = 1


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
    def createFixedFromUint32(val:int):
        """Takes an integer from 0 to 0xFFFFFFFF and returns a Fixed."""

        if val < 0 or val > 0xFFFF_FFFF:
            raise OTCodecError("The val argument must be between 0 "
                               "and 0xFFFF_FFFF (at most 8 hex digits).")
        bytes_ = struct.pack(">L", val)
        return Fixed(bytes_)


    @staticmethod
    def createFixedFromFloat(val:float):
        """Takes a float between -32,768 and 32,767 and returns a Fixed. 

        Fractional values will be rounded to the nearest 1/65,536. If val is out
        of range (< -32,768 or > 32,767), an exception is raised.
        """
        if val < -32738 or val > 32767:
            raise OTCodecError("The val argument is out of range.")
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
        if isinstance(other, Fixed):
            return self.value == other.value
        elif isinstance(other, (bytearray, bytes)):
            return self._rawBytes == other
        elif isinstance(other, float):
            return self.value == other
        elif isinstance(other, int):
            if other < 0x7FFF_FFFF:
                return self.value == other
            else:
                return self.getFixedAsUint32() == other
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
            raise OTCodecError("The buffer argument must be bytearray or bytes.")
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



class F2Dot14:
    """Representation of OpenType F2Dot14 type.
    
    F2Dot14 is a 16-bit signed number with the low-order 14 bits as fraction.
    """

    # Use the following to unpack bytes from a file before calling 
    # createF2Dot14FromUint16.
    _packedFormat = ">H"
    _packedSize = struct.calcsize(_packedFormat)
    _numPackedValues = 1


    def __init__(self, fixedBytes):
        """Construct an F2Dot14 (fixed 2.14) value from byte sequence.
        
        Length of the byte sequence must be 2 bytes, and must be in
        big-endian order, as would occur in a font file.
        """
        if type(fixedBytes) != bytearray and type(fixedBytes) != bytes:
            raise OTCodecError("The fixedBytes argument must be bytearray or bytes.")
        if len(fixedBytes) != 2:
            raise OTCodecError("The fixedBytes argument must be 2 bytes in length.")
    
        self._rawBytes = bytes(fixedBytes)
        val, = struct.unpack(">h", fixedBytes)
        self.value = val / (1 << 14)
        vals = struct.unpack(">2B", fixedBytes)

        # integer portion
        self.mantissa = vals[0] // 0x40
        if self.mantissa > 1:
            self.mantissa -= 4

        # fraction portion
        self.fraction = (vals[0] & 0x3f) * 256 + vals[1]
        pass


    @staticmethod
    def createF2Dot14FromUint16(val:int):
        """Takes an integer from 0 to 0xFFFF and returns an F2Dot14.

        The integer is interpreted like a big-ending byte sequence representing
        an F2Dot14."""

        if val < 0 or val > 0xFFFF:
            raise OTCodecError("The val argument must be between 0 "
                               "and 65,535 (0xFFFF—at most 4 hex digits).")

        bytes_ = struct.pack(">H", val)
        return F2Dot14(bytes_)


    @staticmethod
    def createF2Dot14FromFloat(val:float):
        """Tables a float between [-2, 2) and returns an F2Dot14.

        Fractional values will be rounded to the nearest 1/2**14 (1/16384ths). 
        If val is out of range, an exception is raised."""

        if val < -2 or val >= 2:
            raise OTCodecError("The val argument is out of range.")

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
        if isinstance(other, F2Dot14):
            return self.value == other.value
        elif isinstance(other, (bytearray, bytes)):
            return self._rawBytes == other
        elif isinstance(other, float):
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
        """Return an F2Dot14 constructed from values in the buffer. Returns
        None if the buffer is the wrong length (not 2 bytes)."""
        if not isinstance(buffer, (bytearray, bytes)):
            raise OTCodecError("The buffer argument must be bytearray or bytes.")
        if len(buffer) != 2:
            return None
        return F2Dot14(buffer)

    @staticmethod
    def tryReadFromFile(fileBytesIO:BytesIO):
        """Returns an F2Dot14 read from the current position in the BytesIO stream.

        An exception may be raised if not enough bytes can be read."""
        from ot_file import ReadRawBytes
        # ReadRawBytes will raise exception if not enough data
        bytes_ = ReadRawBytes(fileBytesIO, 2)
        return F2Dot14(bytes_)

# End of class F2Dot14



class OTCodecError(Exception): pass



# static functions

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



def initializeStruct(object, *args):
    """Initialize objects of arbitrary types.

    The type of the object must be a defined class and
    have tuple class attributes "_fieldNames" and "_fieldTypes".
    The number of args, _fieldNames elements and _fieldTypes
    elements must be the same. The args types must match
    _fieldTypes.
    
    The field members must be single objects. A field
    member can be a list or other container type: it will
    be treated like a single object.
    """
    recordClass = type(object)
    assert len(recordClass._fieldNames) == len(recordClass._fieldTypes)
    assert len(args) == len(recordClass._fieldNames)
    for t, a in zip(recordClass._fieldTypes, args):
        assert type(a) == t
    for f, a in zip(recordClass._fieldNames, args):
        setattr(object, f, a)
# End of initializeStruct



def assertIsWellDefinedStruct(structClass):
    """Asserts a set of requirements used for several classes."""

    assert type(structClass) == type
    assert hasattr(structClass, "_packedFormat") and type(structClass._packedFormat) == str and len(structClass._packedFormat) > 0
    assert hasattr(structClass, "_packedSize") and type(structClass._packedSize) == int
    assert structClass._packedSize == struct.calcsize(structClass._packedFormat)
    assert hasattr(structClass, "_fieldNames") and type(structClass._fieldNames) == tuple and len(structClass._fieldNames) > 0
    for f in structClass._fieldNames:
        assert type(f) == str
    assert hasattr(structClass, "_fieldTypes") and type(structClass._fieldTypes) == tuple and len(structClass._fieldTypes) > 0
    for t in structClass._fieldTypes:
        assert type(t) == type
    assert len(structClass._fieldNames) == len(structClass._fieldTypes)
# End of assertIsWellDefinedStruct



def createNewRecordsArray(recordClass, numRecords):
    """Returns a list of objects of the specified type with default values."""

    assertIsWellDefinedStruct(recordClass)

    assert hasattr(recordClass, "_defaults") and (len(recordClass._defaults) == len(recordClass._fieldNames))
    for v, t in zip(recordClass._defaults, recordClass._fieldTypes):
        assert type(v) == t
    
    return [ recordClass(*recordClass._defaults) for i in range(numRecords)]
# End of createNewRecordsArray



def tryReadRecordsArrayFromBuffer(buffer, recordClass, numRecords, arrayName):
    """Takes a byte sequence and returns a list of objects of the indicated type
    read from the buffer.

    Assumes that the types for the recordClass constructor parameters are all
    basic types supported by struct.unpack() and that exactly match the
    recordClass._packedFormat static attribute. (None of the values returned
    by struct.unpack() require re-interpretation before calling the constructor.
    """

    assertIsWellDefinedStruct(recordClass)

    arrayLength = numRecords * recordClass._packedSize
    if len(buffer) < arrayLength:
        raise OTCodecError(f"The file data is not long enough to read the {arrayName} array.")

    # iter_unpack will return an iterator over the records array, which
    # can then be used in a comprehension
    unpack_iter = struct.iter_unpack(recordClass._packedFormat, buffer[:arrayLength])

    return [
        recordClass(*vals)
        for vals in itertools.islice(unpack_iter, numRecords)
        ]
# End of tryReadRecordsArrayFromBuffer



def tryReadComplexRecordsArrayFromBuffer(
        buffer, recordClass, numRecords, arrayName
        ):
    """Takes a byte sequence and returns a list of record objects of the
    specified type read from the byte sequence.
    
    This is used for records that contain defined structures, not
    just basic binary types supported in struct.unpack(). For records
    comprised only of basic types, use tryReadRecordsArrayFromBuffer.

    The buffer argument is assumed start at the first record and end at the
    end of the array.

    The record class is assumed to have a static interpretUnpackedValues()
    method that takes the raw values returned by struct.unpack() and
    returns a tuple of the higher-level values for the given record type.
    The number of elements in the tuple must be the same as the number
    of field names.
    """

    assertIsWellDefinedStruct(recordClass)

    arrayLength = numRecords * recordClass._packedSize
    if len(buffer) < arrayLength:
        raise OTCodecError(f"The file data is not long enough to read the {arrayName} array.")

    # iter_unpack will return an iterator over the records array
    unpack_iter = struct.iter_unpack(recordClass._packedFormat, buffer[:arrayLength])

    return [
        recordClass(*recordClass.interpretUnpackedValues(*vals))
        for vals in itertools.islice(unpack_iter, numRecords)
        ]
# End of tryReadComplexRecordsArrayFromBuffer



def tryReadSubtablesFromBuffer(buffer, subtableClass, subtableOffsets):
    """Takes a byte sequence and returns a list of objects of the 
    specified subtable type read from the byte sequence.

    The buffer is assumed to be large enough to contain all of the
    subtables, and that all of the subtable offsets are from the
    start of the buffer.
    
    The subtable class is assumed to have a static 'tryReadFromFile'
    method that takes a buffer and returns an object of that class."""

    bufferLength = len(buffer)
    subtables = []

    for offset in subtableOffsets:
        if offset > bufferLength:
            raise OTCodecError(f"Offset to {subtableClass.__name__} table is past the end of the data.")

        assert (type(offset) == int and offset > 0)
        subtables.append(
            subtableClass.tryReadFromFile(buffer[offset:])
            )

    return subtables
# End of tryReadSubtablesFromBuffer



def tryReadMultiFormatSubtablesFromBuffer(buffer, subtableClasses:dict, subtableOffsets:tuple):
    """Takes a byte sequence and returns a list of objects of the
    specified subtable types read from the byte sequence.

    Also returns a list of the subtable formats.

    This is designed for subtables of related types but with
    different formats, with each subtable starting with a uint16
    format field.

    The buffer is assumed to be large enough to contain all of the
    subtables, and that all of the subtable offsets are from the
    start of the buffer.
    
    The subtableClasses parameter expects a dict with the formats
    (integers) as keys and corresponding classes as values. If the
    data includes a subtable with an unsupported format, None will
    be returned in place of that subtable object.

    Each subtable class is assumed to have a static 'tryReadFromFile'
    method that takes a buffer and returns an object of that class.
    """

    assert type(subtableClasses) == dict
    for format in subtableClasses.keys():
        assert type(format) == int
    for class_ in subtableClasses.values():
        assert type(class_) == type
        assert (hasattr(class_, "_fieldNames") and class_._fieldNames[0] == "format")
    assert isinstance(subtableOffsets, (list, tuple))

    bufferLength = len(buffer)
    subtables = []
    formats = []

    for offset in subtableOffsets:
        assert (type(offset) == int and offset >= 0)
        if offset + 2 > bufferLength:
            raise OTCodecError(f"Subtable offset is past the end of the data.")

        # Before reading the subtable, we must peek to determine its format.
        format, = struct.unpack(">H", buffer[offset : offset + 2])
        formats.append(format)
        if format in subtableClasses:
            class_ = subtableClasses[format]
            subtables.append(
                class_.tryReadFromFile(buffer[offset:])
                )
        else:
            subtables.append(None)

    return formats, subtables
# End of tryReadMultiFormatSubtablesFromBuffer
