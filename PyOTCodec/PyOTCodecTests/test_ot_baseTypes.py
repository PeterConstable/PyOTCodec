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
               b'\x87\xe4\x79'
               b'\xf0\x00\x80\x00'
               b'\xf6\x42'
               b'\x48\x49\x4a\x4b'
               b'\xB2'
               )
testbio = BytesIO(testBytes1)


#-------------------------------------------------------------
# tests for file read methods
#-------------------------------------------------------------

from ot_baseTypes import _tryReadRawBytes
try:
    x = _tryReadRawBytes(BytesIO(b'\x42\x42\x42'), 4)
except OTCodecError:
    result = True
else:
    result = False
testResults["baseTypes file read test 1 (_tryReadRawBytes)"] = result
testResults["baseTypes file read test 2 (_tryReadRawBytes)"] = _tryReadRawBytes(testbio, 5) == b'\x02\x0F\x37\xDC\x9A'
testResults["baseTypes file read test 3 (int8.tryReadFromBytesIO)"] = int8.tryReadFromBytesIO(testbio) == -94 # \xA2
testResults["baseTypes file read test 4 (uint8.tryReadFromBytesIO)"] = uint8.tryReadFromBytesIO(testbio) == 0x0F
testResults["baseTypes file read test 5 (int16.tryReadFromBytesIO)"] = int16.tryReadFromBytesIO(testbio) == -6180 # \xE7\xDC
testResults["baseTypes file read test 6 (uint16.tryReadFromBytesIO)"] = uint16.tryReadFromBytesIO(testbio) == 0x9A02
testResults["baseTypes file read test 7 (int32.tryReadFromBytesIO)"] = int32.tryReadFromBytesIO(testbio) == -1087906662 # \xBF\x27\xDC\x9A
testResults["baseTypes file read test 8 (uint32.tryReadFromBytesIO)"] = uint32.tryReadFromBytesIO(testbio) == 0xB20F37DC
testResults["baseTypes file read test 9 (int64.tryReadFromBytesIO)"] = int64.tryReadFromBytesIO(testbio) == -7349294909316519972 # \x9A\x02\x0F\x37\xDC\x9A\x27\xDC
testResults["baseTypes file read test 10 (uint64.tryReadFromBytesIO)"] = uint64.tryReadFromBytesIO(testbio) == 0x27DC_9AB2_0F37_DC9A

testResults["baseTypes file read test 11 (FWord.tryReadFromBytesIO)"] = FWord.tryReadFromBytesIO(testbio) == -11628 # \xd2\x94
testResults["baseTypes file read test 12 (UFWord.tryReadFromBytesIO)"] = UFWord.tryReadFromBytesIO(testbio) == 0x92cf
testResults["baseTypes file read test 13 (Offset16.tryReadFromBytesIO)"] = Offset16.tryReadFromBytesIO(testbio) == 0x033a
testResults["baseTypes file read test 14 (Offset32.tryReadFromBytesIO)"] = Offset32.tryReadFromBytesIO(testbio) == 0xa928_bdf1
testResults["baseTypes file read test 15 (LongDateTime.tryReadFromBytesIO)"] = LongDateTime.tryReadFromBytesIO(testbio) == -4452760542906114592 # \xc2\x34\x9d\xe0\xc2\x34\x9d\xe0
testResults["baseTypes file read test 16 (uint24.tryReadFromBytesIO)"] = uint24.tryReadFromBytesIO(testbio) == 0x87_e479
testResults["baseTypes file read test 17 (Fixed.tryReadFromBytesIO)"] = Fixed.tryReadFromBytesIO(testbio)._rawBytes == b'\xf0\x00\x80\x00'
testResults["baseTypes file read test 18 (F2Dot14.tryReadFromBytesIO)"] = F2Dot14.tryReadFromBytesIO(testbio)._rawBytes == b'\xf6\x42'
testResults["baseTypes file read test 19 (Tag.tryReadFromBytesIO)"] = Tag.tryReadFromBytesIO(testbio)._rawBytes == b'\x48\x49\x4a\x4b'


#-------------------------------------------------------------
# tests for otTypeCategory
#-------------------------------------------------------------


result = hasattr(otTypeCategory, 'BASIC')
result &= hasattr(otTypeCategory, 'BASIC_OT_SPECIAL')
result &= hasattr(otTypeCategory, 'FIXED_LENGTH_BASIC_STRUCT')
result &= hasattr(otTypeCategory, 'VAR_LENGTH_STRUCT')
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
class testClass(int):
    TYPE_CATEGORY = otTypeCategory.BASIC
    pass
try:
    assertIsWellDefinedOTType(testClass)
except:
    result = True
else:
    result = False
testResults["baseTypes assertIsWellDefinedOTType test 3"] = result

class testClass(int):
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

class testClass(int):
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
class testClass(int):
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

class testClass(int):
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

class testClass(int):
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

# BASIC not a sub-class of int
class testClass:
    TYPE_CATEGORY = otTypeCategory.BASIC
    PACKED_FORMAT = ">h"
    PACKED_SIZE = 2
    pass
try:
    assertIsWellDefinedOTType(testClass)
except:
    result = True
else:
    result = False
testResults["baseTypes assertIsWellDefinedOTType test 9"] = result



#-------------------------------------------------------------
# Tests for concatFormatStrings
#-------------------------------------------------------------

# tests for concatFormatStrings
try:
    x = concatFormatStrings(None)
except:
    result = True
else:
    result = False
testResults["baseTypes concatFormatStrings test 1"] = result
try:
    x = concatFormatStrings(42)
except:
    result = True
else:
    result = False
testResults["baseTypes concatFormatStrings test 2"] = result
try:
    x = concatFormatStrings(42, "abc")
except:
    result = True
else:
    result = False
testResults["baseTypes concatFormatStrings test 3"] = result
try:
    x = concatFormatStrings("abc", 42)
except:
    result = True
else:
    result = False
testResults["baseTypes concatFormatStrings test 4"] = result
try:
    x = concatFormatStrings("abc", "def", 42, "ghi")
except:
    result = True
else:
    result = False
testResults["baseTypes concatFormatStrings test 5"] = result
try:
    x = concatFormatStrings("@abc", "def")
except OTCodecError:
    result = True
else:
    result = False
testResults["baseTypes concatFormatStrings test 6"] = result
try:
    x = concatFormatStrings(">abc", "@def")
except OTCodecError:
    result = True
else:
    result = False
testResults["baseTypes concatFormatStrings test 7"] = result
try:
    x = concatFormatStrings(">abc", ">def", "@ghi")
except OTCodecError:
    result = True
else:
    result = False
testResults["baseTypes concatFormatStrings test 8"] = result
testResults["baseTypes concatFormatStrings test 9"] = (concatFormatStrings("abc") == "abc")
testResults["baseTypes concatFormatStrings test 10"] = (concatFormatStrings(">abc", "def") == ">abcdef")
testResults["baseTypes concatFormatStrings test 11"] = (concatFormatStrings(">abc", ">def") == ">abcdef")
testResults["baseTypes concatFormatStrings test 12"] = (concatFormatStrings(">abc", ">def", "ghi") == ">abcdefghi")
testResults["baseTypes concatFormatStrings test 13"] = (concatFormatStrings(">abc", ">def", ">ghi") == ">abcdefghi")



#=============================================================
#  otTypeCategory.BASIC types
#=============================================================

#-------------------------------------------------------------
# tests for int8
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(int8)
except:
    result = False
else:
    result = True
testResults["baseTypes int8 definition test 1"] = result

testResults["baseTypes int8 definition test 2"] = (int8.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes int8 definition test 3"] = (int8.PACKED_FORMAT == ">b")
testResults["baseTypes int8 definition test 4"] = (int8.PACKED_SIZE == 1)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for uint8
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(uint8)
except:
    result = False
else:
    result = True
testResults["baseTypes uint8 definition test 1"] = result

testResults["baseTypes uint8 definition test 2"] = (uint8.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes uint8 definition test 3"] = (uint8.PACKED_FORMAT == ">B")
testResults["baseTypes uint8 definition test 4"] = (uint8.PACKED_SIZE == 1)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for int16
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(int16)
except:
    result = False
else:
    result = True
testResults["baseTypes int16 definition test 1"] = result

testResults["baseTypes int16 definition test 2"] = (int16.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes int16 definition test 3"] = (int16.PACKED_FORMAT == ">h")
testResults["baseTypes int16 definition test 4"] = (int16.PACKED_SIZE == 2)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for FWord
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(FWord)
except:
    result = False
else:
    result = True
testResults["baseTypes FWord definition test 1"] = result

testResults["baseTypes FWord definition test 2"] = (FWord.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes FWord definition test 3"] = (FWord.PACKED_FORMAT == ">h")
testResults["baseTypes FWord definition test 4"] = (FWord.PACKED_SIZE == 2)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for uint16
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(uint16)
except:
    result = False
else:
    result = True
testResults["baseTypes uint16 definition test 1"] = result

testResults["baseTypes uint16 definition test 2"] = (uint16.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes uint16 definition test 3"] = (uint16.PACKED_FORMAT == ">H")
testResults["baseTypes uint16 definition test 4"] = (uint16.PACKED_SIZE == 2)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for UFWord
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(UFWord)
except:
    result = False
else:
    result = True
testResults["baseTypes UFWord definition test 1"] = result

testResults["baseTypes UFWord definition test 2"] = (UFWord.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes UFWord definition test 3"] = (UFWord.PACKED_FORMAT == ">H")
testResults["baseTypes UFWord definition test 4"] = (UFWord.PACKED_SIZE == 2)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for Offset16
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(Offset16)
except:
    result = False
else:
    result = True
testResults["baseTypes Offset16 definition test 1"] = result

testResults["baseTypes Offset16 definition test 2"] = (Offset16.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes Offset16 definition test 3"] = (Offset16.PACKED_FORMAT == ">H")
testResults["baseTypes Offset16 definition test 4"] = (Offset16.PACKED_SIZE == 2)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for int32
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(int32)
except:
    result = False
else:
    result = True
testResults["baseTypes int32 definition test 1"] = result

testResults["baseTypes int32 definition test 2"] = (int32.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes int32 definition test 3"] = (int32.PACKED_FORMAT == ">l")
testResults["baseTypes int32 definition test 4"] = (int32.PACKED_SIZE == 4)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for uint32
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(uint32)
except:
    result = False
else:
    result = True
testResults["baseTypes uint32 definition test 1"] = result

testResults["baseTypes uint32 definition test 2"] = (uint32.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes uint32 definition test 3"] = (uint32.PACKED_FORMAT == ">L")
testResults["baseTypes uint32 definition test 4"] = (uint32.PACKED_SIZE == 4)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for Offset32
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(Offset32)
except:
    result = False
else:
    result = True
testResults["baseTypes Offset32 definition test 1"] = result

testResults["baseTypes Offset32 definition test 2"] = (Offset32.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes Offset32 definition test 3"] = (Offset32.PACKED_FORMAT == ">L")
testResults["baseTypes Offset32 definition test 4"] = (Offset32.PACKED_SIZE == 4)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for int64
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(int64)
except:
    result = False
else:
    result = True
testResults["baseTypes int64 definition test 1"] = result

testResults["baseTypes int64 definition test 2"] = (int64.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes int64 definition test 3"] = (int64.PACKED_FORMAT == ">q")
testResults["baseTypes int64 definition test 4"] = (int64.PACKED_SIZE == 8)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for LongDateTime
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(LongDateTime)
except:
    result = False
else:
    result = True
testResults["baseTypes LongDateTime definition test 1"] = result

testResults["baseTypes LongDateTime definition test 2"] = (LongDateTime.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes LongDateTime definition test 3"] = (LongDateTime.PACKED_FORMAT == ">q")
testResults["baseTypes LongDateTime definition test 4"] = (LongDateTime.PACKED_SIZE == 8)

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

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for uint64
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(uint64)
except:
    result = False
else:
    result = True
testResults["baseTypes uint64 definition test 1"] = result

testResults["baseTypes uint64 definition test 2"] = (uint64.TYPE_CATEGORY == otTypeCategory.BASIC)
testResults["baseTypes uint64 definition test 3"] = (uint64.PACKED_FORMAT == ">Q")
testResults["baseTypes uint64 definition test 4"] = (uint64.PACKED_SIZE == 8)

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

# see above for test of tryReadFromBytesIO



#=============================================================
#  otTypeCategory.BASIC_OT_SPECIAL types
#=============================================================

#-------------------------------------------------------------
# tests for uint24
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(uint24)
except:
    result = False
else:
    result = True
testResults["baseTypes uint24 definition test 1"] = result

testResults["baseTypes uint24 definition test 2"] = (uint24.TYPE_CATEGORY == otTypeCategory.BASIC_OT_SPECIAL)
testResults["baseTypes uint24 definition test 3"] = (uint24.PACKED_FORMAT == ">3s")
testResults["baseTypes uint24 definition test 4"] = (uint24.PACKED_SIZE == 3)
testResults["baseTypes uint24 definition test 5"] = (uint24.NUM_PACKED_VALUES == 1)

# constructor requires int argument in range [0, 0xffff_ffff_ffff]
try:
    x = uint24()
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes uint24 constructor test 1"] = result

try:
    x = uint24(24.3)
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes uint24 constructor test 2"] = result

try:
    x = uint24(-1)
except:
    result = True
else:
    result = False
testResults["baseTypes uint24 constructor test 3"] = result

try:
    x = uint24(0x1_0000_0000_0000)
except:
    result = True
else:
    result = False
testResults["baseTypes uint24 constructor test 4"] = result

x = uint24(0)
y = uint24(0xffff_ffff_ffff)
testResults["baseTypes uint24 constructor test 5"] = isinstance(x, int)
result = (type(x) == uint24 and type(y) == uint24 and (x + y) == 0xffff_ffff_ffff)
testResults["baseTypes uint24 constructor test 6"] = result

# constructor accepts bytearray / bytes argument of length 3
try:
    x = uint24(b'\x42\xac')
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes uint24 constructor test 7"] = result

try:
    x = uint24(b'\x42\xac\x87\x32')
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes uint24 constructor test 8"] = result

x = uint24(b'\x42\xac\x87')
result = (type(x) == uint24 and x == 0x42_ac87)
testResults["baseTypes uint24 constructor test 9"] = result


# createFromUnpackedValues

buffer = b'\x42\xac\x87'
val, = struct.unpack(uint24.PACKED_FORMAT, buffer)
x = uint24.createFromUnpackedValues(val)
result = (type(x) == uint24 and x == 0x42_ac87)
testResults["baseTypes uint24 createFromUnpackedValues test 1"] = result

# see above for test of tryReadFromBytesIO


#-------------------------------------------------------------
# tests for Fixed
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(Fixed)
except:
    result = False
else:
    result = True
testResults["baseTypes Fixed definition test 1"] = result

testResults["baseTypes Fixed definition test 2"] = (Fixed.TYPE_CATEGORY == otTypeCategory.BASIC_OT_SPECIAL)
testResults["baseTypes Fixed definition test 3"] = (Fixed.PACKED_FORMAT == ">4s")
testResults["baseTypes Fixed definition test 4"] = (Fixed.PACKED_SIZE == 4)
testResults["baseTypes Fixed definition test 5"] = (Fixed.NUM_PACKED_VALUES == 1)

# constructor

# arg must be bytearray or bytes
try:
    Fixed(None)
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes Fixed constructor test 1"] = result
try:
    Fixed(123)
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes Fixed constructor test 2"] = result

# arg length must be 4 bytes
try:
    Fixed(b'\x00\x01')
except TypeError:
    result = True
else:
    result = False
try:
    Fixed(b'\x00\x01\x02\x03\x04')
except TypeError:
    result &= True
else:
    result &= False
testResults["baseTypes Fixed constructor test 3"] = result

# good args
testResults["baseTypes Fixed constructor test 4"] = (type(Fixed(bytearray([0,1,0,0]))) == Fixed)
testResults["baseTypes Fixed constructor test 5"] = (type(Fixed(bytes(b'\xF0\x00\x80\x00'))) == Fixed)
testResults["baseTypes Fixed constructor test 6"] = (Fixed(b'\xF0\x00\x80\x00') == -4095.5)
testResults["baseTypes Fixed constructor test 7"] = (-4095.5 == Fixed(b'\xF0\x00\x80\x00'))

# Fixed.createFromUnpackedValues: arg must be between 0 and 0xffff_ffff

buffer = b'\x00\x01\x80\x00'
val, = struct.unpack(Fixed.PACKED_FORMAT, buffer)
x = Fixed.createFromUnpackedValues(val)
testResults["baseTypes Fixed.createFromUnpackedValues test 1"] = (x == 1.5)

buffer = b'\xf0\x00\x80\x00'
val, = struct.unpack(Fixed.PACKED_FORMAT, buffer)
x = Fixed.createFromUnpackedValues(val)
testResults["baseTypes Fixed.createFromUnpackedValues test 2"] = (x == -4095.5)

buffer = b'\x00\x01\x50\x00'
val, = struct.unpack(Fixed.PACKED_FORMAT, buffer)
x = Fixed.createFromUnpackedValues(val)
testResults["baseTypes Fixed.createFromUnpackedValues test 3"] = (x._rawBytes == bytes(b'\x00\x01\x50\x00'))

# Fixed.createFixedFromUint32
try:
    Fixed.createFixedFromUint32(-1)
except ValueError:
    result = True
else:
    result = False
testResults["baseTypes Fixed.createFixedFromUint32 test 1"] = result
try:
    Fixed.createFixedFromUint32(0x1_FFFF_FFFF)
except ValueError:
    result = True
else:
    result = False
testResults["baseTypes Fixed.createFixedFromUint32 test 2"] = result

f = Fixed.createFixedFromUint32(0x0001_8000)
testResults["baseTypes Fixed.createFixedFromUint32 test 3"] = (f == 1.5)
f = Fixed.createFixedFromUint32(0xF000_8000)
testResults["baseTypes Fixed.createFixedFromUint32 test 4"] = (f == -4095.5)
f = Fixed.createFixedFromUint32(0x0001_5000)
testResults["baseTypes Fixed.createFixedFromUint32 test 5"] = (f._rawBytes == bytes(b'\x00\x01\x50\x00'))


# tests for Fixed.tryReadFromBytesIO
# also see above for test of tryReadFromBytesIO
testbio = BytesIO(testBytes1)
f = Fixed.tryReadFromBytesIO(testbio)
testResults["baseTypes Fixed.tryReadFromBytesIO test 1"] = (type(f) == Fixed)
testResults["baseTypes Fixed.tryReadFromBytesIO test 2"] = (f.getFixedAsUint32() == 0x020F37DC)
f = Fixed.tryReadFromBytesIO(testbio)
testResults["baseTypes Fixed.tryReadFromBytesIO test 3"] = (f.getFixedAsUint32() == 0x9AA20FE7)
testbio.seek(-1, 2) #from end of stream
try:
    f = Fixed.tryReadFromBytesIO(testbio)
except OTCodecError:
    result = True
else:
    result = False
testResults["baseTypes Fixed.tryReadFromBytesIO test 4"] = result


# Fixed.createFixedFromFloat
try:
    Fixed.createFixedFromFloat(-40000)
except ValueError:
    result = True
else:
    result = False
testResults["baseTypes Fixed.createFixedFromFloat test 1"] = result
try:
    Fixed.createFixedFromFloat(40000)
except ValueError:
    result = True
else:
    result = False
testResults["baseTypes Fixed.createFixedFromFloat test 2"] = result

f = Fixed.createFixedFromFloat(1.5)
testResults["baseTypes Fixed.createFixedFromFloat test 3"] = (f._rawBytes == bytes(b'\x00\x01\x80\x00'))
f = Fixed.createFixedFromFloat(-4095.75)
testResults["baseTypes Fixed.createFixedFromFloat test 4"] = (f._rawBytes == bytes(b'\xF0\x00\x40\x00'))
f = Fixed.createFixedFromFloat(1.3125)
testResults["baseTypes Fixed.createFixedFromFloat test 5"] = (f._rawBytes == bytes(b'\x00\x01\x50\x00'))

# Fixed ==
f = Fixed(b'\xF0\x00\x80\x00')
testResults["baseTypes Fixed __eq__ test 1"] = (Fixed(b'\xF0\x00\x80\x00') == f)
testResults["baseTypes Fixed __eq__ test 2"] = (f == Fixed(b'\xF0\x00\x80\x00'))
testResults["baseTypes Fixed __eq__ test 3"] = (f != Fixed(b'\x00\x00\x00\x00'))
testResults["baseTypes Fixed __eq__ test 4"] = (f == bytearray(b'\xF0\x00\x80\x00'))
testResults["baseTypes Fixed __eq__ test 5"] = (f == bytes(b'\xF0\x00\x80\x00'))
testResults["baseTypes Fixed __eq__ test 6"] = (f == -4095.5)
f = Fixed(b'\xF0\x00\x00\x00')
testResults["baseTypes Fixed __eq__ test 7"] = (f == -4096)
testResults["baseTypes Fixed __eq__ test 8"] = (f == 0xF000_0000)

# Fixed misc
f = Fixed(b'\xF0\x00\x80\x00')
testResults["baseTypes Fixed members test 1"] = (f.mantissa == -4096)
testResults["baseTypes Fixed members test 2"] = (f.fraction == 0x8000)
testResults["baseTypes Fixed members test 3"] = (f.getFixedAsUint32() == 0xF0008000)
testResults["baseTypes Fixed members test 4"] = (f.__str__() == "-4095.5")
testResults["baseTypes Fixed members test 5"] = (f.__repr__() == "-4095.5")
f = Fixed(b'\x00\x02\x50\x00')
testResults["baseTypes Fixed members test 6"] = (f.fixedTableVersion == 2.5)



#-------------------------------------------------------------
# tests for F2Dot14
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(F2Dot14)
except:
    result = False
else:
    result = True
testResults["baseTypes F2Dot14 definition test 1"] = result

testResults["baseTypes F2Dot14 definition test 2"] = (F2Dot14.TYPE_CATEGORY == otTypeCategory.BASIC_OT_SPECIAL)
testResults["baseTypes F2Dot14 definition test 3"] = (F2Dot14.PACKED_FORMAT == ">2s")
testResults["baseTypes F2Dot14 definition test 4"] = (F2Dot14.PACKED_SIZE == 2)
testResults["baseTypes F2Dot14 definition test 5"] = (F2Dot14.NUM_PACKED_VALUES == 1)

# constructor tests

# arg must be bytearray or bytes
try:
    F2Dot14(None)
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes F2Dot14 constructor test 1"] = result
try:
    F2Dot14(123)
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes F2Dot14 constructor test 2"] = result

# arg length must be 2 bytes
try:
    F2Dot14(b'\x01')
except TypeError:
    result = True
else:
    result = False
try:
    F2Dot14(b'\x00\x01\x02')
except TypeError:
    result &= True
else:
    result &= False
testResults["baseTypes F2Dot14 constructor test 3"] = result

# good args
testResults["baseTypes F2Dot14 constructor test 4"] = (type(F2Dot14(bytearray([0,1]))) == F2Dot14)
testResults["baseTypes F2Dot14 constructor test 5"] = (type(F2Dot14(bytes(b'\xF0\x00'))) == F2Dot14)
testResults["baseTypes F2Dot14 constructor test 6"] = (F2Dot14(b'\xF0\x00') == -0.25)


# F2Dot14.createFromUnpackedValues
buffer = b'\x60\x00'
val, = struct.unpack(F2Dot14.PACKED_FORMAT, buffer)
x = F2Dot14.createFromUnpackedValues(val)
testResults["baseTypes F2Dot14.createFromUnpackedValues test 1"] = (x == 1.5)

buffer = b'\xf0\x00'
val, = struct.unpack(F2Dot14.PACKED_FORMAT, buffer)
x = F2Dot14.createFromUnpackedValues(val)
testResults["baseTypes F2Dot14.createFromUnpackedValues test 2"] = (x == -0.25)

buffer = b'\x3c\x01'
val, = struct.unpack(F2Dot14.PACKED_FORMAT, buffer)
x = F2Dot14.createFromUnpackedValues(val)
testResults["baseTypes F2Dot14.createFromUnpackedValues test 3"] = (x._rawBytes == bytes(b'\x3c\x01'))

# F2Dot14.createF2Dot14FromUint16: arg must be between 0 and 0xffff
try:
    F2Dot14.createF2Dot14FromUint16(-1)
except ValueError:
    result = True
else:
    result = False
testResults["baseTypes F2Dot14.createF2Dot14FromUint16 test 1"] = result
try:
    F2Dot14.createF2Dot14FromUint16(0x1_0000)
except ValueError:
    result = True
else:
    result = False
testResults["baseTypes F2Dot14.createF2Dot14FromUint16 test 2"] = result

f = F2Dot14.createF2Dot14FromUint16(0x6000)
testResults["baseTypes F2Dot14.createF2Dot14FromUint16 test 3"] = (f == 1.5)
f = F2Dot14.createF2Dot14FromUint16(0xF000)
testResults["baseTypes F2Dot14.createF2Dot14FromUint16 test 4"] = (f == -0.25)
f = F2Dot14.createF2Dot14FromUint16(0x3c01)
testResults["baseTypes F2Dot14.createF2Dot14FromUint16 test 5"] = (f._rawBytes == bytes(b'\x3c\x01'))

# F2Dot14.createF2Dot14FromFloat
try:
    F2Dot14.createF2Dot14FromFloat(-4)
except ValueError:
    result = True
else:
    result = False
testResults["baseTypes F2Dot14.createF2Dot14FromFloat test 1"] = result
try:
    F2Dot14.createF2Dot14FromFloat(4)
except ValueError:
    result = True
else:
    result = False
testResults["baseTypes F2Dot14.createF2Dot14FromFloat test 2"] = result

f = F2Dot14.createF2Dot14FromFloat(1.5)
testResults["baseTypes F2Dot14.createF2Dot14FromFloat test 3"] = (f._rawBytes == bytes(b'\x60\x00'))
f = F2Dot14.createF2Dot14FromFloat(-0.25)
testResults["baseTypes F2Dot14.createF2Dot14FromFloat test 4"] = (f._rawBytes == bytes(b'\xF0\x00'))
f = F2Dot14.createF2Dot14FromFloat(1.3125)
testResults["baseTypes F2Dot14.createF2Dot14FromFloat test 5"] = (f._rawBytes == bytes(b'\x54\x00'))

# tests for F2Dot14.tryReadFromBytesIO
testbio = BytesIO(testBytes1)
f = F2Dot14.tryReadFromBytesIO(testbio)
testResults["baseTypes F2Dot14.tryReadFromBytesIO test 1"] = (type(f) == F2Dot14)
testResults["baseTypes F2Dot14.tryReadFromBytesIO test 2"] = (f.getF2Dot14AsUint16() == 0x020F)
f = F2Dot14.tryReadFromBytesIO(testbio)
testResults["baseTypes F2Dot14.tryReadFromBytesIO test 3"] = (f.getF2Dot14AsUint16() == 0x37DC)
testbio.seek(-1, 2) #from end of stream
try:
    f = F2Dot14.tryReadFromBytesIO(testbio)
except OTCodecError:
    result = True
else:
    result = False
testResults["baseTypes F2Dot14.tryReadFromBytesIO test 4"] = result

# F2Dot14 __eq__
f = F2Dot14(b'\xF0\x80')
testResults["baseTypes F2Dot14 __eq__ test 1"] = (F2Dot14(b'\xF0\x80') == f)
testResults["baseTypes F2Dot14 __eq__ test 2"] = (f == F2Dot14(b'\xF0\x80'))
testResults["baseTypes F2Dot14 __eq__ test 3"] = (f != F2Dot14(b'\x00\x00'))
testResults["baseTypes F2Dot14 __eq__ test 4"] = (f == bytearray(b'\xF0\x80'))
testResults["baseTypes F2Dot14 __eq__ test 5"] = (f == bytes(b'\xF0\x80'))
testResults["baseTypes F2Dot14 __eq__ test 6"] = (f == -0.2421875)

# F2Dot14 misc
f = F2Dot14(b'\xB0\x00')
testResults["baseTypes F2Dot14 members test 1"] = (f.mantissa == -2)
testResults["baseTypes F2Dot14 members test 2"] = (f.fraction == 0x3000)
testResults["baseTypes F2Dot14 members test 3"] = (f.getF2Dot14AsUint16() == 0xB000)
testResults["baseTypes F2Dot14 members test 4"] = (f.__str__() == "-1.25")
testResults["baseTypes F2Dot14 members test 5"] = (f.__repr__() == "-1.25")


#-------------------------------------------------------------
# tests for Tag
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(Tag)
except:
    result = False
else:
    result = True
testResults["baseTypes Tag definition test 1"] = result

testResults["baseTypes Tag definition test 2"] = (Tag.TYPE_CATEGORY == otTypeCategory.BASIC_OT_SPECIAL)
testResults["baseTypes Tag definition test 3"] = (Tag.PACKED_FORMAT == ">4s")
testResults["baseTypes Tag definition test 4"] = (Tag.PACKED_SIZE == 4)
testResults["baseTypes Tag definition test 5"] = (Tag.NUM_PACKED_VALUES == 1)

# constructor tests

# argument other than str, bytes or bytearray
try:
    Tag([0,1,0,0])
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes Tag constructor test 1"] = result

# argument with invalid characters (out of range 0 - 127)
try:
    Tag("ab¡c")
except ValueError:
    result = True
else:
    result = False
testResults["baseTypes Tag constructor test 2"] = result
try:
    Tag(b'\x61\xa1\x20\x20')
except ValueError:
    result = True
else:
    result = False
testResults["baseTypes Tag constructor test 3"] = result

x = Tag(b'\x00\x01') # pad with 0x00
testResults["baseTypes Tag constructor test 4"] = (x == b'\x00\x01\x00\x00')
x = Tag(b'\x61\x62\x63\x64')
testResults["baseTypes Tag constructor test 5"] = (x == "abcd")
x = Tag("ab") # pad with space
testResults["baseTypes Tag constructor test 6"] = (x == "ab  ")
x = Tag("abcd")
testResults["baseTypes Tag constructor test 7"] = (x == "abcd")

# Tag.createFromUnpackedValues: bytearray or bytes, length 4
try:
    Tag.createFromUnpackedValues(1)
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes Tag.createFromUnpackedValues test 1"] = result

try:
    Tag.createFromUnpackedValues(b'\x00')
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes Tag.createFromUnpackedValues test 2"] = result

try:
    Tag.createFromUnpackedValues(b'\x00\x01\x02\x03\x04')
except TypeError:
    result = True
else:
    result = False
testResults["baseTypes Tag.createFromUnpackedValues test 3"] = result

x = Tag.createFromUnpackedValues(b'\x68\x69\x6a\x6b')
result = (type(x) == Tag and x == 'hijk')
testResults["baseTypes Tag.createFromUnpackedValues test 4"] = result

# tests for Tag.tryReadFromBytesIO
testbio = BytesIO(b'\x61\x63\x65\x67\x48\x49\x4a\x4b\x00\x00\x01\x02\x03')
x = Tag.tryReadFromBytesIO(testbio)
testResults["baseTypes Tag.tryReadFromBytesIO test 1"] = (type(x) == Tag)
testResults["baseTypes Tag.tryReadFromBytesIO test 2"] = (x._rawBytes == b'\x61\x63\x65\x67')
x = Tag.tryReadFromBytesIO(testbio)
testResults["baseTypes Tag.tryReadFromBytesIO test 3"] = (x._rawBytes == b'\x48\x49\x4a\x4b')
testbio.seek(-1, 2) #from end of stream
try:
    x = Tag.tryReadFromBytesIO(testbio)
except OTCodecError:
    result = True
else:
    result = False
testResults["baseTypes Tag.tryReadFromBytesIO test 4"] = result


# Tag __eq__, __ne__
x = Tag("abcd")
testResults["baseTypes Tag methods test 1"] = (x == Tag("abcd"))
testResults["baseTypes Tag methods test 2"] = (Tag("abcd") == x)
testResults["baseTypes Tag methods test 3"] = (x != Tag("abce"))
testResults["baseTypes Tag methods test 4"] = (x == b'\x61\x62\x63\x64')
testResults["baseTypes Tag methods test 5"] = (x != b'\x61\x62\x63\x65')
testResults["baseTypes Tag methods test 6"] = (x == "abcd")
testResults["baseTypes Tag methods test 7"] = (x != "abce")
testResults["baseTypes Tag methods test 8"] = (x.__hash__() == str.__hash__("abcd"))

# Tag validations
testResults["baseTypes Tag validation test 1"] = Tag.validateTag("abcd") == 0
testResults["baseTypes Tag validation test 2"] = Tag.validateTag("abc") == 0x01
testResults["baseTypes Tag validation test 3"] = Tag.validateTag("abcde") == 0x01
testResults["baseTypes Tag validation test 4"] = Tag.validateTag("ab€c") == 0x02
testResults["baseTypes Tag validation test 5"] = Tag.validateTag("ab c") == 0x04
testResults["baseTypes Tag validation test 6"] = Tag.validateTag(" €c") == 0x07




# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

assert numTestResults == 290

printTestResultSummary("Tests for ot_baseTypes", testResults, skippedTests)
