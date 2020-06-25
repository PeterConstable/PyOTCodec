from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from ot_file import *


testResults = dict({})
skippedTests = []




testBytes1 = ( b'\x02\x0F\x37\xDC\x9A'
               b'\xA2\x0F'
               b'\xE7\xDC'
               b'\x9A\x02'
               b'\xBF\x27\xDC\x9A'
               b'\xB2\x0F\x37\xDC'
               b'\x9A\x02\x0F\x37\xDC\x9A\x27\xDC'
               b'\x27\xDC\x9A\xB2\x0F\x37\xDC\x9A'
               b'\xB2'
               )



#-------------------------------------------------------------
# Tests for ot_types static functions
#-------------------------------------------------------------

# tests for ot_types.assertIsWellDefinedStruct

# arg not a class
try:
    x = assertIsWellDefinedStruct(42)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 1"] = result

# class missing "_packedFormat" string
class test_Class:
    _packedSize = 0
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 2"] = result

class test_Class:
    _packedFormat = 0
    _packedSize = 0
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 3"] = result

# class missing "_packedSize" int
class test_Class:
    _packedFormat = ">H"
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 4"] = result

class test_Class:
    _packedFormat = ">H"
    _packedSize = "abc"
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 5"] = result

# _packedSize doesn't match _packedFormat
class test_Class:
    _packedFormat = ">H"
    _packedSize = 4
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 6"] = result

# class missing "_fieldNames" tuple
class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldTypes = (int, float)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 7"] = result

class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = "test1, test2"
    _fieldTypes = (int, float)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 8"] = result

class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", 42)
    _fieldTypes = (int, float)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 9"] = result

# class missing "_fieldTypes" tuple
class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 10"] = result

class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1",)
    _fieldTypes = int
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 11"] = result

class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, 42)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 12"] = result

# count mis-match between _fieldNames, _fieldTypes 
class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int,)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = True
else:
    result = False
testResults["assertIsWellDefinedStruct test 13"] = result

# good class definition
class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, int)
try:
    x = assertIsWellDefinedStruct(test_Class)
except:
    result = False
else:
    result = True
testResults["assertIsWellDefinedStruct test 14"] = result


# tests for createNewRecordsArray
numRecs = 5

# class missing "_defaults"
class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)

    def __init__(self, *args):
        pass

try:
    x = createNewRecordsArray(test_Class, numRecs)
except:
    result = True
else:
    result = False
testResults["createNewRecordsArray test 1"] = result

# count mis-match between _defaults, _fieldTypes
class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
    _defaults = (0, 0, 0)

    def __init__(self, *args):
        pass

try:
    x = createNewRecordsArray(test_Class, numRecs)
except:
    result = True
else:
    result = False
testResults["createNewRecordsArray test 2"] = result

# mis-match between defaults, types
class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
    _defaults = (2.0, 4.0)

    def __init__(self, *args):
        pass

try:
    x = createNewRecordsArray(test_Class, numRecs)
except:
    result = True
else:
    result = False
testResults["createNewRecordsArray test 3"] = result

# missing __init__()
class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
    _defaults = (2, 4.0)
try:
    x = createNewRecordsArray(test_Class, numRecs)
except:
    result = True
else:
    result = False
testResults["createNewRecordsArray test 4"] = result

# __init__() with wrong arg count
class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
    _defaults = (2, 4.0)

    def __init__(self, args):
        pass

try:
    x = createNewRecordsArray(test_Class, numRecs)
except:
    result = True
else:
    result = False
testResults["createNewRecordsArray test 5"] = result

# good class def'n
class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
    _defaults = (2, 4.0)

    def __init__(self, arg1, arg2):
        pass

try:
    x = createNewRecordsArray(test_Class, numRecs)
except:
    result = False
else:
    result = True
testResults["createNewRecordsArray test 6"] = result

class test_Class:
    _packedFormat = ">H"
    _packedSize = 2
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, float)
    _defaults = (2, 4.0)

    def __init__(self, *args):
        for f, a in zip(test_Class._fieldNames, args):
            setattr(self, f, a)

x = createNewRecordsArray(test_Class, numRecs)
result = (type(x) == list and len(x) == numRecs)
testResults["createNewRecordsArray test 7"] = result
result = (type(x[0]) == test_Class and list(vars(x[0])) == list(test_Class._fieldNames))
testResults["createNewRecordsArray test 8"] = result
result = (type(x[0].test1) == test_Class._fieldTypes[0] and type(x[0].test2) == test_Class._fieldTypes[1])
result &= (x[0].test1 == 2 and x[0].test2 == 4.0)
testResults["createNewRecordsArray test 9"] = result


# tests for tryReadRecordsArrayFromBuffer

class test_Class:
    _packedFormat = ">hL"
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, int)

    def __init__(self, *args):
        self.test1, self.test2 = args

numRecs = 5
arrayName = "testArray"

# insufficient buffer size
buffer = b'\x40\x00\x40'

try:
    x = tryReadRecordsArrayFromBuffer(buffer, test_Class, numRecs, arrayName)
except OTCodecError:
    result = True
else:
    result = False
testResults["tryReadRecordsArrayFromBuffer test 1"] = result

# good buffer
buffer = b'\x40\x00\x40\x72\x00\x00\x80\x56\x00\x72\x00\x00\x40\x00\x40\x72\x00\x00\xfc\x09\x73\x72\x00\x00\x40\x00\x40\x72\x00\x00\x72\x8c\x85\x72\x32\x50'
x = tryReadRecordsArrayFromBuffer(buffer, test_Class, numRecs, arrayName)
result = (type(x) == list and len(x) == numRecs and type(x[0]) == test_Class)
testResults["tryReadRecordsArrayFromBuffer test 2"] = result
result = (x[0].test1 == 0x4000 and x[0].test2 == 0x4072_0000)
result &= (x[3].test1 == -1015 and x[3].test2 == 0x7372_0000)
testResults["tryReadRecordsArrayFromBuffer test 3"] = result



# tests for tryReadComplexRecordsArrayFromBuffer

class test_Class:
    _packedFormat = ">h3H"
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("test1", "test2")
    _fieldTypes = (int, Fixed)

    def __init__(self, *args):
        for f, a in zip(test_Class._fieldNames, args):
            setattr(self, f, a)

    @staticmethod
    def interpretUnpackedValues(*args):
        # will receive ">hHHH"; reinterpret as (int32, Fixed)
        x, = struct.unpack(">l", struct.pack(">hH", *args[:2]))
        y = Fixed.createFixedFromUint32((args[2] << 16) + args[3])
        return x, y

numRecs = 3
arrayName = "testArray"

# buffer too short
buffer = b'\x40\x00\x40\x72\x00\x00\x80\x56'
try:
    x = tryReadComplexRecordsArrayFromBuffer(buffer, test_Class, numRecs, arrayName)
except OTCodecError:
    result = True
else:
    result = False
testResults["tryReadComplexRecordsArrayFromBuffer test 1"] = result

# buffer good
buffer = b'\x40\x00\x40\x72\x00\x00\x80\x56\xC0\x00\x40\x32\xC0\x00\x40\x32\x40\x00\x40\x72\x00\x00\x80\x56\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
x = tryReadComplexRecordsArrayFromBuffer(buffer, test_Class, numRecs, arrayName)
result = (type(x) == list and len(x) == 3 and type(x[0]) == test_Class)
testResults["tryReadComplexRecordsArrayFromBuffer test 2"] = result

fields = list(vars(x[0]))
result = (len(fields) == len(test_Class._fieldNames) and fields == list(test_Class._fieldNames))
testResults["tryReadComplexRecordsArrayFromBuffer test 3"] = result

result = (x[0].test1 == 0x40004072 and type(x[0].test2) == Fixed and x[0].test2._rawBytes == b'\x00\x00\x80\x56')
testResults["tryReadComplexRecordsArrayFromBuffer test 4"] = result
result = (x[1].test1 == -1073725390 and x[1].test2._rawBytes == b'\xC0\x00\x40\x32')
testResults["tryReadComplexRecordsArrayFromBuffer test 5"] = result


# tests for tryReadSubtablesFromBuffer

class test_Class:
    _format = ">hH"
    _size = struct.calcsize(_format)
    _fields = ("field1", "field2")

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    @staticmethod
    def tryReadFromFile(fileBytes):
        vals = struct.unpack(test_Class._format, fileBytes[:test_Class._size])
        return test_Class(*vals)

buffer = b'\x40\x00\x40\x72\x00\x00\x80\x56'
offsets = (20,)
try:
    x = tryReadSubtablesFromBuffer(buffer, test_Class, offsets)
except OTCodecError:
    result = True
else:
    result = False
testResults["tryReadSubtablesFromBuffer test 1"] = result

buffer = b'\x40\x00\x40\x72\x00\x00\x80\x56\xC0\x00\x40\x32\xC0\x00\x40\x32\x40\x00\x40\x72\x00\x00\x80\x56\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
offsets = (2, 8, 14)
x = tryReadSubtablesFromBuffer(buffer, test_Class, offsets)
results = (type(x) == list and len(x) == 3 and type(x[0]) == test_Class)
results &= (list(x[0].__dict__) == list(test_Class._fields))
testResults["tryReadSubtablesFromBuffer test 2"] = result

results = (x[0].field1 == 0x4072 and x[0].field2 == 0)
results &= (x[1].field1 == -16384 and x[1].field2 == 0x4032)
results &= (x[2].field1 == 0x4032 and x[2].field2 == 0x4000)
testResults["tryReadSubtablesFromBuffer test 3"] = result


# tests for tryReadMultiFormatSubtablesFromBuffer

# arg validations:

buffer = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
subtableOffsets = (2, 4)

# 2nd arg not dict
try:
    x = tryReadMultiFormatSubtablesFromBuffer(buffer, 42, subtableOffsets)
except:
    result = True
else:
    result = False
testResults["tryReadMultiFormatSubtablesFromBuffer test 1"] = result

# 2nd arg is dict, but with non-int key
class test_Class:
    _packedFormat = ">HL"
    _packedSize = 6

    @staticmethod
    def tryReadFromFile(fileBytes):
        pass

try:
    x = tryReadMultiFormatSubtablesFromBuffer(buffer, {1.0:test_Class}, subtableOffsets)
except:
    result = True
else:
    result = False
testResults["tryReadMultiFormatSubtablesFromBuffer test 2"] = result


# 2nd arg is dict, but not of classes
try:
    x = tryReadMultiFormatSubtablesFromBuffer(buffer, {1:42}, subtableOffsets)
except:
    result = True
else:
    result = False
testResults["tryReadMultiFormatSubtablesFromBuffer test 3"] = result

# class without _fieldNames
class test_Class:
    _packedFormat = ">HL"
    _packedSize = 6

    @staticmethod
    def tryReadFromFile(fileBytes):
        pass

try:
    x = tryReadMultiFormatSubtablesFromBuffer(buffer, {1:test_Class}, subtableOffsets)
except:
    result = True
else:
    result = False
testResults["tryReadMultiFormatSubtablesFromBuffer test 4"] = result

# first name in _fieldNames not "format"
class test_Class:
    _packedFormat = ">HL"
    _packedSize = 6
    _fieldNames = ("format_x", "test1")

    @staticmethod
    def tryReadFromFile(fileBytes):
        pass

try:
    x = tryReadMultiFormatSubtablesFromBuffer(buffer, {1:test_Class}, subtableOffsets)
except:
    result = True
else:
    result = False
testResults["tryReadMultiFormatSubtablesFromBuffer test 5"] = result

# subtableOffsets not list or tuple
class test_Class:
    _packedFormat = ">HL"
    _packedSize = 6
    _fieldNames = ("format", "test1")

    @staticmethod
    def tryReadFromFile(fileBytes):
        pass

try:
    x = tryReadMultiFormatSubtablesFromBuffer(buffer, {1:test_Class}, 2)
except:
    result = True
else:
    result = False
testResults["tryReadMultiFormatSubtablesFromBuffer test 6"] = result

# subtable offset not int >= 0
subtableOffsets = (5.5, )
try:
    x = tryReadMultiFormatSubtablesFromBuffer(buffer, {1:test_Class}, subtableOffsets)
except:
    result = True
else:
    result = False
testResults["tryReadMultiFormatSubtablesFromBuffer test 7"] = result

subtableOffsets = (-2, )
try:
    x = tryReadMultiFormatSubtablesFromBuffer(buffer, {1:test_Class}, subtableOffsets)
except:
    result = True
else:
    result = False
testResults["tryReadMultiFormatSubtablesFromBuffer test 8"] = result

# buffer too short to read format
buffer = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
subtableOffsets = (8, )
try:
    x = tryReadMultiFormatSubtablesFromBuffer(buffer, {1:test_Class}, subtableOffsets)
except OTCodecError:
    result = True
else:
    result = False
testResults["tryReadMultiFormatSubtablesFromBuffer test 9"] = result

# bad class: missing tryReadFromFile method
class test_Class:
    _packedFormat = ">HL"
    _packedSize = 6
    _fieldNames = ("format", "test1")

buffer = b'\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00'
subtableOffsets = (6, )
try:
    x = tryReadMultiFormatSubtablesFromBuffer(buffer, {1:test_Class}, subtableOffsets)
except:
    result = True
else:
    result = False
testResults["tryReadMultiFormatSubtablesFromBuffer test 10"] = result

# returns tuple of two lists (formats, subtables)
buffer = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
subtableOffsets = (6, )
x = tryReadMultiFormatSubtablesFromBuffer(buffer, {1:test_Class}, subtableOffsets)
result = (type(x) == tuple and len(x) == 2 and type(x[0]) == list and type(x[1]) == list)
testResults["tryReadMultiFormatSubtablesFromBuffer test 11"] = result

# for format not in subtableClasses, format list includes format, but subtable list has None
buffer = b'\x00\x00\x00\x00\x00\x00\x01\x03\x00\x00\x00'
subtableOffsets = (6, )
x, y = tryReadMultiFormatSubtablesFromBuffer(buffer, {1:test_Class}, subtableOffsets)
result = (type(x[0]) == int and x[0] == 259 and y[0] == None)
testResults["tryReadMultiFormatSubtablesFromBuffer test 12"] = result

# distinct formats: expected types with expected values
class test_Class1:
    _packedFormat = ">HH"
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("format", "test1")

    def __init__(self, *args):
        for f, a in zip(test_Class1._fieldNames, args):
            setattr(self, f, a)
        assert self.format == 1

    @staticmethod
    def tryReadFromFile(fileBytes):
        vals = struct.unpack(test_Class1._packedFormat, fileBytes[:test_Class1._packedSize])
        return test_Class1(*vals)

class test_Class2:
    _packedFormat = ">3H"
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("format", "test1", "test2")

    def __init__(self, *args):
        for f, a in zip(test_Class2._fieldNames, args):
            setattr(self, f, a)
        assert self.format == 2

    @staticmethod
    def tryReadFromFile(fileBytes):
        vals = struct.unpack(test_Class2._packedFormat, fileBytes[:test_Class2._packedSize])
        return test_Class2(*vals)

buffer = b'\x00\x00\x00\x02\x04\x32\x00\x01\xCC\x00\x01\x05\x07\xCC\xCC\x00\x01\x60\x98\xf0\xf1\xf2'
# st 0: \x00\x02\x04\x32\x00\x01
# st 1: \x00\x01\x05\x07
# st 2: \x00\x01\x60\x98
subtableClasses = {1: test_Class1, 2: test_Class2}
subtableOffsets = (2, 9, 15)

x, y = tryReadMultiFormatSubtablesFromBuffer(buffer, subtableClasses, subtableOffsets)
result = (len(x) == 3 and x == [2, 1, 1])
result &= (len(y) == 3 and type(y[0]) == test_Class2 and type(y[1]) == test_Class1 and type(y[2]) == test_Class1)
testResults["tryReadSubtablesFromBuffer test 13"] = result
result = (y[0].format == 2 and y[0].test1 == 0x0432 and y[0].test2 == 1)
result &= (y[1].format == 1 and y[1].test1 == 0x0507)
result &= (y[2].format == 1 and y[2].test1 == 0x6098)
testResults["tryReadMultiFormatSubtablesFromBuffer test 14"] = result







# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

# assert numTestResults == 155

printTestResultSummary("Tests for table_maxp", testResults, skippedTests)

