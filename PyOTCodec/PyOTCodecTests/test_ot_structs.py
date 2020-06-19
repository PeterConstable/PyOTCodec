from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from ot_structs import *


testResults = dict({})
skippedTests = []



#-------------------------------------------------------------
# Tests for tryReadFixedLengthBasicStructFromBuffer
#-------------------------------------------------------------

# Want a class conforming to FIXED_LENGTH_BASIC_STRUCT, and then
# test that tryReadFixedLengthBasicStructFromBuffer is able to read
# an instance of that class from a buffer. We should test for each
# different category of type: basic, basic-special, basic-struct.

# arg validations
buffer = b'\x02\x04\xf5\x32\x01\x02'
class testClass:
    pass
try:
    x = tryReadFixedLengthBasicStructFromBuffer(buffer, testClass)
except TypeError:
    result = True
else:
    result = False
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 1"] = result

class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
try:
    x = tryReadFixedLengthBasicStructFromBuffer(buffer, testClass)
except TypeError:
    result = True
else:
    result = False
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 2"] = result


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
    x = tryReadFixedLengthBasicStructFromBuffer(buffer, testClass)
except OTCodecError:
    result = True
else:
    result = False
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 3"] = result


# structs with BASIC fields

buffer = b'\x02\x04\xf5\x32\x01\x02'

x = tryReadFixedLengthBasicStructFromBuffer(buffer, testClass)
result = type(x) == testClass
# x has expected fields with values of expected types and values
result &= len(vars(x)) == len(testClass.FIELDS)
for field, type_ in testClass.FIELDS.items():
    result &= (field in vars(x))
    result &= (type(getattr(x, field)) == type_)
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 4"] = result

result = (x.field1 == 0x0204 and x.field2 == -2766)
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 5"] = result

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
x = tryReadFixedLengthBasicStructFromBuffer(buffer, testClass)
result = type(x) == testClass
# x has expected fields with values of expected types and values
result &= len(vars(x)) == len(testClass.FIELDS)
for field, type_ in testClass.FIELDS.items():
    result &= (field in vars(x))
    result &= (type(getattr(x, field)) == type_)
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 6"] = result

result = (x.field1 == 0x0204_f538 and x.field2 == -2305801756621367884 and x.field3 == 126)
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 7"] = result


# structs with BASIC_OT_SPECIAL fields

class testClass:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("field1", Tag),
        ("field2", Fixed),
        ("field3", F2Dot14)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDefinition(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

buffer = b'\x61\x62\x64\x63\xE0\x00\xc0\x00\xf0\x0e'
x = tryReadFixedLengthBasicStructFromBuffer(buffer, testClass)
result = type(x) == testClass
# x has expected fields with values of expected types and values
result &= len(vars(x)) == len(testClass.FIELDS)
for field, type_ in testClass.FIELDS.items():
    result &= (field in vars(x))
    result &= (type(getattr(x, field)) == type_)
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 8"] = result

result = (x.field1 == 'abdc' and x.field2._rawBytes == b'\xE0\x00\xc0\x00' and x.field3._rawBytes == b'\xf0\x0e')
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 9"] = result


# structs with fields that have FIXED_LENGTH_BASIC_STRUCT as values

class testClassChild:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("fieldC1", F2Dot14),
        ("fieldC2", uint16),
        ("fieldC3", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDefinition(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

class testClassParent:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("fieldP1", F2Dot14),
        ("fieldP2", testClassChild),
        ("fieldP3", uint16)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDefinition(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

buffer = (b'\x60\x00'
          b'\x70\x00\x01\x01\x01\x02'
          b'\x00\x02')
x = tryReadFixedLengthBasicStructFromBuffer(buffer, testClassParent)
result = type(x) == testClassParent
result &= len(vars(x)) == len(testClassParent.FIELDS)
for field, type_ in testClassParent.FIELDS.items():
    result &= (field in vars(x))
    result &= (type(getattr(x, field)) == type_)
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 10"] = result

result = (x.fieldP1 == 1.5 and x.fieldP3 == 2)
y = x.fieldP2
result &= type(y) == testClassChild
for field, type_ in testClassChild.FIELDS.items():
    result &= (field in vars(y))
    result &= (type(getattr(y, field)) == type_)
result &= (y.fieldC1 == 1.75 and y.fieldC2 == 0x0101 and y.fieldC3 == 0x0102)
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 11"] = result


class testClassGrandParent:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("fieldGP1", uint8),
        ("fieldGP2", testClassParent)
        ])
    PACKED_FORMAT, NUM_PACKED_VALUES = getPackedFormatFromFieldsDefinition(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)

    def __init__(self, *args):
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

buffer = (b'\xa0'
            b'\x60\x00'
            b'\x70\x00\x01\x01\x01\x02'
            b'\x00\x02'
          b'\xa1')

x = tryReadFixedLengthBasicStructFromBuffer(buffer, testClassGrandParent)
result = type(x) == testClassGrandParent
result &= len(vars(x)) == len(testClassGrandParent.FIELDS)
for field, type_ in testClassGrandParent.FIELDS.items():
    result &= (field in vars(x))
    result &= (type(getattr(x, field)) == type_)
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 12"] = result

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
testResults["structs tryReadFixedLengthBasicStructFromBuffer test 13"] = result



# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

assert numTestResults == 13

printTestResultSummary("Tests for ot_structs", testResults, skippedTests)
