from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from ot_baseTypes import *


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
               b'\xd2\x94'
               b'\x92\xcf'
               b'\x03\x3a'
               b'\xa9\x28\xbd\xf1'
               b'\xc2\x34\x9d\xe0\xc2\x34\x9d\xe0'
               b'\xB2'
               )
testbio = BytesIO(testBytes1)


#-------------------------------------------------------------
# tests for file read methods
#-------------------------------------------------------------

from ot_baseTypes import _readRawBytes
testResults["baseTypes file read test 1 (_readRawBytes)"] = _readRawBytes(testbio, 5) == b'\x02\x0F\x37\xDC\x9A'
testResults["baseTypes file read test 2 (int8.readFromBytesIO)"] = int8.readFromBytesIO(testbio) == -94 # \xA2
testResults["baseTypes file read test 3 (uint8.readFromBytesIO)"] = uint8.readFromBytesIO(testbio) == 0x0F
testResults["baseTypes file read test 4 (int16.readFromBytesIO)"] = int16.readFromBytesIO(testbio) == -6180 # \xE7\xDC
testResults["baseTypes file read test 5 (uint16.readFromBytesIO)"] = uint16.readFromBytesIO(testbio) == 0x9A02
testResults["baseTypes file read test 6 (int32.readFromBytesIO)"] = int32.readFromBytesIO(testbio) == -1087906662 # \xBF\x27\xDC\x9A
testResults["baseTypes file read test 7 (uint32.readFromBytesIO)"] = uint32.readFromBytesIO(testbio) == 0xB20F37DC
testResults["baseTypes file read test 8 (int64.readFromBytesIO)"] = int64.readFromBytesIO(testbio) == -7349294909316519972 # \x9A\x02\x0F\x37\xDC\x9A\x27\xDC
testResults["baseTypes file read test 9 (uint64.readFromBytesIO)"] = uint64.readFromBytesIO(testbio) == 0x27DC_9AB2_0F37_DC9A

testResults["baseTypes file read test 10 (FWord.readFromBytesIO)"] = FWord.readFromBytesIO(testbio) == -11,628 # \xd2\x94
testResults["baseTypes file read test 11 (UFWord.readFromBytesIO)"] = UFWord.readFromBytesIO(testbio) == 0x92cf
testResults["baseTypes file read test 12 (Offset16.readFromBytesIO)"] = Offset16.readFromBytesIO(testbio) == 0x033a
testResults["baseTypes file read test 13 (Offset32.readFromBytesIO)"] = Offset32.readFromBytesIO(testbio) == 0xa928_bdf1
testResults["baseTypes file read test 14 (LongDateTime.readFromBytesIO)"] = LongDateTime.readFromBytesIO(testbio) == -4452760542906114592 # \xc2\x34\x9d\xe0\xc2\x34\x9d\xe0


#-------------------------------------------------------------
# tests for otTypeCategory
#-------------------------------------------------------------


result = hasattr(otTypeCategory, 'BASIC')
result &= hasattr(otTypeCategory, 'BASIC_OT_SPECIAL')
result &= hasattr(otTypeCategory, 'BASIC_FIXED_STRUCT')
result &= hasattr(otTypeCategory, 'BASIC_VARIABLE_STRUCT')
testResults["baseTypes otTypeCategory constants test"] = result


#-------------------------------------------------------------
# tests for assertIsWellDefinedOTType
#-------------------------------------------------------------

# missing TYPE_CATEGORY
class testClass:
    pass

try:
    assertIsWellDefinedOTType(testClass)
except:
    result = True
else:
    result = False
testResults["baseTypes assertIsWellDefinedOTType test 1"] = result

# TYPE_CATEGORY not an otTypeCategory
class testClass:
    TYPE_CATEGORY = 42
    pass
try:
    assertIsWellDefinedOTType(testClass)
except:
    result = True
else:
    result = False
testResults["baseTypes assertIsWellDefinedOTType test 2"] = result


# BASIC

# missing PACKED_FORMAT, wrong type, or not starting with '>'
class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
    pass
try:
    assertIsWellDefinedOTType(testClass)
except:
    result = True
else:
    result = False
testResults["baseTypes assertIsWellDefinedOTType test 3"] = result

class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = 42
    pass
try:
    assertIsWellDefinedOTType(testClass)
except:
    result = True
else:
    result = False
testResults["baseTypes assertIsWellDefinedOTType test 4"] = result

class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = "x"
    pass
try:
    assertIsWellDefinedOTType(testClass)
except:
    result = True
else:
    result = False
testResults["baseTypes assertIsWellDefinedOTType test 5"] = result


# missing PACKED_SIZE, wrong type, or not correct value
class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">h"
    pass
try:
    assertIsWellDefinedOTType(testClass)
except:
    result = True
else:
    result = False
testResults["baseTypes assertIsWellDefinedOTType test 6"] = result

class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">h"
    PACKED_SIZE = 'x'
    pass
try:
    assertIsWellDefinedOTType(testClass)
except:
    result = True
else:
    result = False
testResults["baseTypes assertIsWellDefinedOTType test 7"] = result

class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">h"
    PACKED_SIZE = 4
    pass
try:
    assertIsWellDefinedOTType(testClass)
except:
    result = True
else:
    result = False
testResults["baseTypes assertIsWellDefinedOTType test 8"] = result




#-------------------------------------------------------------
# tests for int8
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(int8)
except:
    result = False
else:
    result = True
testResults["baseTypes int8 definition test"] = result

# constructor requires int argument in range [-128, 127]
try:
    x = int8()
except:
    result = True
else:
    result = False
testResults["baseTypes int8 constructor test 1"] = result

try:
    x = int8(-129)
except:
    result = True
else:
    result = False
testResults["baseTypes int8 constructor test 2"] = result

try:
    x = int8(128)
except:
    result = True
else:
    result = False
testResults["baseTypes int8 constructor test 3"] = result

x = int8(-128)
y = int8(127)
testResults["baseTypes int8 constructor test 4"] = isinstance(x, int)
result = (type(x) == int8 and type(y) == int8 and (x + y) == -1)
testResults["baseTypes int8 constructor test 5"] = result




#-------------------------------------------------------------
# tests for uint8
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(uint8)
except:
    result = False
else:
    result = True
testResults["baseTypes uint8 definition test"] = result

# constructor requires int argument in range [0, 255]
try:
    x = uint8()
except:
    result = True
else:
    result = False
testResults["baseTypes uint8 constructor test 1"] = result

try:
    x = uint8(-1)
except:
    result = True
else:
    result = False
testResults["baseTypes uint8 constructor test 2"] = result

try:
    x = uint8(256)
except:
    result = True
else:
    result = False
testResults["baseTypes uint8 constructor test 3"] = result

x = uint8(0)
y = uint8(255)
testResults["baseTypes uint8 constructor test 4"] = isinstance(x, int)
result = (type(x) == uint8 and type(y) == uint8 and (x + y) == 255)
testResults["baseTypes uint8 constructor test 5"] = result


#-------------------------------------------------------------
# tests for int16
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(int16)
except:
    result = False
else:
    result = True
testResults["baseTypes int16 definition test"] = result

# constructor requires int argument in range [-(0x8000), 0x7fff]
try:
    x = int16()
except:
    result = True
else:
    result = False
testResults["baseTypes int16 constructor test 1"] = result

try:
    x = int16(-(0x8001))
except:
    result = True
else:
    result = False
testResults["baseTypes int16 constructor test 2"] = result

try:
    x = int16(0x8000)
except:
    result = True
else:
    result = False
testResults["baseTypes int16 constructor test 3"] = result

x = int16(-(0x8000))
y = int16(0x7fff)
testResults["baseTypes int16 constructor test 4"] = isinstance(x, int)
result = (type(x) == int16 and type(y) == int16 and (x + y) == -1)
testResults["baseTypes int16 constructor test 5"] = result


#-------------------------------------------------------------
# tests for FWord
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(FWord)
except:
    result = False
else:
    result = True
testResults["baseTypes FWord definition test"] = result

# constructor requires int argument in range [-(0x8000), 0x7fff]
try:
    x = FWord()
except:
    result = True
else:
    result = False
testResults["baseTypes FWord constructor test 1"] = result

try:
    x = FWord(-(0x8001))
except:
    result = True
else:
    result = False
testResults["baseTypes FWord constructor test 2"] = result

try:
    x = FWord(0x8000)
except:
    result = True
else:
    result = False
testResults["baseTypes FWord constructor test 3"] = result

x = FWord(-(0x8000))
y = FWord(0x7fff)
testResults["baseTypes FWord constructor test 4"] = isinstance(x, int16)
result = (type(x) == FWord and type(y) == FWord and (x + y) == -1)
testResults["baseTypes FWord constructor test 5"] = result


#-------------------------------------------------------------
# tests for uint16
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(uint16)
except:
    result = False
else:
    result = True
testResults["baseTypes uint16 definition test"] = result

# constructor requires int argument in range [0, 0xffff]
try:
    x = uint16()
except:
    result = True
else:
    result = False
testResults["baseTypes uint16 constructor test 1"] = result

try:
    x = uint16(-1)
except:
    result = True
else:
    result = False
testResults["baseTypes uint16 constructor test 2"] = result

try:
    x = uint16(0x1_0000)
except:
    result = True
else:
    result = False
testResults["baseTypes uint16 constructor test 3"] = result

x = uint16(0)
y = uint16(0xffff)
testResults["baseTypes uint16 constructor test 4"] = isinstance(x, int)
result = (type(x) == uint16 and type(y) == uint16 and (x + y) == 0xffff)
testResults["baseTypes uint16 constructor test 5"] = result


#-------------------------------------------------------------
# tests for UFWord
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(UFWord)
except:
    result = False
else:
    result = True
testResults["baseTypes UFWord definition test"] = result

# constructor requires int argument in range [0, 0xffff]
try:
    x = UFWord()
except:
    result = True
else:
    result = False
testResults["baseTypes UFWord constructor test 1"] = result

try:
    x = UFWord(-1)
except:
    result = True
else:
    result = False
testResults["baseTypes UFWord constructor test 2"] = result

try:
    x = UFWord(0x1_0000)
except:
    result = True
else:
    result = False
testResults["baseTypes UFWord constructor test 3"] = result

x = UFWord(0)
y = UFWord(0xffff)
testResults["baseTypes UFWord constructor test 4"] = isinstance(x, uint16)
result = (type(x) == UFWord and type(y) == UFWord and (x + y) == 0xffff)
testResults["baseTypes UFWord constructor test 5"] = result


#-------------------------------------------------------------
# tests for Offset16
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(Offset16)
except:
    result = False
else:
    result = True
testResults["baseTypes Offset16 definition test"] = result

# constructor requires int argument in range [0, 0xffff]
try:
    x = Offset16()
except:
    result = True
else:
    result = False
testResults["baseTypes Offset16 constructor test 1"] = result

try:
    x = Offset16(-1)
except:
    result = True
else:
    result = False
testResults["baseTypes Offset16 constructor test 2"] = result

try:
    x = Offset16(0x1_0000)
except:
    result = True
else:
    result = False
testResults["baseTypes Offset16 constructor test 3"] = result

x = Offset16(0)
y = Offset16(0xffff)
testResults["baseTypes Offset16 constructor test 4"] = isinstance(x, uint16)
result = (type(x) == Offset16 and type(y) == Offset16 and (x + y) == 0xffff)
testResults["baseTypes Offset16 constructor test 5"] = result



#-------------------------------------------------------------
# tests for int32
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(int32)
except:
    result = False
else:
    result = True
testResults["baseTypes int32 definition test"] = result

# constructor requires int argument in range [-0x8000_0000, 0x7fff_ffff]
try:
    x = int32()
except:
    result = True
else:
    result = False
testResults["baseTypes int32 constructor test 1"] = result

try:
    x = int32(-0x8000_0001)
except:
    result = True
else:
    result = False
testResults["baseTypes int32 constructor test 2"] = result

try:
    x = int32(0x8000_0000)
except:
    result = True
else:
    result = False
testResults["baseTypes int32 constructor test 3"] = result

x = int32(-0x8000_0000)
y = int32(0x7fff_ffff)
testResults["baseTypes int32 constructor test 4"] = isinstance(x, int)
result = (type(x) == int32 and type(y) == int32 and (x + y) == -1)
testResults["baseTypes int32 constructor test 5"] = result


#-------------------------------------------------------------
# tests for uint32
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(uint32)
except:
    result = False
else:
    result = True
testResults["baseTypes uint32 definition test"] = result

# constructor requires int argument in range [0, 0xffff_ffff]
try:
    x = uint32()
except:
    result = True
else:
    result = False
testResults["baseTypes uint32 constructor test 1"] = result

try:
    x = uint32(-1)
except:
    result = True
else:
    result = False
testResults["baseTypes uint32 constructor test 2"] = result

try:
    x = uint32(0x1_0000_0000)
except:
    result = True
else:
    result = False
testResults["baseTypes uint32 constructor test 3"] = result

x = uint32(0)
y = uint32(0xffff_ffff)
testResults["baseTypes uint32 constructor test 4"] = isinstance(x, int)
result = (type(x) == uint32 and type(y) == uint32 and (x + y) == 0xffff_ffff)
testResults["baseTypes uint32 constructor test 5"] = result


#-------------------------------------------------------------
# tests for Offset32
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(Offset32)
except:
    result = False
else:
    result = True
testResults["baseTypes Offset32 definition test"] = result

# constructor requires int argument in range [0, 0xffff_ffff]
try:
    x = Offset32()
except:
    result = True
else:
    result = False
testResults["baseTypes Offset32 constructor test 1"] = result

try:
    x = Offset32(-1)
except:
    result = True
else:
    result = False
testResults["baseTypes Offset32 constructor test 2"] = result

try:
    x = Offset32(0x1_0000_0000)
except:
    result = True
else:
    result = False
testResults["baseTypes Offset32 constructor test 3"] = result

x = Offset32(0)
y = Offset32(0xffff_ffff)
testResults["baseTypes Offset32 constructor test 4"] = isinstance(x, uint32)
result = (type(x) == Offset32 and type(y) == Offset32 and (x + y) == 0xffff_ffff)
testResults["baseTypes Offset32 constructor test 5"] = result


#-------------------------------------------------------------
# tests for int64
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(int64)
except:
    result = False
else:
    result = True
testResults["baseTypes int64 definition test"] = result

# constructor requires int argument in range [-0x8000_0000_0000_0000, 0x7fff_ffff_ffff_ffff]
try:
    x = int64()
except:
    result = True
else:
    result = False
testResults["baseTypes int64 constructor test 1"] = result

try:
    x = int64(-0x8000_0000_0000_0001)
except:
    result = True
else:
    result = False
testResults["baseTypes int64 constructor test 2"] = result

try:
    x = int64(0x8000_0000_0000_0000)
except:
    result = True
else:
    result = False
testResults["baseTypes int64 constructor test 3"] = result

x = int64(-0x8000_0000_0000_0000)
y = int64(0x7fff_ffff_ffff_ffff)
testResults["baseTypes int64 constructor test 4"] = isinstance(x, int)
result = (type(x) == int64 and type(y) == int64 and (x + y) == -1)
testResults["baseTypes int64 constructor test 5"] = result


#-------------------------------------------------------------
# tests for LongDateTime
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(LongDateTime)
except:
    result = False
else:
    result = True
testResults["baseTypes LongDateTime definition test"] = result

# constructor requires int argument in range [-0x8000_0000_0000_0000, 0x7fff_ffff_ffff_ffff]
try:
    x = LongDateTime()
except:
    result = True
else:
    result = False
testResults["baseTypes LongDateTime constructor test 1"] = result

try:
    x = LongDateTime(-0x8000_0000_0000_0001)
except:
    result = True
else:
    result = False
testResults["baseTypes LongDateTime constructor test 2"] = result

try:
    x = LongDateTime(0x8000_0000_0000_0000)
except:
    result = True
else:
    result = False
testResults["baseTypes LongDateTime constructor test 3"] = result

x = LongDateTime(-0x8000_0000_0000_0000)
y = LongDateTime(0x7fff_ffff_ffff_ffff)
testResults["baseTypes LongDateTime constructor test 4"] = isinstance(x, int64)
result = (type(x) == LongDateTime and type(y) == LongDateTime and (x + y) == -1)
testResults["baseTypes LongDateTime constructor test 5"] = result


#-------------------------------------------------------------
# tests for uint64
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(uint64)
except:
    result = False
else:
    result = True
testResults["baseTypes uint64 definition test"] = result

# constructor requires int argument in range [0, 0xffff_ffff_ffff_ffff]
try:
    x = uint64()
except:
    result = True
else:
    result = False
testResults["baseTypes uint64 constructor test 1"] = result

try:
    x = uint64(-1)
except:
    result = True
else:
    result = False
testResults["baseTypes uint64 constructor test 2"] = result

try:
    x = uint64(0x1_0000_0000_0000_0000)
except:
    result = True
else:
    result = False
testResults["baseTypes uint64 constructor test 3"] = result

x = uint64(0)
y = uint64(0xffff_ffff_ffff_ffff)
testResults["baseTypes uint64 constructor test 4"] = isinstance(x, int)
result = (type(x) == uint64 and type(y) == uint64 and (x + y) == 0xffff_ffff_ffff_ffff)
testResults["baseTypes uint64 constructor test 5"] = result







# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

assert numTestResults == 101

printTestResultSummary("Tests for table_maxp", testResults, skippedTests)
