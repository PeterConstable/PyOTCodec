import math
import re
import struct
import itertools
from io import BytesIO
from ot_structs import *


# static functions


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
