from io import BytesIO
import itertools
from ot_baseTypes import *


def getPackedFormatFromFieldsDef(fields:OrderedDict):
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



def getCombinedFieldNames(fields:OrderedDict, arrays:list):
    """Takes a FIELDS definition and an ARRAYS definition and returns
    a list of the combined field names.

    The result list has names from FIELDS first, then names from ARRAYS.
    """
    fieldNames = list(fields)
    arrayNames = [a["field"] for a in arrays]
    return fieldNames + arrayNames



def tryReadFixedLengthStructFieldsFromBuffer(buffer, className):
    """Takes a buffer and returns an OrderedDict of field name/value pairs.

    Assumes that the struct starts at the beginning of the buffer.
    
    Also assume that caller has verified that className meets criteria for
    FIXED_LENGTH_BASIC_STRUCT structures, and 
    """
    if len(buffer) < className.PACKED_SIZE:
        raise OTCodecError(f"The buffer is to short to read {className} header.")

    allFields = OrderedDict([])

    # FIXED_LENGTH_BASIC_STRUCT structs have only BASIC or BASIC_OT_SPECIAL 
    # fields. Those types have constructors that can accept unpacked values
    # directly.
    # 
    # FIXED_LENGTH_COMPLEX_STRUCT structs have fields that take other nested
    # FIXED_LENGTH_COMPLEX_STRUCT or FIXED_LENGTH_BASIC_STRUCT structs as values.
    # These require a recursive call to this function, passing the portion of the
    # buffer for that struct. So for the parent struct we need to process the 
    # buffer sequentially.

    if className.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT:
        vals = struct.unpack(className.PACKED_FORMAT, buffer[:className.PACKED_SIZE])
        for val, field, type_ in zip(vals, className.FIELDS.keys(), className.FIELDS.values()):
            fieldValue = type_(val)
            allFields[field] = fieldValue
    else:
        bufferIO = BytesIO(buffer)
        for field, type_ in className.FIELDS.items():
            if (type_.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
                or type_.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT):
                fieldBuffer = bufferIO.read(type_.PACKED_SIZE)
                fieldValue = tryReadFixedLengthStructFromBuffer(fieldBuffer, type_)
            else:
                fieldValue = type_.tryReadFromBytesIO(bufferIO)
            allFields[field] = fieldValue

    return allFields
# End of tryReadFixedLengthStructFieldsFromBuffer



def tryReadFixedLengthStructFromBuffer(buffer, className):
    """Takes a buffer and returns a struct of the specified type, read from
    the buffer.

    Assumes that the struct starts at the beginning of the buffer.
    
    Also assumes className meets the criteria for FIXED_LENGTH_BASIC_STRUCT 
    or FIXED_LENGTH_COMPLEX_STRUCT.
    """
    try:
       assertIsWellDefinedOTType(className)
    except:
        raise TypeError(f"{className} isn't a well-defined fixed-length struct type.")
    if not className.TYPE_CATEGORY in (
            otTypeCategory.FIXED_LENGTH_BASIC_STRUCT,
            otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT):
        raise TypeError(f"{className} isn't a fixed-length struct type.")

    if len(buffer) < className.PACKED_SIZE:
        raise OTCodecError(f"The buffer is to short to read {className}.")

    allFields = tryReadFixedLengthStructFieldsFromBuffer(buffer, className)

    return className(*allFields.values())
# End of tryReadFixedLengthStructFromBuffer



def tryReadFixedLengthRecordsArrayFromBuffer(buffer, recordClass, numRecords, arrayName):
    """Takes a buffer and returns a list of objects of the indicated type read
    from the buffer.

    Assumes that the records array starts at the beginning of the buffer.

    Also assumes that recordClass meets the criteria for FIXED_LENGTH_BASIC_STRUCT.
    """
    try:
        assertIsWellDefinedOTType(recordClass)
    except:
        raise TypeError(f"{recordClass} isn't a well-defined fixed-length struct type.")
    if not recordClass.TYPE_CATEGORY in (
            otTypeCategory.FIXED_LENGTH_BASIC_STRUCT,
            otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT):
        raise TypeError(f"{recordClass} isn't a fixed-length struct type.")

    arrayLength = numRecords * recordClass.PACKED_SIZE
    if len(buffer) < arrayLength:
        raise OTCodecError(f"The buffer is not long enough to read the {arrayName} array.")

    bufferIO = BytesIO(buffer)
    records = []
    for i in range(numRecords):
        recordBuffer = bufferIO.read(recordClass.PACKED_SIZE)
        records.append(tryReadFixedLengthStructFromBuffer(recordBuffer, recordClass))

    return records
# End of tryReadFixedBasicRecordsArrayFromBuffer



def tryReadVarLengthBasicStructFromBuffer(buffer, className):
    """Takes a buffer and returns a struct of the specified type, read from
    the buffer.

    Assumes that the struct starts at the beginning of the buffer. The
    structClass must meet the criteria for VAR_LENGTH_STRUCT 
    structures (otTypeCategory enums): comprised of basic struct types
    described by FIELDS, and has one or more arrays described by ARRAYS.
    """
    try:
       assertIsWellDefinedOTType(className)
    except:
        raise TypeError(f"{className} isn't a well-defined type for purposes of declarative parsing.")
    if not className.TYPE_CATEGORY in (
            otTypeCategory.FIXED_LENGTH_BASIC_STRUCT,
            otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT,
            otTypeCategory.VAR_LENGTH_STRUCT):
        raise TypeError(f"{className} isn't a fixed- or variable-length struct type.")

    # start with header
    allFields = tryReadFixedLengthStructFieldsFromBuffer(buffer, className)

    # finished with headers; now process arrays
    if className.TYPE_CATEGORY == otTypeCategory.VAR_LENGTH_STRUCT:
        for array in className.ARRAYS:
            # determine count: either a number or a header field name
            if type(array["count"]) == str:
                count = allFields[array["count"]]
            else:
                count = array["count"]
            # determine location: if "offset" is a str, then a header field name for
            # offset; else "offset" has offset directly;
            # 
            if type(array["offset"]) == str:
                offset = allFields[array["offset"]]
            else:
                offset = array["offset"]
            allFields[array["field"]] = tryReadFixedLengthRecordsArrayFromBuffer(
                buffer[offset:],
                array["type"],
                count,
                array["field"]
                )
        
    return className(*allFields.values())
