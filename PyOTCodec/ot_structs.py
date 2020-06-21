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



def getCombinedFieldNames(fields:OrderedDict, arrays:list = None, subtables: list = None):
    """Takes a FIELDS definition and an ARRAYS definition and returns
    a list of the combined field names.

    The result list has names from FIELDS first, then names from ARRAYS.
    """
    fieldNames = list(fields)
    arrayNames = []
    if not arrays is None:
        arrayNames = [a["field"] for a in arrays]
    subtableNames = []
    if not subtables is None:
        subtableNames = [s["field"] for s in subtables]
    return fieldNames + arrayNames + subtableNames



def tryReadFixedLengthStructFieldsFromBuffer(buffer, className):
    """Takes a buffer and returns an OrderedDict of field name/value pairs.

    Assumed that the struct starts at the beginning of the buffer.
    
    Also assumed that caller has verified that className is type category
    FIXED_LENGTH_BASIC_STRUCT structures or FIXED_LENGTH_COMPLEX_STRUCT.
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

    Assumed that the struct starts at the beginning of the buffer.
    
    className must be one of the type categories FIXED_LENGTH_BASIC_STRUCT
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

    recordClass must be of type category FIXED_LENGTH_BASIC_STRUCT or
    FIXED_LENGTH_COMPLEX_STRUCT.
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



def tryReadStructArrayFieldsFromBuffer(buffer, className, headerFields):
    """Takes a buffer and returns an OrderedDict of field name/value pairs
    where the values are arrays.

    Assumed that the parent struct starts at the beginning of the buffer.

    Also assumed that caller has verified that className is type category
    VAR_LENGTH_STRUCT or VAR_LENGTH_STRUCT_WITH_SUBTABLES, with
    descriptions of the arrays given in className.ARRAYS.

    Returns an OrderedDict with each element having a field name as key,
    and a value that is a list of objects, with name and object type as
    indicated in the ARRAYS description.
    """

    arrayFields = OrderedDict([])

    for array in className.ARRAYS:
        # determine count: either a number or a header field name
        if type(array["count"]) == str:
            count = headerFields[array["count"]]
        else:
            count = array["count"]
        # determine offset: either a number or a header field name
        if type(array["offset"]) == str:
            offset = headerFields[array["offset"]]
        else:
            offset = array["offset"]

        arrayFields[array["field"]] = tryReadFixedLengthRecordsArrayFromBuffer(
            buffer[offset:],
            array["type"],
            count,
            array["field"]
            )

    return arrayFields
# End of tryReadStructArrayFieldsFromBuffer



def tryReadVarLengthStructFromBuffer(buffer, className):
    """Takes a buffer and returns a struct of the specified type, read from
    the buffer.

    Assumed that the struct starts at the beginning of the buffer.
    
    className must be one of the type categories VAR_LENGTH_STRUCT,
    FIXED_LENGTH_COMPLEX_STRUCT or FIXED_LENGTH_BASIC_STRUCT.
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
        arrayFields = tryReadStructArrayFieldsFromBuffer(buffer, className, allFields)
        allFields.update(arrayFields)
        
    return className(*allFields.values())
# End of tryReadVarLengthStructFromBuffer



def tryReadSubtableFieldsFromBuffer(buffer, className, headerFields):
    """Takes a buffer and returns an OrderedDict of field name/value pairs
    where the values are subtables.

    The buffer and className arguments are for the parent struct. Assumed
    that the parent struct starts at the beginning of the buffer.

    Also assumed that caller has verified that className is type category
    VAR_LENGTH_STRUCT_WITH_SUBTABLES, with descriptions of the subtables
    given in className.SUBTABLES.

    The headerFields argument must include any record array fields in the 
    parent table as well as the header fields proper.

    Returns an OrderedDict with each element having a field name as key,
    and a value that is an object, with name and object type as
    indicated in the SUBTABLES description.
    """

    subtableFields = OrderedDict([])

    for subtable in className.SUBTABLES:
        # determine count: either a number or a header field name
        if type(subtable["count"]) == str:
            count = headerFields[subtable["count"]]
        else:
            count = subtable["count"]
        # determine offset: either a number or a header field name
        if type(subtable["offset"]) == str:
            offset = headerFields[subtable["offset"]]
        else:
            offset = subtable["offset"]

        subtableFields[subtable["field"]] = tryReadStructWithSubtablesFromBuffer(
            buffer[offset:],
            subtable["type"]
            )

    return subtableFields
# End of tryReadSubtableFieldsFromBuffer



def tryReadStructWithSubtablesFromBuffer(buffer, className):
    """Takes a buffer and returns a struct of the specified type, read from
    the buffer.

    Assumed that the struct starts at the beginning of the buffer.

    Also assumed that caller has verified that className is one of type
    categories VAR_LENGTH_STRUCT_WITH_SUBTABLES, VAR_LENGTH_STRUCT, 
    FIXED_LENGTH_COMPLEX_STRUCT or FIXED_LENGTH_BASIC_STRUCT.
    """
    # start with header
    allFields = tryReadFixedLengthStructFieldsFromBuffer(buffer, className)

    # get any arrays
    if hasattr(className, 'ARRAYS'):
        arrayFields = tryReadStructArrayFieldsFromBuffer(buffer, className, allFields)
        allFields.update(arrayFields)

    # get any subtables
    if hasattr(className, 'SUBTABLES'):
        subtableFields = tryReadSubtableFieldsFromBuffer(
            buffer,
            className,
            allFields
            )
        allFields.update(subtableFields)

    return className(*allFields.values())
# End of tryReadVarLengthStructWithSubtablesFieldsFromBuffer



def tryReadVarLengthStructWithSubtablesFromBuffer(buffer, className):
    """Takes a buffer and returns a struct of the specified type, read from
    the buffer.

    Assumes that the struct starts at the beginning of the buffer.
    
    className must be one of the type categories
    VAR_LENGTH_STRUCT_WITH_SUBTABLES, VAR_LENGTH_STRUCT, 
    FIXED_LENGTH_COMPLEX_STRUCT or FIXED_LENGTH_BASIC_STRUCT.
    """
    try:
       assertIsWellDefinedOTType(className)
    except:
        raise TypeError(f"{className} isn't a well-defined type for purposes of declarative parsing.")
    if not className.TYPE_CATEGORY in (
            otTypeCategory.FIXED_LENGTH_BASIC_STRUCT,
            otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT,
            otTypeCategory.VAR_LENGTH_STRUCT,
            otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES):
        raise TypeError(f"{className} isn't a fixed- or variable-length struct type.")

    return tryReadStructWithSubtablesFromBuffer(buffer, className)
# End of tryReadVarLengthStructWithSubtablesFromBuffer