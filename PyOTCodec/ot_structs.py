from io import BytesIO
from ot_baseTypes import *


def getPackedFormatFromFieldsDefinition(fields:OrderedDict):
    """Takes an OrderedDict that describes the fields for a class
    and returns a packed format string that can be used in
    struct.unpack or struct.pack; and also returns the number
    of packed values.

    Returned tuple: packedFormat, numPackedValues
    """
    packedFormats = []
    numPackedValues = 0
    for t in fields.values():
        packedFormats.append(t.PACKED_FORMAT)
        numPackedValues += t.NUM_PACKED_VALUES
    return concatFormatStrings(*packedFormats), numPackedValues


def tryReadFixedLengthBasicStructFromBuffer(buffer, className):
    """Takes a buffer and returns a struct of the specified type, read from
    the buffer.

    Assumes that the struct starts at the beginning of the buffer. The
    structClass must meet the criteria for FIXED_LENGTH_BASIC_STRUCT 
    structures (otTypeCategory enum): comprised of basic struct types
    without arrays or subtables, and has a createFromUnpackedValues
    """
    try:
       assertIsWellDefinedOTType(className)
    except:
        raise TypeError(f"{className} isn't a well-defined FIXED_LENGTH_BASIC_STRUCT type.")
    if className.TYPE_CATEGORY != otTypeCategory.FIXED_LENGTH_BASIC_STRUCT:
        raise TypeError(f"{className} isn't a FIXED_LENGTH_BASIC_STRUCT type.")

    if len(buffer) < className.PACKED_SIZE:
        raise OTCodecError(f"The buffer is to short to read {className}")

    # Structs that have only BASIC or BASIC_OT_SPECIAL fields are fairly
    # easy since those types have constructors that can accept unpacked 
    # values directly.
    # 
    # But fields that take FIXED_LENGTH_BASIC_STRUCT values are more
    # complex. They can have nested FIXED_LENGTH_BASIC_STRUCT structs,
    # and their constructors don't take unpacked values directly. They
    # require a recursive call to this function.

    fieldValues = []

    categories = [ t.TYPE_CATEGORY for t in className.FIELDS.values()]

    if not otTypeCategory.FIXED_LENGTH_BASIC_STRUCT in categories:
        vals = struct.unpack(className.PACKED_FORMAT, buffer[:className.PACKED_SIZE])
        for val, type_ in zip(vals, className.FIELDS.values()):
            fieldValues.append(type_(val))

    else:
        bufferIO = BytesIO(buffer)

        for field, type_ in className.FIELDS.items():
            if type_.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT:
                fieldBuffer = bufferIO.read(type_.PACKED_SIZE)
                val = tryReadFixedLengthBasicStructFromBuffer(fieldBuffer, type_)
                fieldValues.append(val)
            else:
                fieldValues.append(type_.tryReadFromBytesIO(bufferIO))

    return className(*fieldValues)
