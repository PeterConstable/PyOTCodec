from io import BytesIO
import itertools
from ot_baseTypes import *


class structBaseClass:
    """Base class for structs of type categories
    FIXED_LENGTH_BASIC_STRUCT and higher.

    Every subclass must have a FIELDS attribute and also get
    PACKED_FORMAT and PACKED_SIZE attributes with values derived
    from FIELDS.
    """
    def __init_subclass__(cls):
        # This will be called _after_ subclass definitions have
        # been processed.
        super().__init_subclass__()
        cls.PACKED_FORMAT = getPackedFormatFromFieldsDef(cls.FIELDS)
        cls.PACKED_SIZE = struct.calcsize(cls.PACKED_FORMAT)
        arrays = None; subtables = None
        if hasattr(cls, 'ARRAYS'):
            arrays = cls.ARRAYS
        if hasattr(cls, 'SUBTABLES'):
            subtables = cls.SUBTABLES
        cls.ALL_FIELD_NAMES = getCombinedFieldNames(cls.FIELDS, arrays, subtables)

    def __init__(self, *args):
        init_setattributes(self, *args)


def getPackedFormatFromFieldsDef(fields:OrderedDict):
    """Takes an OrderedDict that describes the fields for a class
    and returns a packed format string that can be used in
    struct.unpack or struct.pack; and also returns the number
    of packed values.
    """
    packedFormats = []
    for t in fields.values():
        packedFormats.append(t.PACKED_FORMAT)
    return concatFormatStrings(*packedFormats)


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


def getCombinedFieldTypes(obj):
    """Takes a object and returns a list of types for all of the fields
    in that struct.

    The object must have a type category FIXED_LENGTH_BASIC_STRUCT or more complex.

    The list of types will be in order with header fields followed by array fields,
    then fields for subtables or subtable arrays.
    """
    assert hasattr(obj, 'TYPE_CATEGORY')
    assert not obj.TYPE_CATEGORY in (otTypeCategory.BASIC, otTypeCategory.BASIC_OT_SPECIAL)
    
    types = []
    for t in obj.FIELDS.values():
        types.append(t)
    if hasattr(obj, 'ARRAYS'):
        for a in obj.ARRAYS:
            types.append(list)
    if hasattr(obj, 'SUBTABLES'):
        for x in obj.SUBTABLES:
            if x["count"] == 1:
                types.append(x["type"])
            else:
                types.append(list)
    return types


def validateArgs(obj, *args):
    """Takes an object of a defined type plus arguments passed to its 
    constructor and validates that the correct number and types of arguments
    were passed.

    Returns True or False
    """
    types = getCombinedFieldTypes(obj)
    if len(types) != len(args):
        return False
    for a, t in zip(args, types):
        if type(a) != t:
            return False
    return True


def init_setattributes(obj, *args):
    """Takes an object of a defined type plus argument passed to its
    constructor, validates the args and then sets the attributes.
    """
    if not validateArgs(obj, *args):
        raise TypeError(f"Wrong arguments were passed to the {type(obj)} constructor.")
    if hasattr(obj, 'ALL_FIELD_NAMES'):
        fields = obj.ALL_FIELD_NAMES
    else:
        fields = obj.FIELDS
    for f, a in zip(fields, args):
        setattr(obj, f, a)



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
    assert className.TYPE_CATEGORY in (
            otTypeCategory.FIXED_LENGTH_BASIC_STRUCT,
            otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT)
    assertIsWellDefinedOTType(className)

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
    assert recordClass.TYPE_CATEGORY in (
            otTypeCategory.FIXED_LENGTH_BASIC_STRUCT,
            otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT)
    assertIsWellDefinedOTType(recordClass)

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



def tryReadArrayFieldsFromBuffer(buffer, className, headerFields):
    """Takes a buffer and returns an OrderedDict of field name/value pairs
    where the values are arrays as defined in className.ARRAYS.

    Assumed that the parent struct starts at the beginning of the buffer.

    Also assumed that caller has verified that className is type category
    VAR_LENGTH_STRUCT or VAR_LENGTH_STRUCT_WITH_SUBTABLES.

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
        else: # int
            offset = array["offset"]

        # check if the type of array elements is a basic type or struct
        if isBasicType(array["type"]):
            # get the values directly
            arrayLength = count * array["type"].PACKED_SIZE
            if len(buffer) < offset + arrayLength:
                raise OTCodecError(f'Unable to read the {array["field"]} array in {className}: buffer is not long enough.')
            unpack_iter = struct.iter_unpack(array["type"].PACKED_FORMAT, buffer[offset : offset + arrayLength])
            arrayFields[array["field"]] = [array["type"](v)
                for v, in itertools.islice(unpack_iter, count)]
            
        else:
            arrayFields[array["field"]] = tryReadFixedLengthRecordsArrayFromBuffer(
                buffer[offset:],
                array["type"],
                count,
                array["field"]
                )

    return arrayFields
# End of tryReadStructArrayFieldsFromBuffer



# USED ONLY FOR TESTING
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
        arrayFields = tryReadArrayFieldsFromBuffer(buffer, className, allFields)
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
        # NOTE: count will only be relevant if offset comes from
        # a records array
        if type(subtable["count"]) == str:
            count = headerFields[subtable["count"]]
        else:
            count = subtable["count"]
        
        # determine offset: either a number or a header field name
        if type(subtable["offset"]) == str:
            offset = headerFields[subtable["offset"]]
            assert count == 1
        elif type(subtable["offset"]) == int:
            offset = subtable["offset"]
            assert count == 1
        else: # dict
            # offset is dict with one or 2 elements
            # will need to get the offsets within a loop
            offsetArrayField = subtable["offset"]["parentField"]
            if len(subtable["offset"]) > 1:
                offsetRecordField = subtable["offset"]["recordField"]

        # determine subtable type -- may be variant formats
        # subtable["type"] is either a type or a dict; if a dict,
        # then there are multiple subtable formats that start with
        # a format field
        if type(subtable["type"]) == type:
            subtableType = subtable["type"]
        else:
            # alternate subtable formats -- need to determine
            # the type for each within a loop
            formatFieldType = subtable["type"]["formatFieldType"]
            subtableFormats = subtable["type"]["subtableFormats"]

        subtableArray = []
        for i in range(count):
            # get the offset
            if type(subtable["offset"]) == dict:
                if len(subtable["offset"]) == 1:
                    offset = headerFields[offsetArrayField][i]
                else:
                    offset = getattr(headerFields[offsetArrayField][i], offsetRecordField)
            else:
                # already got the single offset earlier
                pass

            # get the type
            if type(subtable["type"]) == dict:
                # read the format at offset
                bufferIO = BytesIO(buffer[offset:])
                subtableFormat = formatFieldType.tryReadFromBytesIO(bufferIO)
                subtableType = subtableFormats[subtableFormat]
            else:
                # already got the single type earlier
                pass

            subtableArray.append(
                tryReadStructWithSubtablesFromBuffer(
                    buffer[offset:],
                    subtableType
                    )
                )

        if type(subtable["count"]) == int and subtable["count"] == 1:
            subtableFields[subtable["field"]] = subtableArray[0]
        else:
            subtableFields[subtable["field"]] = subtableArray

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
        arrayFields = tryReadArrayFieldsFromBuffer(buffer, className, allFields)
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



def tryReadVersionedTableFromBuffer(buffer, className):
    """Takes a buffer and returns a table of the specified type, read from
    the buffer.

    Assumes that the table starts at the beginning of the buffer.

    className must be of type category VERSIONED_TABLE.
    """

    if not className.TYPE_CATEGORY in (otTypeCategory.VERSIONED_TABLE,):
        raise TypeError(f"{className} isn't a versioned table.")
    try:
        assertIsWellDefinedOTType(className)
    except:
        raise TypeError(f"{className} isn't a well-defined versioned table.")

    # get the version field value(s) according to the type
    versionType = className.FORMATS["versionType"]
    if versionType == otVersionType.UINT16_MINOR:
        versionFormat = ">H"
    elif versionType == otVersionType.UINT16_MAJOR_MINOR:
        versionFormat = ">2H"
    elif versionType == otVersionType.UINT32_MINOR:
        versionFormat = ">L"
    else: # UINT32_SFNT
        versionFormat = "4s"
    versionVals = struct.unpack(versionFormat, buffer[:struct.calcsize(versionFormat)])

    # From here, want to resolve the appropriate format data from what's available.
    if versionType == otVersionType.UINT32_SFNT:
        version == versionVals[0]
    elif versionType in (otVersionType.UINT16_MINOR, otVersionType.UINT32_MINOR):
        # take the max available that's less than or equal to the value read
        eligibleFormatVersions = [x for x in className.FORMATS["versions"] if x <= versionVals[0]]
        if len(eligibleFormatVersions) == 0:
            raise OTCodecError(f"The table version in the data, {versionVals[0]}, is not supported. "
                              f"The minimum version supported is {min(className.FORMATS['versions'])}.")
        version = max(eligibleFormatVersions)
        format = className.FORMATS["versions"][version]
    else: # UINT16_MAJOR_MINOR
        # ??
        pass

    # got the format; apply to the class
    for k, v in format.items():
        setattr(className, k, v)

    # now we can read like a non-versioned table
    return tryReadStructWithSubtablesFromBuffer(buffer, className)

# End of tryReadVersionedTableFromBuffer