from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from ot_structs import *


testResults = dict({})
skippedTests = []



#-------------------------------------------------------------
# Tests for tryReadFixedLengthStructFromBuffer
#-------------------------------------------------------------

# Want a class conforming to FIXED_LENGTH_BASIC_STRUCT, and then
# test that tryReadFixedLengthStructFromBuffer is able to read
# an instance of that class from a buffer. We should test for each
# different category of type: basic, basic-special, basic-struct.

# arg validations
buffer = b'\x02\x04\xf5\x32\x01\x02'

# not a FIXED_LENGTH_BASIC_STRUCT or FIXED_LENGTH_COMPLEX_STRUCT type
class testClass:
    pass
try:
    x = tryReadFixedLengthStructFromBuffer(buffer, testClass)
except TypeError:
    result = True
else:
    result = False
testResults["structs tryReadFixedLengthStructFromBuffer test 1"] = result

class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
try:
    x = tryReadFixedLengthStructFromBuffer(buffer, testClass)
except TypeError:
    result = True
else:
    result = False
testResults["structs tryReadFixedLengthStructFromBuffer test 2"] = result

# buffer too short
class testClass:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    PACKED_FORMAT = ">Hh"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    NUM_PACKED_VALUES = 2
    FIELDS = OrderedDict([
        ("field1", uint16),
        ("field2", int16)
        ])
    
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

buffer = b'\x02\x04\xf5'
try:
    x = tryReadFixedLengthStructFromBuffer(buffer, testClass)
except OTCodecError:
    result = True
else:
    result = False
testResults["structs tryReadFixedLengthStructFromBuffer test 3"] = result


# structs with BASIC fields

buffer = b'\x02\x04\xf5\x32\x01\x02'

x = tryReadFixedLengthStructFromBuffer(buffer, testClass)
result = type(x) == testClass
# x has expected fields with values of expected types and values
result &= len(vars(x)) == len(testClass.FIELDS)
for field, type_ in testClass.FIELDS.items():
    result &= (field in vars(x))
    result &= (type(getattr(x, field)) == type_)
testResults["structs tryReadFixedLengthStructFromBuffer test 4"] = result

result = (x.field1 == 0x0204 and x.field2 == -2766)
testResults["structs tryReadFixedLengthStructFromBuffer test 5"] = result

class testClass:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    PACKED_FORMAT = ">LqB"
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    NUM_PACKED_VALUES = 3
    FIELDS = OrderedDict([
        ("field1", uint32),
        ("field2", int64),
        ("field3", uint8)
        ])
    
    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

buffer = b'\x02\x04\xf5\x38\xE0\x00\x25\x84\xDE\x1C\x95\xB4\x7e\x01\x02'
x = tryReadFixedLengthStructFromBuffer(buffer, testClass)
result = type(x) == testClass
# x has expected fields with values of expected types and values
result &= len(vars(x)) == len(testClass.FIELDS)
for field, type_ in testClass.FIELDS.items():
    result &= (field in vars(x))
    result &= (type(getattr(x, field)) == type_)
testResults["structs tryReadFixedLengthStructFromBuffer test 6"] = result

result = (x.field1 == 0x0204_f538 and x.field2 == -2305801756621367884 and x.field3 == 126)
testResults["structs tryReadFixedLengthStructFromBuffer test 7"] = result


# structs with BASIC_OT_SPECIAL fields

class testClass:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("field1", Tag),
        ("field2", Fixed),
        ("field3", F2Dot14)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

buffer = b'\x61\x62\x64\x63\xE0\x00\xc0\x00\xf0\x0e'
x = tryReadFixedLengthStructFromBuffer(buffer, testClass)
result = type(x) == testClass
# x has expected fields with values of expected types and values
result &= len(vars(x)) == len(testClass.FIELDS)
for field, type_ in testClass.FIELDS.items():
    result &= (field in vars(x))
    result &= (type(getattr(x, field)) == type_)
testResults["structs tryReadFixedLengthStructFromBuffer test 8"] = result

result = (x.field1 == 'abdc' and x.field2._rawBytes == b'\xE0\x00\xc0\x00' and x.field3._rawBytes == b'\xf0\x0e')
testResults["structs tryReadFixedLengthStructFromBuffer test 9"] = result


# structs with fields that have FIXED_LENGTH_BASIC_STRUCT as values

class testClassChild:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("fieldC1", F2Dot14),
        ("fieldC2", uint16),
        ("fieldC3", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

class testClassParent:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("fieldP1", F2Dot14),
        ("fieldP2", testClassChild),
        ("fieldP3", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

buffer = (b'\x60\x00'
          b'\x70\x00\x01\x01\x01\x02'
          b'\x00\x02')
x = tryReadFixedLengthStructFromBuffer(buffer, testClassParent)
result = type(x) == testClassParent
result &= len(vars(x)) == len(testClassParent.FIELDS)
for field, type_ in testClassParent.FIELDS.items():
    result &= (field in vars(x))
    result &= (type(getattr(x, field)) == type_)
testResults["structs tryReadFixedLengthStructFromBuffer test 10"] = result

result = (x.fieldP1 == 1.5 and x.fieldP3 == 2)
y = x.fieldP2
result &= type(y) == testClassChild
for field, type_ in testClassChild.FIELDS.items():
    result &= (field in vars(y))
    result &= (type(getattr(y, field)) == type_)
result &= (y.fieldC1 == 1.75 and y.fieldC2 == 0x0101 and y.fieldC3 == 0x0102)
testResults["structs tryReadFixedLengthStructFromBuffer test 11"] = result


class testClassGrandParent:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("fieldGP1", uint8),
        ("fieldGP2", testClassParent)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

buffer = (b'\xa0'
            b'\x60\x00'
            b'\x70\x00\x01\x01\x01\x02'
            b'\x00\x02'
          b'\xa1')

x = tryReadFixedLengthStructFromBuffer(buffer, testClassGrandParent)
result = type(x) == testClassGrandParent
result &= len(vars(x)) == len(testClassGrandParent.FIELDS)
for field, type_ in testClassGrandParent.FIELDS.items():
    result &= (field in vars(x))
    result &= (type(getattr(x, field)) == type_)
testResults["structs tryReadFixedLengthStructFromBuffer test 12"] = result

result = (x.fieldGP1 == 0xa0)
y = x.fieldGP2
result = type(y) == testClassParent
result &= len(vars(y)) == len(testClassParent.FIELDS)
for field, type_ in testClassParent.FIELDS.items():
    result &= (field in vars(y))
    result &= (type(getattr(y, field)) == type_)
result &= (y.fieldP1 == 1.5 and y.fieldP3 == 2)
z = y.fieldP2
result &= type(z) == testClassChild
for field, type_ in testClassChild.FIELDS.items():
    result &= (field in vars(z))
    result &= (type(getattr(z, field)) == type_)
result &= (z.fieldC1 == 1.75 and z.fieldC2 == 0x0101 and z.fieldC3 == 0x0102)
testResults["structs tryReadFixedLengthStructFromBuffer test 13"] = result



#-------------------------------------------------------------
# Tests for tryReadVarLengthStructFromBuffer
#-------------------------------------------------------------

# arg validations
buffer = b'\x02\x04\xf5\x32\x01\x02'

# not a FIXED_LENGTH_BASIC_STRUCT, FIXED_LENGTH_COMPLEX_STRUCT 
# or VAR_LENGTH_STRUCT type
class testClass:
    pass
try:
    x = tryReadVarLengthStructFromBuffer(buffer, testClass)
except TypeError:
    result = True
else:
    result = False
testResults["structs tryReadVarLengthStructFromBuffer test 1"] = result


class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
try:
    x = tryReadFixedLengthStructFromBuffer(buffer, testClass)
except TypeError:
    result = True
else:
    result = False
testResults["structs tryReadVarLengthStructFromBuffer test 2"] = result


# buffer too short

class testClassRecord:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("field1", uint8),
        ("field2", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

class testClassTable:
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT
    FIELDS = OrderedDict([
        ("numRecs", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    ARRAYS = [
        {"field": "records", 
         "type": testClassRecord, 
         "count": "numRecs", 
         "offset": PACKED_SIZE}
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

buffer = b'\x00\x03\xa0\x10\x11'
try:
    x = tryReadVarLengthStructFromBuffer(buffer, testClassTable)
except OTCodecError:
    result = True
else:
    result = False
testResults["structs tryReadVarLengthStructFromBuffer test 3"] = result


# records are FIXED_LENGTH_BASIC_STRUCT
# count from header field; offset by value

buffer = (b'\x00\x03'
            b'\xa0\x10\x11'
            b'\xb0\x11\x11'
            b'\xc0\x12\x11'
          b'\xff\xfe')
x = tryReadVarLengthStructFromBuffer(buffer, testClassTable)
result = type(x) == testClassTable
result &= len(vars(x)) == 2
result &= "numRecs" in vars(x) and type(x.numRecs) == uint16 and x.numRecs == 3
result &= "records" in vars(x) and type(x.records) == list and len(x.records) == 3
result &= type(x.records[0]) == testClassRecord
result &= type(x.records[0].field1) == uint8
result &= type(x.records[0].field2) == uint16
result &= (x.records[0].field1 == 0xa0 and x.records[0].field2 == 0x1011)
result &= (x.records[1].field1 == 0xb0 and x.records[1].field2 == 0x1111)
result &= (x.records[2].field1 == 0xc0 and x.records[2].field2 == 0x1211)
testResults["structs tryReadVarLengthStructFromBuffer test 4"] = result


# count by value; offset from header field

class testClassTable:
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT
    FIELDS = OrderedDict([
        ("arrayOffset", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    ARRAYS = [
        {"field": "records", 
         "type": testClassRecord, 
         "count": 3, 
         "offset": "arrayOffset"}
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

buffer = (b'\x00\x05'
          b'\x00\x00\x00'
            b'\xa0\x10\x11'
            b'\xb0\x11\x11'
            b'\xc0\x12\x11'
          b'\xff\xfe')
x = tryReadVarLengthStructFromBuffer(buffer, testClassTable)
result = type(x) == testClassTable
result &= len(vars(x)) == 2
result &= "arrayOffset" in vars(x) and type(x.arrayOffset) == uint16 and x.arrayOffset == 5
result &= "records" in vars(x) and type(x.records) == list and len(x.records) == 3
result &= type(x.records[0]) == testClassRecord
result &= type(x.records[0].field1) == uint8
result &= type(x.records[0].field2) == uint16
result &= (x.records[0].field1 == 0xa0 and x.records[0].field2 == 0x1011)
result &= (x.records[1].field1 == 0xb0 and x.records[1].field2 == 0x1111)
result &= (x.records[2].field1 == 0xc0 and x.records[2].field2 == 0x1211)
testResults["structs tryReadVarLengthStructFromBuffer test 5"] = result



# records are FIXED_LENGTH_COMPLEX_STRUCT
# count from header field; offset by value

class testClassRecChild:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("fieldC1", uint8),
        ("fieldC2", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

class testClassRecord:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("fieldR1", uint8),
        ("fieldR2", testClassRecChild)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

class testClassTable:
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT
    FIELDS = OrderedDict([
        ("numRecs", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    ARRAYS = [
        {"field": "records", 
         "type": testClassRecord, 
         "count": "numRecs", 
         "offset": PACKED_SIZE}
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

buffer = (b'\x00\x03'
            b'\xa0' b'\xe0\x01\x00'
            b'\xa1' b'\xe1\x01\x01'
            b'\xa2' b'\xe2\x01\x02')
x = tryReadVarLengthStructFromBuffer(buffer, testClassTable)
result = type(x) == testClassTable
result &= len(vars(x)) == 2
result &= "numRecs" in vars(x) and type(x.numRecs) == uint16 and x.numRecs == 3
result &= "records" in vars(x) and type(x.records) == list and len(x.records) == 3
result &= type(x.records[0]) == testClassRecord
result &= type(x.records[0].fieldR1) == uint8
result &= type(x.records[0].fieldR2) == testClassRecChild
result &= type(x.records[0].fieldR2.fieldC1) == uint8
result &= type(x.records[0].fieldR2.fieldC2) == uint16
result &= x.records[0].fieldR1 == 0xa0
result &= x.records[1].fieldR1 == 0xa1
result &= x.records[2].fieldR1 == 0xa2
y = x.records[0].fieldR2
result &= y.fieldC1 == 0xe0
result &= y.fieldC2 == 0x0100
y = x.records[1].fieldR2
result &= y.fieldC1 == 0xe1
result &= y.fieldC2 == 0x0101
y = x.records[2].fieldR2
result &= y.fieldC1 == 0xe2
result &= y.fieldC2 == 0x0102
testResults["structs tryReadVarLengthStructFromBuffer test 6"] = result


# count and offset from header fields
class testClassTable:
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT
    FIELDS = OrderedDict([
        ("arrayOffset", uint16),
        ("numRecs", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    ARRAYS = [
        {"field": "records", 
         "type": testClassRecord, 
         "count": "numRecs", 
         "offset": "arrayOffset"}
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

buffer = (b'\x00\x05\x00\x03'
          b'\x00'
            b'\xa0' b'\xe0\x01\x00'
            b'\xa1' b'\xe1\x01\x01'
            b'\xa2' b'\xe2\x01\x02')
x = tryReadVarLengthStructFromBuffer(buffer, testClassTable)
result = type(x) == testClassTable
result &= len(vars(x)) == 3
result &= "arrayOffset" in vars(x) and type(x.arrayOffset) == uint16 and x.arrayOffset == 5
result &= "numRecs" in vars(x) and type(x.numRecs) == uint16 and x.numRecs == 3
result &= "records" in vars(x) and type(x.records) == list and len(x.records) == 3
result &= type(x.records[0]) == testClassRecord
result &= type(x.records[0].fieldR1) == uint8
result &= type(x.records[0].fieldR2) == testClassRecChild
result &= type(x.records[0].fieldR2.fieldC1) == uint8
result &= type(x.records[0].fieldR2.fieldC2) == uint16
result &= x.records[0].fieldR1 == 0xa0
result &= x.records[1].fieldR1 == 0xa1
result &= x.records[2].fieldR1 == 0xa2
y = x.records[0].fieldR2
result &= y.fieldC1 == 0xe0
result &= y.fieldC2 == 0x0100
y = x.records[1].fieldR2
result &= y.fieldC1 == 0xe1
result &= y.fieldC2 == 0x0101
y = x.records[2].fieldR2
result &= y.fieldC1 == 0xe2
result &= y.fieldC2 == 0x0102
testResults["structs tryReadVarLengthStructFromBuffer test 7"] = result


# multiple arrays: one after header and one at offset from header field
class testClassTable:
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT
    FIELDS = OrderedDict([
        ("numRecs1", uint16),
        ("array2Offset", uint16),
        ("numRecs2", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    # intentionally listing arrays out of logical order: the one that's later
    # in the file before the one sequentially after the header (not likely to
    # occur in any OT table spec, but algorithm should have that flexibility)
    ARRAYS = [
        {"field": "records1", 
         "type": testClassRecord, 
         "count": "numRecs1", 
         "offset": "array2Offset"},
        {"field": "records2", 
         "type": testClassRecord, 
         "count": "numRecs2", 
         "offset": PACKED_SIZE}
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

buffer = (b'\x00\x03\x00\x10\x00\x02'
            b'\xa0' b'\xe0\x01\x00'
            b'\xa1' b'\xe1\x01\x01'
          b'\x00\x00'
            b'\xb0' b'\xf0\x02\x00'
            b'\xb1' b'\xf1\x02\x01'
            b'\xb2' b'\xf2\x02\x02'
          )
x = tryReadVarLengthStructFromBuffer(buffer, testClassTable)
result = type(x) == testClassTable
result &= len(vars(x)) == 5
result &= "numRecs1" in vars(x) and type(x.numRecs1) == uint16 and x.numRecs1 == 3
result &= "array2Offset" in vars(x) and type(x.array2Offset) == uint16 and x.array2Offset == 16
result &= "numRecs2" in vars(x) and type(x.numRecs2) == uint16 and x.numRecs2 == 2
result &= "records1" in vars(x) and type(x.records1) == list and len(x.records1) == 3
result &= "records2" in vars(x) and type(x.records2) == list and len(x.records2) == 2
result &= type(x.records1[0]) == testClassRecord
result &= type(x.records1[0].fieldR1) == uint8
result &= type(x.records1[0].fieldR2) == testClassRecChild
result &= type(x.records1[0].fieldR2.fieldC1) == uint8
result &= type(x.records1[0].fieldR2.fieldC2) == uint16
result &= type(x.records2[0]) == testClassRecord

result &= x.records1[0].fieldR1 == 0xb0
result &= x.records1[1].fieldR1 == 0xb1
result &= x.records1[2].fieldR1 == 0xb2
y = x.records1[0].fieldR2
result &= y.fieldC1 == 0xf0
result &= y.fieldC2 == 0x0200
y = x.records1[1].fieldR2
result &= y.fieldC1 == 0xf1
result &= y.fieldC2 == 0x0201
y = x.records1[2].fieldR2
result &= y.fieldC1 == 0xf2
result &= y.fieldC2 == 0x0202

result &= x.records2[0].fieldR1 == 0xa0
result &= x.records2[1].fieldR1 == 0xa1
y = x.records2[0].fieldR2
result &= y.fieldC1 == 0xe0
result &= y.fieldC2 == 0x0100
y = x.records2[1].fieldR2
result &= y.fieldC1 == 0xe1
result &= y.fieldC2 == 0x0101

testResults["structs tryReadVarLengthStructFromBuffer test 8"] = result



# fn can also handle FIXED_LENGTH_COMPLEX_STRUCT

class testClassChild:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("fieldC1", F2Dot14),
        ("fieldC2", uint16),
        ("fieldC3", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

class testClassParent:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("fieldP1", F2Dot14),
        ("fieldP2", testClassChild),
        ("fieldP3", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

buffer = (b'\x60\x00'
          b'\x70\x00\x01\x01\x01\x02'
          b'\x00\x02')
x = tryReadVarLengthStructFromBuffer(buffer, testClassParent)
result = type(x) == testClassParent
result &= len(vars(x)) == 3
result &= "fieldP1" in vars(x) and type(x.fieldP1) == F2Dot14 and x.fieldP1 == 1.5
result &= "fieldP3" in vars(x) and type(x.fieldP3) == uint16 and x.fieldP3 == 2
result &= "fieldP2" in vars(x) and type (x.fieldP2) == testClassChild
y = x.fieldP2
result &= "fieldC1" in vars(y) and type(y.fieldC1) == F2Dot14 and y.fieldC1 == 1.75
result &= "fieldC2" in vars(y) and type(y.fieldC2) == uint16 and y.fieldC2 == 0x0101
result &= "fieldC3" in vars(y) and type(y.fieldC3) == uint16 and y.fieldC3 == 0x0102
testResults["structs tryReadVarLengthStructFromBuffer test 9"] = result



#-------------------------------------------------------------
# Tests for tryReadVarLengthStructWithSubtablesFromBuffer
#-------------------------------------------------------------

# Want to define a class of category VAR_LENGTH_STRUCT_WITH_SUBTABLES
# with data describing one or more member subtables.
#
# In the simple case, this is like having a record array of fixed length
# 1 at an offset indicated in a header field. It will get more involved
# when we add subtables of different formats, or subtable arrays with 
# offsets from a record array.

# arg validations
buffer = b'\x02\x04\xf5\x32\x01\x02'

# not a FIXED_LENGTH_BASIC_STRUCT, FIXED_LENGTH_COMPLEX_STRUCT 
# VAR_LENGTH_STRUCT type or VAR_LENGTH_STRUCT_WITH_SUBTABLES type
class testClass:
    pass
try:
    x = tryReadVarLengthStructWithSubtablesFromBuffer(buffer, testClass)
except TypeError:
    result = True
else:
    result = False
testResults["structs tryReadVarLengthStructWithSubtablesFromBuffer test 1"] = result


class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
try:
    x = tryReadVarLengthStructWithSubtablesFromBuffer(buffer, testClass)
except TypeError:
    result = True
else:
    result = False
testResults["structs tryReadVarLengthStructWithSubtablesFromBuffer test 2"] = result



# good struct definitions, buffer too short

class testClassChild:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("fieldC1", uint8),
        ("fieldC2", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

class testClassParent:
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
    FIELDS = OrderedDict([
        ("fieldP1", uint16),
        ("subtable1Offset", uint16),
        ("subtable2Offset", uint16),
        ("fieldP2", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    SUBTABLES = [
        {"field": "subtable1", 
         "type": testClassChild, 
         "count": 1, 
         "offset": "subtable1Offset"},
        {"field": "subtable2", 
         "type": testClassChild, 
         "count": 1, 
         "offset": "subtable2Offset"}
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, subtables = SUBTABLES)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

buffer = (b'\x0f\x42' b'\x00\x10' b'\x00\x0a' b'\x0f\x43'
          b'\x00\x00')

try:
    x = tryReadVarLengthStructWithSubtablesFromBuffer(buffer, testClassParent)
except OTCodecError:
    result = True
else:
    result = False
testResults["structs tryReadVarLengthStructWithSubtablesFromBuffer test 3"] = result


# good args

# multiple single-count subtable fields, offsets in header, single format; no arrays

buffer = (b'\x0f\x42' b'\x00\x10' b'\x00\x0a' b'\x0f\x43'
          b'\x00\x00'
          b'\xb0\x01\x01'
          b'\x00\x00\x00'
          b'\xb1\x01\x02'
          b'\xf0\xf0'
        )
x = tryReadVarLengthStructWithSubtablesFromBuffer(buffer, testClassParent)
result = type(x) == testClassParent
result &= len(vars(x)) == 6
result &= "fieldP1" in vars(x) and type(x.fieldP1) == uint16 and x.fieldP1 == 0x0f42
result &= "subtable1Offset" in vars(x) and type(x.subtable1Offset) == uint16 and x.subtable1Offset == 16
result &= "subtable2Offset" in vars(x) and type(x.subtable2Offset) == uint16 and x.subtable2Offset == 10
result &= "fieldP2" in vars(x) and type(x.fieldP2) == uint16 and x.fieldP2 == 0x0f43
result &= "subtable1" in vars(x) and type (x.subtable1) == testClassChild
result &= "subtable2" in vars(x) and type (x.subtable1) == testClassChild
y = x.subtable1
result &= y.fieldC1 == 0xb1
result &= y.fieldC2 == 0x0102
y = x.subtable2
result &= y.fieldC1 == 0xb0
result &= y.fieldC2 == 0x0101

testResults["structs tryReadVarLengthStructWithSubtablesFromBuffer test 4"] = result


# similar to previous case, but add a record array after header, and use a constant offset
# multiple single-count subtable fields, offsets in header, single format; no arrays

class testClassParent:
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
    FIELDS = OrderedDict([
        ("fieldP1", uint16),
        ("subtable1Offset", uint16),
        ("fieldP2", uint16),
        ("fieldP3", uint16),
        ("numRecs", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    ARRAYS = [
        {"field": "records", 
         "type": testClassChild, 
         "count": "numRecs", 
         "offset": PACKED_SIZE}
        ]
    SUBTABLES = [
        {"field": "subtable1", 
         "type": testClassChild, 
         "count": 1, 
         "offset": "subtable1Offset"},
        {"field": "subtable2", 
         "type": testClassChild, 
         "count": 1, 
         "offset": 17}
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS, SUBTABLES)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

buffer = (b'\x0f\x42' b'\x00\x17' b'\x00\x10' b'\x0f\x43' b'\x00\x02'
            b'\xc0\x03\x01'
            b'\xc1\x03\x02'
          b'\x00'
          b'\xb0\x01\x01'
          b'\x00\x00\x00'
          b'\xb1\x01\x02'
          b'\xf0\xf0')
x = tryReadVarLengthStructWithSubtablesFromBuffer(buffer, testClassParent)
result = type(x) == testClassParent
result &= len(vars(x)) == 8
result &= "fieldP1" in vars(x) and type(x.fieldP1) == uint16 and x.fieldP1 == 0x0f42
result &= "subtable1Offset" in vars(x) and type(x.subtable1Offset) == uint16 and x.subtable1Offset == 23
result &= "fieldP2" in vars(x) and type(x.fieldP2) == uint16 and x.fieldP2 == 16
result &= "fieldP3" in vars(x) and type(x.fieldP3) == uint16 and x.fieldP3 == 0x0f43
result &= "records" in vars(x) and type(x.records) == list and len(x.records) == 2
result &= "subtable1" in vars(x) and type (x.subtable1) == testClassChild
result &= "subtable2" in vars(x) and type (x.subtable1) == testClassChild

y = x.records[0]
result &= y.fieldC1 == 0xc0
result &= y.fieldC2 == 0x0301
y = x.records[1]
result &= y.fieldC1 == 0xc1
result &= y.fieldC2 == 0x0302

y = x.subtable1
result &= y.fieldC1 == 0xb1
result &= y.fieldC2 == 0x0102
y = x.subtable2
result &= y.fieldC1 == 0xb0
result &= y.fieldC2 == 0x0101

testResults["structs tryReadVarLengthStructWithSubtablesFromBuffer test 5"] = result


# add formatted subtables: assume uint16 format field

class testClassFormat1:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("format", uint16),
        ("fieldC2", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

class testClassFormat2:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("format", uint16),
        ("fieldC2", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

class testClassParent:
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
    FIELDS = OrderedDict([
        ("fieldP1", uint16),
        ("subtable1Offset", uint16),
        ("subtable2Offset", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    SUBTABLES = [
        {"field": "subtable1", 
         "type": {
             "formatFieldType": uint16,
             "subtableFormats": {1: testClassFormat1, 2: testClassFormat2}
             }, 
         "count": 1, 
         "offset": "subtable1Offset"},
        {"field": "subtable2", 
         "type": {
             "formatFieldType": uint16,
             "subtableFormats": {1: testClassFormat1, 2: testClassFormat2}
             }, 
         "count": 1, 
         "offset": "subtable2Offset"}
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, subtables = SUBTABLES)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

buffer = (b'\x0f\x42' b'\x00\x08' b'\x00\x0f'
          b'\x00\x00'
          b'\x00\x02\xf0\x01'
          b'\x00\x00\x00'
          b'\x00\x01\xf0\x02'
          b'\xf0\xf0'
        )
x = tryReadVarLengthStructWithSubtablesFromBuffer(buffer, testClassParent)
result = type(x) == testClassParent
result &= len(vars(x)) == 5
result &= "fieldP1" in vars(x) and type(x.fieldP1) == uint16 and x.fieldP1 == 0x0f42
result &= "subtable1Offset" in vars(x) and type(x.subtable1Offset) == uint16 and x.subtable1Offset == 8
result &= "subtable2Offset" in vars(x) and type(x.subtable2Offset) == uint16 and x.subtable2Offset == 15
result &= "subtable1" in vars(x) and type (x.subtable1) == testClassFormat2
result &= "subtable2" in vars(x) and type (x.subtable2) == testClassFormat1

y = x.subtable1
result &= y.format == 2
result &= y.fieldC2 == 0xf001
y = x.subtable2
result &= y.format == 1
result &= y.fieldC2 == 0xf002

testResults["structs tryReadVarLengthStructWithSubtablesFromBuffer test 6"] = result


# add subtable arrays using offset array

class testClassParent:
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
    FIELDS = OrderedDict([
        ("fieldP1", uint16),
        ("numSubtables", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    ARRAYS = [
        {"field": "subtableOffsets",
         "type": Offset16,
         "count": "numSubtables",
         "offset": PACKED_SIZE}
        ]
    SUBTABLES = [
        {"field": "subtables", 
         "type": testClassChild, 
         "count": "numSubtables", 
         "offset": {"parentField": "subtableOffsets"}
        }
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS, SUBTABLES)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

assertIsWellDefinedOTType(testClassParent)

buffer = (b'\x0f\x42' b'\x00\x03'
            b'\x00\x0c\x00\x12\x00\x15'
          b'\x00\x00'
          b'\x02\xf0\x01'
          b'\x00\x00\x00'
          b'\x01\xf0\x02'
          b'\x03\xf0\x03'
          b'\xf0\xf0'
        )
x = tryReadVarLengthStructWithSubtablesFromBuffer(buffer, testClassParent)
result = type(x) == testClassParent
result &= len(vars(x)) == 4
result &= "fieldP1" in vars(x) and type(x.fieldP1) == uint16 and x.fieldP1 == 0x0f42
result &= "numSubtables" in vars(x) and type(x.numSubtables) == uint16 and x.numSubtables == 3
result &= "subtableOffsets" in vars(x) and type(x.subtableOffsets) == list and len(x.subtableOffsets) == 3
result &= "subtables" in vars(x) and type (x.subtables) == list and len(x.subtables) == 3

result &= x.subtableOffsets == [12, 18, 21]
y = x.subtables[0]
result &= type(y) == testClassChild
result &= y.fieldC1 == 2
result &= y.fieldC2 == 0xf001
y = x.subtables[1]
result &= type(y) == testClassChild
result &= y.fieldC1 == 1
result &= y.fieldC2 == 0xf002
y = x.subtables[2]
result &= type(y) == testClassChild
result &= y.fieldC1 == 3
result &= y.fieldC2 == 0xf003

testResults["structs tryReadVarLengthStructWithSubtablesFromBuffer test 7"] = result


# offset array with format-variant subtables

class testClassParent:
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
    FIELDS = OrderedDict([
        ("fieldP1", uint16),
        ("numSubtables", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    ARRAYS = [
        {"field": "subtableOffsets",
         "type": Offset16,
         "count": "numSubtables",
         "offset": PACKED_SIZE}
        ]
    SUBTABLES = [
        {"field": "subtables", 
         "type": {
             "formatFieldType": uint16,
             "subtableFormats": {1: testClassFormat1, 2: testClassFormat2}
             }, 
         "count": "numSubtables", 
         "offset": {"parentField": "subtableOffsets"}
        }
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS, SUBTABLES)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

assertIsWellDefinedOTType(testClassParent)

buffer = (b'\x0f\x42' b'\x00\x03'
            b'\x00\x0c\x00\x13\x00\x17'
          b'\x00\x00'
          b'\x00\x02\xf0\x01'
          b'\x00\x00\x00'
          b'\x00\x01\xf0\x02'
          b'\x00\x02\xf0\x03'
          b'\xf0\xf0'
        )
x = tryReadVarLengthStructWithSubtablesFromBuffer(buffer, testClassParent)
result = type(x) == testClassParent
result &= len(vars(x)) == 4
result &= "fieldP1" in vars(x) and type(x.fieldP1) == uint16 and x.fieldP1 == 0x0f42
result &= "numSubtables" in vars(x) and type(x.numSubtables) == uint16 and x.numSubtables == 3
result &= "subtableOffsets" in vars(x) and type(x.subtableOffsets) == list and len(x.subtableOffsets) == 3
result &= "subtables" in vars(x) and type (x.subtables) == list and len(x.subtables) == 3

result &= x.subtableOffsets == [12, 19, 23]
y = x.subtables[0]
result &= type(y) == testClassFormat2
result &= y.format == 2
result &= y.fieldC2 == 0xf001
y = x.subtables[1]
result &= type(y) == testClassFormat1
result &= y.format == 1
result &= y.fieldC2 == 0xf002
y = x.subtables[2]
result &= type(y) == testClassFormat2
result &= y.format == 2
result &= y.fieldC2 == 0xf003

testResults["structs tryReadVarLengthStructWithSubtablesFromBuffer test 8"] = result


# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

assert numTestResults == 30

printTestResultSummary("Tests for ot_structs", testResults, skippedTests)
