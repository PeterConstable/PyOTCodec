from ot_file import * # imports are transitive







#-------------------------------------------------------------
# END -- anything that follows is for testing
#-------------------------------------------------------------


testResults = dict({})
skippedTests = []

# Several tests will use selawk.ttf, SourceHanSans-Regular.TTC
selawk_file = OTFile(r"TestData\selawk.ttf")
sourceHansSans_file = OTFile(r"TestData\SourceHanSans-Regular.TTC")
bungeeColor_file = OTFile(r"TestData\BungeeColor-Regular_colr_Windows.ttf")
notoHW_COLR1_rev2 = OTFile(r"TestData\noto-handwriting-colr_1_rev2.ttf")



#-------------------------------------------------------------
# Tests for low-level stuff: 
#   - file read methods
#   - custom types: Tag, Fixed, F2Dot14
#-------------------------------------------------------------

# test methods to read specific data types from file
from io import BytesIO
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
testbio = BytesIO(testBytes1)
testResults["File read test 1 (ReadRawBytes)"] = ReadRawBytes(testbio, 5) == b'\x02\x0F\x37\xDC\x9A'
testResults["File read test 2 (ReadInt8)"] = ReadInt8(testbio) == -94 # \xA2
testResults["File read test 3 (ReadUint8)"] = ReadUint8(testbio) == 0x0F
testResults["File read test 4 (ReadInt16)"] = ReadInt16(testbio) == -6180 # \xE7\xDC
testResults["File read test 5 (ReadUint16)"] = ReadUint16(testbio) == 0x9A02
testResults["File read test 6 (ReadInt32)"] = ReadInt32(testbio) == -1087906662 # \xBF\x27\xDC\x9A
testResults["File read test 7 (ReadUint32)"] = ReadUint32(testbio) == 0xB20F37DC
testResults["File read test 8 (ReadInt64)"] = ReadInt64(testbio) == -7349294909316519972 # \x9A\x02\x0F\x37\xDC\x9A\x27\xDC
testResults["File read test 9 (ReadUint64)"] = ReadUint64(testbio) == 0x27DC9AB20F37DC9A

# reading with insufficient data left from current position
try:
    ReadInt16(testbio)
except OTCodecError:
    result = True
else:
    result = False
testResults["File read test 10 (insufficient data)"] = result

# reading with insufficient data left from current position
testbio.seek(-1, 2)
try:
    ReadRawBytes(testbio, 2)
except OTCodecError:
    result = True
else:
    result = False
testResults["File read test 11 (insufficient data)"] = result


# tests for calcCheckSum
b = b'\0\0\0\1\0\0\0\2\0\0\0\3'
testResults["calcChecksum test 1"] = (calcCheckSum(b) == 6)
b = b'\0\0\0\1\0\0\0\2\0\0\0\3\0'
testResults["calcChecksum test 2"] = (calcCheckSum(b) == 6)
testResults["calcChecksum test 3"] = (calcCheckSum(b, 4) == 10)
b = bytearray(b'\0\0\0\1\0\0\0\2\0\0\0\3\0')
b1 = b
testResults["calcChecksum test 4"] = (calcCheckSum(b) == 6)
testResults["calcChecksum test 5"] = (b == b1)
b = bytes(b'\0\0\0\1\0\0\0\2\0\0\0\3\0')
b1 = b
testResults["calcChecksum test 6"] = (calcCheckSum(b) == 6)
testResults["calcChecksum test 7"] = (b == b1)
b = memoryview(b'\0\0\0\1\0\0\0\2\0\0\0\3\0')
b1 = b
testResults["calcChecksum test 8"] = (calcCheckSum(b) == 6)
testResults["calcChecksum test 9"] = (b == b1)

hhea = selawk_file.fonts[0].tables["hhea"]
tr_hhea = selawk_file.fonts[0].offsetTable.tryGetTableRecord("hhea")
testResults["calcChecksum test 10"] = (hhea.calculatedCheckSum == tr_hhea.checkSum)


# tests for Tag

testResults["Tag constants test 1"] = (Tag._packedFormat == ">4s")
testResults["Tag constants test 2"] = (Tag._packedSize == 4)
testResults["Tag constants test 3"] = (Tag._numPackedValues == 1)

x = Tag(b'\x00\x01') # pad with 0x00
testResults["Tag constructor test 1"] = (x == b'\x00\x01\x00\x00')
x = Tag(b'\x61\x62\x63\x64')
testResults["Tag constructor test 2"] = (x == "abcd")
x = Tag("ab") # pad with space
testResults["Tag constructor test 3"] = (x == "ab  ")
x = Tag("abcd")
testResults["Tag constructor test 4"] = (x == "abcd")

# pass argument other than str, bytes or bytearray
try:
    Tag([0,1,0,0])
except OTCodecError:
    result = True
else:
    result = False
testResults["Tag invalid argument test 1"] = result

# Tag validations
testResults["Tag validation test 1"] = Tag.validateTag("abcd") == 0
testResults["Tag validation test 2"] = Tag.validateTag("abc") == 0x01
testResults["Tag validation test 3"] = Tag.validateTag("abcde") == 0x01
testResults["Tag validation test 4"] = Tag.validateTag("ab€c") == 0x02
testResults["Tag validation test 5"] = Tag.validateTag("ab c") == 0x04
testResults["Tag validation test 6"] = Tag.validateTag(" €c") == 0x07


# tests for Fixed

testResults["Fixed constants test 1"] = (Fixed._packedFormat == ">L")
testResults["Fixed constants test 2"] = (Fixed._packedSize == 4)
testResults["Fixed constants test 3"] = (Fixed._numPackedValues == 1)

# arg must be bytearray or bytes
try:
    Fixed(None)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed constructor test 1"] = result
try:
    Fixed(123)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed constructor test 2"] = result

# arg length must be 4 bytes
try:
    Fixed(b'\x00\x01')
except OTCodecError:
    result = True
else:
    result = False
try:
    Fixed(b'\x00\x01\x02\x03\x04')
except OTCodecError:
    result &= True
else:
    result &= False
testResults["Fixed constructor test 3"] = result

# good args
testResults["Fixed constructor test 4"] = (type(Fixed(bytearray([0,1,0,0]))) == Fixed)
testResults["Fixed constructor test 5"] = (type(Fixed(bytes(b'\xF0\x00\x80\x00'))) == Fixed)
testResults["Fixed constructor test 6"] = (Fixed(b'\xF0\x00\x80\x00') == -4095.5)

# Fixed.createFixedFromUint32: arg must be between 0 and 0xffff_ffff
try:
    Fixed.createFixedFromUint32(-1)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.createFixedFromUint32 test 1"] = result
try:
    Fixed.createFixedFromUint32(0x1_FFFF_FFFF)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.createFixedFromUint32 test 2"] = result

f = Fixed.createFixedFromUint32(0x0001_8000)
testResults["Fixed.createFixedFromUint32 test 3"] = (f == 1.5)
f = Fixed.createFixedFromUint32(0xF000_8000)
testResults["Fixed.createFixedFromUint32 test 4"] = (f == -4095.5)
f = Fixed.createFixedFromUint32(0x0001_5000)
testResults["Fixed.createFixedFromUint32 test 5"] = (f._rawBytes == bytes(b'\x00\x01\x50\x00'))

# Fixed.createFixedFromFloat
try:
    Fixed.createFixedFromFloat(-40000)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.createFixedFromFloat test 1"] = result
try:
    Fixed.createFixedFromFloat(40000)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.createFixedFromFloat test 2"] = result

f = Fixed.createFixedFromFloat(1.5)
testResults["Fixed.createFixedFromFloat test 3"] = (f._rawBytes == bytes(b'\x00\x01\x80\x00'))
f = Fixed.createFixedFromFloat(-4095.75)
testResults["Fixed.createFixedFromFloat test 4"] = (f._rawBytes == bytes(b'\xF0\x00\x40\x00'))
f = Fixed.createFixedFromFloat(1.3125)
testResults["Fixed.createFixedFromFloat test 5"] = (f._rawBytes == bytes(b'\x00\x01\x50\x00'))


# Fixed ==
f = Fixed(b'\xF0\x00\x80\x00')
testResults["Fixed __eq__ test 1"] = (Fixed(b'\xF0\x00\x80\x00') == f)
testResults["Fixed __eq__ test 2"] = (f == Fixed(b'\xF0\x00\x80\x00'))
testResults["Fixed __eq__ test 3"] = (f != Fixed(b'\x00\x00\x00\x00'))
testResults["Fixed __eq__ test 4"] = (f == bytearray(b'\xF0\x00\x80\x00'))
testResults["Fixed __eq__ test 5"] = (f == bytes(b'\xF0\x00\x80\x00'))
testResults["Fixed __eq__ test 6"] = (f == -4095.5)
f = Fixed(b'\xF0\x00\x00\x00')
testResults["Fixed __eq__ test 7"] = (f == -4096)
testResults["Fixed __eq__ test 8"] = (f == 0xF000_0000)

# Fixed misc
f = Fixed(b'\xF0\x00\x80\x00')
testResults["Fixed members test 1"] = (f.value == -4095.5)
testResults["Fixed members test 2"] = (f.mantissa == -4096)
testResults["Fixed members test 3"] = (f.fraction == 0x8000)
testResults["Fixed members test 4"] = (f.getFixedAsUint32() == 0xF0008000)
testResults["Fixed members test 5"] = (f.__str__() == "-4095.5")
testResults["Fixed members test 6"] = (f.__repr__() == "-4095.5")
f = Fixed(b'\x00\x02\x50\x00')
testResults["Fixed members test 8"] = (f.fixedTableVersion == 2.5)

# Fixed.tryReadFromBuffer: arg type must be bytearray or bytes
try:
    Fixed.tryReadFromBuffer(None)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.tryReadFromBuffer test 1"] = result
try:
    Fixed.tryReadFromBuffer(123)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.tryReadFromBuffer test 2"] = result

# Fixed.tryReadFromBuffer: returns None if buffer length != 4 bytes
testResults["Fixed.tryReadFromBuffer test 3"] = (Fixed.tryReadFromBuffer(b'\xF0\x00') == None)
testResults["Fixed.tryReadFromBuffer test 4"] = (Fixed.tryReadFromBuffer(b'\xF0\x00\x00\x00\x00') == None)

# Fixed.tryReadFromBuffer: good arg
testResults["Fixed.tryReadFromBuffer test 5"] = (Fixed.tryReadFromBuffer(b'\xF0\x00\x80\x00') == -4095.5)


# tests for Fixed.tryReadFromFile
testbio = BytesIO(testBytes1)
f = Fixed.tryReadFromFile(testbio)
testResults["Fixed.tryReadFromFile test 1"] = (type(f) == Fixed)
testResults["Fixed.tryReadFromFile test 2"] = (f.getFixedAsUint32() == 0x020F37DC)
f = Fixed.tryReadFromFile(testbio)
testResults["Fixed.tryReadFromFile test 3"] = (f.getFixedAsUint32() == 0x9AA20FE7)
testbio.seek(-1, 2) #from end of stream
try:
    f = Fixed.tryReadFromFile(testbio)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.tryReadFromFile test 4"] = result


# tests for F2Dot14

testResults["F2Dot14 constants test 1"] = (F2Dot14._packedFormat == ">H")
testResults["F2Dot14 constants test 2"] = (F2Dot14._packedSize == 2)
testResults["F2Dot14 constants test 3"] = (F2Dot14._numPackedValues == 1)

# arg must be bytearray or bytes
try:
    F2Dot14(None)
except OTCodecError:
    result = True
else:
    result = False
testResults["F2Dot14 constructor test 1"] = result
try:
    F2Dot14(123)
except OTCodecError:
    result = True
else:
    result = False
testResults["F2Dot14 constructor test 2"] = result

# arg length must be 2 bytes
try:
    F2Dot14(b'\x01')
except OTCodecError:
    result = True
else:
    result = False
try:
    F2Dot14(b'\x00\x01\x02')
except OTCodecError:
    result &= True
else:
    result &= False
testResults["F2Dot14 constructor test 3"] = result

# good args
testResults["F2Dot14 constructor test 4"] = (type(F2Dot14(bytearray([0,1]))) == F2Dot14)
testResults["F2Dot14 constructor test 5"] = (type(F2Dot14(bytes(b'\xF0\x00'))) == F2Dot14)
testResults["F2Dot14 constructor test 6"] = (F2Dot14(b'\xF0\x00') == -0.25)

# Fixed.createF2Dot14FromUint16: arg must be between 0 and 0xffff
try:
    F2Dot14.createF2Dot14FromUint16(-1)
except OTCodecError:
    result = True
else:
    result = False
testResults["F2Dot14.createF2Dot14FromUint16 test 1"] = result
try:
    F2Dot14.createF2Dot14FromUint16(0x1_0000)
except OTCodecError:
    result = True
else:
    result = False
testResults["F2Dot14.createF2Dot14FromUint16 test 2"] = result

f = F2Dot14.createF2Dot14FromUint16(0x6000)
testResults["F2Dot14.createF2Dot14FromUint16 test 3"] = (f == 1.5)
f = F2Dot14.createF2Dot14FromUint16(0xF000)
testResults["F2Dot14.createF2Dot14FromUint16 test 4"] = (f == -0.25)
f = F2Dot14.createF2Dot14FromUint16(0x3c01)
testResults["F2Dot14.createF2Dot14FromUint16 test 5"] = (f._rawBytes == bytes(b'\x3c\x01'))

# F2Dot14.createF2Dot14FromFloat
try:
    F2Dot14.createF2Dot14FromFloat(-4)
except OTCodecError:
    result = True
else:
    result = False
testResults["F2Dot14.createF2Dot14FromFloat test 1"] = result
try:
    F2Dot14.createF2Dot14FromFloat(4)
except OTCodecError:
    result = True
else:
    result = False
testResults["F2Dot14.createF2Dot14FromFloat test 2"] = result

f = F2Dot14.createF2Dot14FromFloat(1.5)
testResults["F2Dot14.createF2Dot14FromFloat test 3"] = (f._rawBytes == bytes(b'\x60\x00'))
f = F2Dot14.createF2Dot14FromFloat(-0.25)
testResults["F2Dot14.createF2Dot14FromFloat test 4"] = (f._rawBytes == bytes(b'\xF0\x00'))
f = F2Dot14.createF2Dot14FromFloat(1.3125)
testResults["F2Dot14.createF2Dot14FromFloat test 5"] = (f._rawBytes == bytes(b'\x54\x00'))

# F2Dot14 ==
f = F2Dot14(b'\xF0\x80')
testResults["F2Dot14 __eq__ test 1"] = (F2Dot14(b'\xF0\x80') == f)
testResults["F2Dot14 __eq__ test 2"] = (f == F2Dot14(b'\xF0\x80'))
testResults["F2Dot14 __eq__ test 3"] = (f != F2Dot14(b'\x00\x00'))
testResults["F2Dot14 __eq__ test 4"] = (f == bytearray(b'\xF0\x80'))
testResults["F2Dot14 __eq__ test 5"] = (f == bytes(b'\xF0\x80'))
testResults["F2Dot14 __eq__ test 6"] = (f == -0.2421875)

# F2Dot14 misc
f = F2Dot14(b'\xB0\x00')
testResults["F2Dot14 members test 1"] = (f.value == -1.25)
testResults["F2Dot14 members test 2"] = (f.mantissa == -2)
testResults["F2Dot14 members test 3"] = (f.fraction == 0x3000)
testResults["F2Dot14 members test 4"] = (f.getF2Dot14AsUint16() == 0xB000)
testResults["F2Dot14 members test 5"] = (f.__str__() == "-1.25")
testResults["F2Dot14 members test 6"] = (f.__repr__() == "-1.25")

# F2Dot14.tryReadFromBuffer: arg type must be bytearray or bytes
try:
    F2Dot14.tryReadFromBuffer(None)
except OTCodecError:
    result = True
else:
    result = False
testResults["F2Dot14.tryReadFromBuffer test 1"] = result
try:
    F2Dot14.tryReadFromBuffer(123)
except OTCodecError:
    result = True
else:
    result = False
testResults["F2Dot14.tryReadFromBuffer test 2"] = result

# F2Dot14.tryReadFromBuffer: returns None if buffer length != 2 bytes
testResults["F2Dot14.tryReadFromBuffer test 3"] = (F2Dot14.tryReadFromBuffer(b'\xF0') == None)
testResults["F2Dot14.tryReadFromBuffer test 4"] = (F2Dot14.tryReadFromBuffer(b'\xF0\x00\x00') == None)

# F2Dot14.tryReadFromBuffer: good arg
testResults["F2Dot14.tryReadFromBuffer test 5"] = (F2Dot14.tryReadFromBuffer(b'\xF0\x00') == -0.25)

# tests for F2Dot14.tryReadFromFile
testbio = BytesIO(testBytes1)
f = F2Dot14.tryReadFromFile(testbio)
testResults["F2Dot14.tryReadFromFile test 1"] = (type(f) == F2Dot14)
testResults["F2Dot14.tryReadFromFile test 2"] = (f.getF2Dot14AsUint16() == 0x020F)
f = F2Dot14.tryReadFromFile(testbio)
testResults["F2Dot14.tryReadFromFile test 3"] = (f.getF2Dot14AsUint16() == 0x37DC)
testbio.seek(-1, 2) #from end of stream
try:
    f = F2Dot14.tryReadFromFile(testbio)
except OTCodecError:
    result = True
else:
    result = False
testResults["F2Dot14.tryReadFromFile test 4"] = result



#-------------------------------------------------------------
# Tests for ot_types static functions
#-------------------------------------------------------------

# tests for concatFormatStrings
try:
    x = concatFormatStrings(None)
except:
    result = True
else:
    result = False
testResults["concatFormatStrings test 1"] = result
try:
    x = concatFormatStrings(42)
except:
    result = True
else:
    result = False
testResults["concatFormatStrings test 2"] = result
try:
    x = concatFormatStrings(42, "abc")
except:
    result = True
else:
    result = False
testResults["concatFormatStrings test 3"] = result
try:
    x = concatFormatStrings("abc", 42)
except:
    result = True
else:
    result = False
testResults["concatFormatStrings test 4"] = result
try:
    x = concatFormatStrings("abc", "def", 42, "ghi")
except:
    result = True
else:
    result = False
testResults["concatFormatStrings test 5"] = result
try:
    x = concatFormatStrings("@abc", "def")
except OTCodecError:
    result = True
else:
    result = False
testResults["concatFormatStrings test 6"] = result
try:
    x = concatFormatStrings(">abc", "@def")
except OTCodecError:
    result = True
else:
    result = False
testResults["concatFormatStrings test 7"] = result
try:
    x = concatFormatStrings(">abc", ">def", "@ghi")
except OTCodecError:
    result = True
else:
    result = False
testResults["concatFormatStrings test 8"] = result
testResults["concatFormatStrings test 9"] = (concatFormatStrings("abc") == "abc")
testResults["concatFormatStrings test 10"] = (concatFormatStrings(">abc", "def") == ">abcdef")
testResults["concatFormatStrings test 11"] = (concatFormatStrings(">abc", ">def") == ">abcdef")
testResults["concatFormatStrings test 12"] = (concatFormatStrings(">abc", ">def", "ghi") == ">abcdefghi")
testResults["concatFormatStrings test 13"] = (concatFormatStrings(">abc", ">def", ">ghi") == ">abcdefghi")


# tests for ot_types.createNewRecordsArray

recordsArray = createNewRecordsArray(4, ("foo", "bar"), (17, 42))
result = True
result &= (len(recordsArray) == 4)
result &= ("foo" in list(recordsArray[0]) and "bar" in list(recordsArray[1]))
result &= (recordsArray[2]["foo"] == 17 and recordsArray[3]["bar"] == 42)
testResults["createNewRecordsArray test"] = result


# tests for tryReadRecordsArrayFromBuffer

buffer = b'\x40\x00\x40'
numRecs = 5
fmt = ">hL"
fields = ("test1", "test2")
name = "Test"
try:
    x = tryReadRecordsArrayFromBuffer(buffer, numRecs, fmt, fields, name)
except OTCodecError:
    result = True
else:
    result = False
testResults["tryReadRecordsArrayFromBuffer test 1"] = result
buffer = b'\x40\x00\x40\x72\x00\x00\x80\x56\x00\x72\x00\x00\x40\x00\x40\x72\x00\x00\xfc\x09\x73\x72\x00\x00\x40\x00\x40\x72\x00\x00\x72\x8c\x85\x72\x32\x50'
x = tryReadRecordsArrayFromBuffer(buffer, numRecs, fmt, fields, name)
result = (type(x) == list and len(x) == 5 and type(x[0]) == dict and list(x[0]) == ["test1", "test2"])
testResults["tryReadRecordsArrayFromBuffer test 2"] = result
result = (x[0]["test1"] == 0x4000 and x[0]["test2"] == 0x4072_0000 and x[3]["test1"] == -1015 and x[3]["test2"] == 0x7372_0000)
testResults["tryReadRecordsArrayFromBuffer test 3"] = result


# tests for tryReadComplexRecordsArrayFromBuffer

class testRec_ReadCPRA:
    @staticmethod
    def interpretUnpackedValues(*args):
        # will receive ">hHHH"; reinterpret as (int32, Fixed)
        x, = struct.unpack(">l", struct.pack(">hH", *args[:2]))
        y = Fixed.createFixedFromUint32((args[2] << 16) + args[3])
        return x, y

buffer = b'\x40\x00\x40\x72\x00\x00\x80\x56'
numRecs = 3
fmt = ">hHHH"
fields = ("test1", "test2")
name = "Test"
try:
    x = tryReadComplexRecordsArrayFromBuffer(buffer, numRecs, fmt, fields, testRec_ReadCPRA, name)
except OTCodecError:
    result = True
else:
    result = False
testResults["tryReadComplexRecordsArrayFromBuffer test 1"] = result
buffer = b'\x40\x00\x40\x72\x00\x00\x80\x56\xC0\x00\x40\x32\xC0\x00\x40\x32\x40\x00\x40\x72\x00\x00\x80\x56\x7f\xff\x7f\xff\x7f\xff\x7f\xff'
x = tryReadComplexRecordsArrayFromBuffer(buffer, numRecs, fmt, fields, testRec_ReadCPRA, name)
result = (type(x) == list and len(x) == 3 and type(x[0]) == dict and len(x[0]) == len(fields) and list(x[0]) == list(fields))
testResults["tryReadComplexRecordsArrayFromBuffer test 2"] = result
result = (x[0]['test1'] == 0x40004072 and type(x[0]['test2']) == Fixed and x[0]['test2']._rawBytes == b'\x00\x00\x80\x56')
testResults["tryReadComplexRecordsArrayFromBuffer test 3"] = result
result = (x[1]['test1'] == -1073725390 and x[1]['test2']._rawBytes == b'\xC0\x00\x40\x32')
testResults["tryReadComplexRecordsArrayFromBuffer test 4"] = result


# tests for tryReadSubtablesFromBuffer



#-------------------------------------------------------------
# Tests for OTFile, TTCHeader
#-------------------------------------------------------------

# tests for OTFile constructor path validations
try:
    x = OTFile()
except OTCodecError:
    result = True
else:
    result = False
testResults["OTFile path test 1"] = result

try:
    x = OTFile("")
except OTCodecError:
    result = True
else:
    result = False
testResults["OTFile path test 2"] = result

try:
    x = OTFile("foo") # doesn't exist
except OTCodecError:
    result = True
else:
    result = False
testResults["OTFile path test 3"] = result

try:
    x = OTFile("TestData") # not a file
except OTCodecError:
    result = True
else:
    result = False
testResults["OTFile path test 4"] = result

testResults["OTFile path test 5"] = (selawk_file.path.name == r"selawk.ttf")

# tests for OTFile.IsSupportedSfntVersion
testResults["OTFile.IsSupportedSfntVersion test 1"] = (OTFile.isSupportedSfntVersion(b'\x00\x01\x00\x00') == True)
testResults["OTFile.IsSupportedSfntVersion test 2"] = (OTFile.isSupportedSfntVersion("OTTO") == True)
testResults["OTFile.IsSupportedSfntVersion test 3"] = (OTFile.isSupportedSfntVersion("true") == True)
testResults["OTFile.IsSupportedSfntVersion test 4"] = (OTFile.isSupportedSfntVersion("ttcf") == True)
testResults["OTFile.IsSupportedSfntVersion test 5"] = (OTFile.isSupportedSfntVersion("abcd") == False)


testResults["OTFile read test 1"] = (selawk_file.sfntVersion == b'\x00\x01\x00\x00')
testResults["OTFile read test 2"] = (selawk_file.numFonts == 1)
testResults["OTFile read test 3"] = (selawk_file.isCollection() == False)

testResults["OTFile read test 4"] = (sourceHansSans_file.sfntVersion == "ttcf")
testResults["OTFile read test 5"] = (sourceHansSans_file.numFonts == 10)
testResults["OTFile read test 6"] = (sourceHansSans_file.isCollection() == True)

ttchdr = sourceHansSans_file.ttcHeader
testResults["TTCHeader read test 1"] = (ttchdr.ttcTag == "ttcf")
testResults["TTCHeader read test 2"] = (ttchdr.majorVersion == 1)
testResults["TTCHeader read test 3"] = (ttchdr.minorVersion == 0)
testResults["TTCHeader read test 4"] = (ttchdr.numFonts == 10)




#-------------------------------------------------------------
# Tests for TableRecord, OffsetTable
#-------------------------------------------------------------


#-------------------------------------------------------------
# tests for TableRecord constructor
tr = TableRecord()
testResults["TableRecord() test 1"] = (type(tr) == TableRecord)
testResults["TableRecord() test 2"] = (tr.tableTag == None)
testResults["TableRecord() test 3"] = (tr.checkSum == 0)
testResults["TableRecord() test 4"] = (tr.offset == 0)
testResults["TableRecord() test 5"] = (tr.length == 0)

#-------------------------------------------------------------
# tests for TableRecord.createNewTableRecord
try:
    tr = TableRecord.createNewTableRecord(None) # table Tag required
except OTCodecError:
    result = True
else:
    result = False
testResults["TableRecord.createNewTableRecord test 1"] = result

tr = TableRecord.createNewTableRecord("abcd")
testResults["TableRecord.createNewTableRecord test 2"] = (type(tr) == TableRecord)
testResults["TableRecord.createNewTableRecord test 3"] = (tr.tableTag == "abcd")
testResults["TableRecord.createNewTableRecord test 4"] = (tr.checkSum == 0)
tr = TableRecord.createNewTableRecord("bcde", 42)
testResults["TableRecord.createNewTableRecord test 5"] = (tr.tableTag == "bcde")
testResults["TableRecord.createNewTableRecord test 6"] = (tr.checkSum == 42)
testResults["TableRecord.createNewTableRecord test 7"] = (tr.offset == 0)
tr = TableRecord.createNewTableRecord("cdef", 42, 43, 44)
testResults["TableRecord.createNewTableRecord test 8"] = (tr.tableTag == "cdef")
testResults["TableRecord.createNewTableRecord test 9"] = (tr.checkSum == 42)
testResults["TableRecord.createNewTableRecord test 10"] = (tr.offset == 43)
testResults["TableRecord.createNewTableRecord test 11"] = (tr.length == 44)

#-------------------------------------------------------------
# tests for TableRecord.tryReadFromBuffer
offtbl = selawk_file.fonts[0].offsetTable
tblrec = list(offtbl.tableRecords.values())[0]
testResults["TableRecord test 1"] = (tblrec.tableTag == "DSIG")
testResults["TableRecord test 2"] = (tblrec.checkSum == 0xF054_3E26)
testResults["TableRecord test 3"] = (tblrec.offset == 0x0000_91E4)
testResults["TableRecord test 4"] = (tblrec.length == 0x0000_1ADC)

tblrec = list(offtbl.tableRecords.values())[5]
testResults["TableRecord test 5"] = (tblrec.tableTag == "cmap")
testResults["TableRecord test 6"] = (tblrec.checkSum == 0x22F2_F74C)
testResults["TableRecord test 7"] = (tblrec.offset == 0x0000_0758)
testResults["TableRecord test 8"] = (tblrec.length == 0x0000_0606)

offtbl = sourceHansSans_file.fonts[0].offsetTable
tblrec = list(offtbl.tableRecords.values())[3]
testResults["TableRecord test 9"] = (tblrec.tableTag == "GPOS")
testResults["TableRecord test 10"] = (tblrec.checkSum == 0x0D16_AD78)
testResults["TableRecord test 11"] = (tblrec.offset == 0x00F8_CB20)
testResults["TableRecord test 12"] = (tblrec.length == 0x0000_B91A)


#-------------------------------------------------------------
# tests for OffsetTable constructor
ot = OffsetTable()
testResults["OffsetTable() test 1"] = (type(ot) == OffsetTable)
testResults["OffsetTable() test 2"] = (ot.sfntVersion == None)
testResults["OffsetTable() test 3"] = (ot.searchRange == 0)
testResults["OffsetTable() test 4"] = (ot.entrySelector == 0)
testResults["OffsetTable() test 5"] = (ot.rangeShift == 0)

#-------------------------------------------------------------
# tests for OffsetTable.createNewOffsetTable
try:
    ot = OffsetTable.createNewOffsetTable(None) # sfntVersion tag required
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.createNewOffsetTable test 1"] = result

try:
    ot = OffsetTable.createNewOffsetTable("cmap") # valid sfntVersion tag required
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.createNewOffsetTable test 2"] = result

ot = OffsetTable.createNewOffsetTable("true")
testResults["OffsetTable.createNewOffsetTable test 3"] = (type(ot) == OffsetTable)
testResults["OffsetTable.createNewOffsetTable test 4"] = (ot.sfntVersion == "true")
testResults["OffsetTable.createNewOffsetTable test 5"] = (ot.searchRange == 0)
ot = OffsetTable.createNewOffsetTable("true", 42)
testResults["OffsetTable.createNewOffsetTable test 6"] = (ot.sfntVersion == "true")
testResults["OffsetTable.createNewOffsetTable test 7"] = (ot.searchRange == 42)
testResults["OffsetTable.createNewOffsetTable test 8"] = (ot.entrySelector == 0)
ot = OffsetTable.createNewOffsetTable("true", 42, 43, 44)
testResults["OffsetTable.createNewOffsetTable test 9"] = (ot.sfntVersion == "true")
testResults["OffsetTable.createNewOffsetTable test 10"] = (ot.searchRange == 42)
testResults["OffsetTable.createNewOffsetTable test 11"] = (ot.entrySelector == 43)
testResults["OffsetTable.createNewOffsetTable test 12"] = (ot.rangeShift == 44)


#-------------------------------------------------------------
# tests for OffsetTable.tryReadFromFile

offtbl = selawk_file.fonts[0].offsetTable
testResults["OffsetTable test 1"] = (offtbl.offsetInFile == 0)
testResults["OffsetTable test 2"] = (offtbl.sfntVersion == b'\x00\x01\x00\x00')
testResults["OffsetTable test 3"] = (offtbl.numTables == 15)
testResults["OffsetTable test 4"] = (offtbl.searchRange == 0x80)
testResults["OffsetTable test 5"] = (offtbl.entrySelector == 0x03)
testResults["OffsetTable test 6"] = (offtbl.rangeShift == 0x70)

offtbl = sourceHansSans_file.fonts[0].offsetTable
testResults["OffsetTable test 7"] = (offtbl.offsetInFile == 0x34)
testResults["OffsetTable test 8"] = (offtbl.sfntVersion == "OTTO")
testResults["OffsetTable test 9"] = (offtbl.numTables == 16)
testResults["OffsetTable test 10"] = (offtbl.searchRange == 0x0100)
testResults["OffsetTable test 11"] = (offtbl.entrySelector == 0x0004)
testResults["OffsetTable test 12"] = (offtbl.rangeShift == 0x0000)

offtbl = sourceHansSans_file.fonts[1].offsetTable
testResults["OffsetTable test 13"] = (offtbl.offsetInFile == 0x140)
testResults["OffsetTable test 14"] = (offtbl.sfntVersion == "OTTO")
testResults["OffsetTable test 15"] = (offtbl.numTables == 16)
testResults["OffsetTable test 16"] = (offtbl.searchRange == 0x100)
testResults["OffsetTable test 17"] = (offtbl.entrySelector == 0x04)
testResults["OffsetTable test 18"] = (offtbl.rangeShift == 0x00)


#-------------------------------------------------------------
# tests for OffsetTable methods: tryGet, add, remove TR

# tryGetTableRecord
offtbl = selawk_file.fonts[0].offsetTable
testResults["OffsetTable.TryGetTableRecord test 1"] = (type(offtbl.tryGetTableRecord("cmap")) == TableRecord)
testResults["OffsetTable.TryGetTableRecord test 2"] = (offtbl.tryGetTableRecord("zzzz") == None)


# tests for OffsetTable.AddTableRecord
ot = OffsetTable.createNewOffsetTable("true", 42, 43, 44)
try:
    ot.addTableRecord(None) # TableRecord object required
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.addTableRecord test 1"] = result

tr = TableRecord()
try:
    ot.addTableRecord(tr) # TableRecord with table record Tag required
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.addTableRecord test 2"] = result

tr = TableRecord.createNewTableRecord("abcd", 42)
assert(len(ot.tableRecords) == 0)
ot.addTableRecord(tr)
testResults["OffsetTable.addTableRecord test 3"] = (len(ot.tableRecords) == 1)
testResults["OffsetTable.addTableRecord test 4"] = (ot.tableRecords["abcd"].checkSum == 42)
tr = TableRecord.createNewTableRecord("abcd", 43)
ot.addTableRecord(tr) # duplicate table tag: replaces existing TableRecord
testResults["OffsetTable.addTableRecord test 5"] = (len(ot.tableRecords) == 1)
testResults["OffsetTable.addTableRecord test 6"] = (ot.tableRecords["abcd"].checkSum == 43)

# can't add table record to OffsetTable read from file
try:
    selawk_file.fonts[0].offsetTable.addTableRecord(tr)
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.AddTableRecord test 7"] = result

# TableRecord read from file can be added to a new OffsetTable
tr = selawk_file.fonts[0].offsetTable.tableRecords["cmap"]
ot.addTableRecord(tr)
testResults["OffsetTable.AddTableRecord test 8"] = (len(ot.tableRecords) == 2)
testResults["OffsetTable.AddTableRecord test 9"] = (ot.tableRecords["cmap"].checkSum == 0x22F2_F74C)

# tests for OffsetTable.removeTableRecord
ot = OffsetTable.createNewOffsetTable("OTTO")
tr = TableRecord.createNewTableRecord("cmap")
ot.addTableRecord(tr)
tr = TableRecord.createNewTableRecord("glyf", 42)
ot.addTableRecord(tr)
assert(len(ot.tableRecords) == 2)
assert(ot.tryGetTableRecord("cmap") is not None)

# specified TableRecord is removed, other TableRecord not affected
ot.removeTableRecord("cmap")
testResults["OffsetTable.removeTableRecord test 1"] = (len(ot.tableRecords) == 1)
testResults["OffsetTable.removeTableRecord test 2"] = (ot.tryGetTableRecord("cmap") == None)
testResults["OffsetTable.removeTableRecord test 3"] = (ot.tryGetTableRecord("glyf").checkSum == 42)

# None is no-op
try:
    ot.removeTableRecord(None)
except Exception:
    result = False
else:
    result = True
testResults["OffsetTable.removeTableRecord test 4"] = result

# request to remove TableRecord that's not present is no-op
try:
    ot.removeTableRecord("GPOS")
except Exception:
    result = False
else:
    result = True
testResults["OffsetTable.removeTableRecord test 5"] = result

# Can't attempt to remove OffsetTable read from file, even if None is passed
try:
    selawk_file.fonts[0].offsetTable.removeTableRecord(None)
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.removeTableRecord test 6"] = result

# can't remove TableRecord from OffsetTable read from file
try:
    selawk_file.fonts[0].offsetTable.removeTableRecord("cmap")
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.removeTableRecord test 7"] = result

# even if not present, can't try to remove TableRecord from OffsetTable read from file
try:
    selawk_file.fonts[0].offsetTable.removeTableRecord("zzzz")
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.removeTableRecord test 8"] = result




#-------------------------------------------------------------
#-------------------------------------------------------------

# tests for OTFont.IsSupportedSfntVersion
testResults["OTFont.IsSupportedSfntVersion test 1"] = (OTFont.isSupportedSfntVersion(b'\x00\x01\x00\x00') == True)
testResults["OTFont.IsSupportedSfntVersion test 2"] = (OTFont.isSupportedSfntVersion("OTTO") == True)
testResults["OTFont.IsSupportedSfntVersion test 3"] = (OTFont.isSupportedSfntVersion("true") == True)
testResults["OTFont.IsSupportedSfntVersion test 4"] = (OTFont.isSupportedSfntVersion("ttcf") == False)
testResults["OTFont.IsSupportedSfntVersion test 5"] = (OTFont.isSupportedSfntVersion("abcd") == False)

# tests for OTFont.IsKnownTableType
testResults["OTFont.IsKnownTableType test 1"] = (OTFont.isKnownTableType("CBDT") == True)
testResults["OTFont.IsKnownTableType test 2"] = (OTFont.isKnownTableType("bdat") == True)
testResults["OTFont.IsKnownTableType test 3"] = (OTFont.isKnownTableType("Gloc") == True)
testResults["OTFont.IsKnownTableType test 4"] = (OTFont.isKnownTableType("TSI2") == True)
testResults["OTFont.IsKnownTableType test 5"] = (OTFont.isKnownTableType("zzzz") == False)

# tests for OTFont.IsSupportedTableType
testResults["OTFont.IsSupportedTableType test 1"] = (OTFont.isSupportedTableType("zzzz") == False)
testResults["OTFont.IsSupportedTableType test 2"] = (OTFont.isSupportedTableType("hhea") == True)



font = selawk_file.fonts[0]
testResults["OTFont read test 1"] = (font.offsetInFile == 0)
testResults["OTFont read test 2"] = (font.sfntVersionTag() == b'\x00\x01\x00\x00')
testResults["OTFont read test 3"] = (font.ttcIndex == None)
testResults["OTFont read test 4"] = (font.isWithinTtc == False)
testResults["OTFont read test 5"] = (font.defaultLabel == "selawk.ttf")

testResults["OTFont.ContainsTable test 1"] = (font.containsTable("cmap") == True)
testResults["OTFont.ContainsTable test 2"] = (font.containsTable("GPOS") == True)
testResults["OTFont.ContainsTable test 3"] = (font.containsTable("avar") == False)

testResults["OTFont.TryGetTableOffset test 1"] = (font.tryGetTableOffset("cmap") == 0x0758)
testResults["OTFont.TryGetTableOffset test 2"] = (font.tryGetTableOffset("zzzz") == None)





# tests for OTFile, TTCHeader, OTFont using SourceHanSans-Regular.TTC

font = sourceHansSans_file.fonts[0]
testResults["OTFont read test 6"] = (font.offsetInFile == 0x34)
testResults["OTFont read test 7"] = (font.sfntVersionTag() == "OTTO")
testResults["OTFont read test 8"] = (font.ttcIndex == 0)
testResults["OTFont read test 9"] = (font.isWithinTtc == True)
testResults["OTFont read test 10"] = (font.defaultLabel == "SourceHanSans-Regular.TTC:0")


font = sourceHansSans_file.fonts[1]
testResults["OTFont read test 11"] = (font.offsetInFile == 0x0140)
testResults["OTFont read test 12"] = (font.sfntVersionTag() == "OTTO")
testResults["OTFont read test 13"] = (font.ttcIndex == 1)
testResults["OTFont read test 14"] = (font.isWithinTtc == True)
testResults["OTFont read test 15"] = (font.defaultLabel == "SourceHanSans-Regular.TTC:1")




#-------------------------------------------------------------
# tests for table_hhea
#-------------------------------------------------------------

hhea = Table_hhea()
testResults["Table_hhea constructor test 1"] = (type(hhea) == Table_hhea)
testResults["Table_hhea constructor test 2"] = (hhea.tableTag == "hhea")
testResults["Table_hhea constructor test 3"] = (not hasattr(hhea, "ascender"))

hhea = Table_hhea.createNew_hhea()
testResults["Table_hhea.createNew_hhea test 1"] = (type(hhea) == Table_hhea)

# check default values
result = True
expected = zip(Table_hhea._hhea_1_0_fields, Table_hhea._hhea_1_0_defaults)
for k, v in expected:
    val = getattr(hhea, k)
    if val != v:
        result = False
        break
testResults["Table_hhea.createNew_hhea test 2"] = result

# test Table_hhea.tryReadFromFile using selawk.ttf
try:
    hhea = selawk_file.fonts[0].tables["hhea"]
except Exception:
    result = False
else:
    result = True
testResults["Table_hhea.tryReadFromFile test 1"] = result
testResults["Table_hhea.tryReadFromFile test 2"] = (type(hhea) == Table_hhea)
selawk_hhea_values = [1, 0, 2027, -431, 0, 2478, -800, -1426, 2402, 1, 0, 0, 0, 0, 0, 0, 0, 352]
result = True
expected = zip(Table_hhea._hhea_1_0_fields, selawk_hhea_values)
for k, v in expected:
    val = getattr(hhea, k)
    if val != v:
        result = False
        break
testResults["Table_hhea.tryReadFromFile test 3"] = result
tr = selawk_file.fonts[0].offsetTable.tryGetTableRecord("hhea")
testResults["Table_hhea.tryReadFromFile test 4"] = (hhea.calculatedCheckSum == tr.checkSum)

# test tryReadFromFile using SourceHanSans-Regular.TTC
try:
    hhea = sourceHansSans_file.fonts[0].tables["hhea"]
except Exception:
    result = False
else:
    result = True
testResults["Table_hhea.tryReadFromFile test 5"] = result
testResults["Table_hhea.tryReadFromFile test 6"] = (type(hhea) == Table_hhea)
sourcehansans_0_hhea_values = [1, 0, 0x0488, -288, 0, 3000, -1002, -551, 2928, 1, 0, 0, 0, 0, 0, 0, 0, 0xFFFB]
result = True
expected = zip(Table_hhea._hhea_1_0_fields, sourcehansans_0_hhea_values)
for k, v in expected:
    val = getattr(hhea, k)
    if val != v:
        result = False
        break
testResults["Table_hhea.tryReadFromFile test 7"] = result
tr = sourceHansSans_file.fonts[0].offsetTable.tryGetTableRecord("hhea")
testResults["Table_hhea.tryReadFromFile test 8"] = (hhea.calculatedCheckSum == tr.checkSum)


# test tryReadFromFile offset/length checks
tr_s = selawk_file.fonts[0].offsetTable.tryGetTableRecord("hhea")

# offset out of bounds:
tr = TableRecord.createNewTableRecord("hhea", tr_s.checkSum, 0x7FFF_FFFF, tr_s.length)
try:
    hhea = Table_hhea.tryReadFromFile(selawk_file.fonts[0], tr)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_hhea.tryReadFromFile test 9"] = result

# length out of bounds:
tr = TableRecord.createNewTableRecord("hhea", tr_s.checkSum, tr_s.offset, 0x7FFF_FFFF)
try:
    hhea = Table_hhea.tryReadFromFile(selawk_file.fonts[0], tr)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_hhea.tryReadFromFile test 10"] = result

# wrong length:
tr = TableRecord.createNewTableRecord("hhea", tr_s.checkSum, tr_s.offset, tr_s.length + 1)
try:
    hhea = Table_hhea.tryReadFromFile(selawk_file.fonts[0], tr)
except Exception:
    result = True
else:
    result = False
testResults["Table_hhea.tryReadFromFile test 11"] = result




#-------------------------------------------------------------
# tests for table_maxp
#-------------------------------------------------------------

maxp = Table_maxp()
testResults["Table_maxp constructor test 1"] = (type(maxp) == Table_maxp)
testResults["Table_maxp constructor test 2"] = (maxp.tableTag == "maxp")
testResults["Table_maxp constructor test 3"] = (not hasattr(maxp, "version"))

# createNew_maxp: check default values for v0.5
maxp = Table_maxp.createNew_maxp(0.5)
testResults["Table_maxp.createNew_maxp test 1"] = (type(maxp) == Table_maxp)
result = True
expected = zip(Table_maxp._maxp_0_5_fields, [Fixed.createFixedFromUint32(0x0000_5000), 0])
for k, v in expected:
    val = getattr(maxp, k)
    if val != v:
        result = False
        break
testResults["Table_maxp.createNew_maxp test 2"] = result
testResults["Table_maxp.createNew_maxp test 3"] = (not hasattr(maxp, "maxPoints"))

# createNew_maxp: check default values for v1.0
maxp = Table_maxp.createNew_maxp(1.0)
testResults["Table_maxp.createNew_maxp test 4"] = (type(maxp) == Table_maxp)
result = True
expected = zip(Table_maxp._maxp_0_5_fields, [Fixed.createFixedFromUint32(0x0001_0000), 0])
for k, v in expected:
    val = getattr(maxp, k)
    if val != v:
        result = False
        break
testResults["Table_maxp.createNew_maxp test 5"] = result
result = True
expected = zip(Table_maxp._maxp_1_0_addl_fields, Table_maxp._maxp_1_0_addl_defaults)
for k, v in expected:
    val = getattr(maxp, k)
    if val != v:
        result = False
        break
testResults["Table_maxp.createNew_maxp test 6"] = result

# test Table_maxp.tryReadFromFile using selawk.ttf
try:
    maxp = selawk_file.fonts[0].tables["maxp"]
except Exception:
    result = False
else:
    result = True
testResults["Table_maxp.tryReadFromFile test 1"] = result
testResults["Table_maxp.tryReadFromFile test 2"] = (type(maxp) == Table_maxp)
selawk_maxp_values = [1, 0x0160, 0x64, 7, 0x4d, 4, 0, 0, 0, 1, 0, 0, 0, 3, 1]
result = True
expected = zip(Table_maxp._maxp_1_0_all_fields, selawk_maxp_values)
for k, v in expected:
    val = getattr(maxp, k)
    if val != v:
        result = False
        break
testResults["Table_maxp.tryReadFromFile test 3"] = result
tr = selawk_file.fonts[0].offsetTable.tryGetTableRecord("maxp")
testResults["Table_maxp.tryReadFromFile test 4"] = (maxp.calculatedCheckSum == tr.checkSum)




#-------------------------------------------------------------
# tests for table_fmtx
#-------------------------------------------------------------

fmtx = Table_fmtx()
testResults["Table_fmtx constructor test 1"] = (type(fmtx) == Table_fmtx)
testResults["Table_fmtx constructor test 2"] = (fmtx.tableTag == "fmtx")
testResults["Table_fmtx constructor test 3"] = (not hasattr(fmtx, "version"))

# createNew_fmtx: check default values
fmtx = Table_fmtx.createNew_fmtx()
testResults["Table_fmtx.createNew_fmtx test 1"] = (type(fmtx) == Table_fmtx)
result = True
expected = zip(Table_fmtx._fmtx_2_0_fields, Table_fmtx._fmtx_2_0_defaults)
for k, v in expected:
    val = getattr(fmtx, k)
    if val != v:
        result = False
        break
testResults["Table_fmtx.createNew_fmtx test 2"] = result

# test Table_fmtx.tryReadFromFile using skia.ttf -- if present
try:
    font = OTFile(r"TestData\Skia.ttf").fonts[0]
except Exception:
    skippedTests.append("Table_fmtx.tryReadFromFile using skia.ttf")
else:
    try:
        fmtx = font.tables["fmtx"]
    except Exception:
        result = False
    else:
        result = True
testResults["Table_fmtx.tryReadFromFile test 1"] = result
testResults["Table_fmtx.tryReadFromFile test 2"] = (type(fmtx) == Table_fmtx)
skia_fmtx_values = [b'\x00\x02\x00\x00', 0x0238, 0, 1, 3, 2, 4, 5, 7, 6]
result = True
expected = zip(Table_fmtx._fmtx_2_0_fields, skia_fmtx_values)
for k, v in expected:
    val = getattr(fmtx, k)
    if val != v:
        result = False
        break
testResults["Table_fmtx.tryReadFromFile test 3"] = result



#-------------------------------------------------------------
# tests for table_COLR
#-------------------------------------------------------------

# test BaseGlyphRecordsArray.createNew_BaseGlyphRecordsArray
recArray = BaseGlyphRecordsArray.createNew_BaseGlyphRecordsArray(4)
result = True
result &= (len(recArray) == 4)
record = recArray[0]
result &= (len(record) == 3)
keys = list(record)
result &= ("glyphID" in keys and "firstLayerIndex" in keys and "numLayers" in keys)
result &= (record["glyphID"] == 0 and record["firstLayerIndex"] == 0 and record["numLayers"] == 0)
testResults["BaseGlyphRecordsArray.createNew test"] = result

# test LayerRecordsArray.createNew_LayerRecordsArray
recArray = LayerRecordsArray.createNew_layerRecordsArray(4)
result = True
result &= (len(recArray) == 4)
record = recArray[0]
result &= (len(record) == 2)
keys = list(record)
result &= ("glyphID" in keys and "paletteIndex" in keys)
result &= (record["glyphID"] == 0 and record["paletteIndex"] == 0)
testResults["LayerRecordsArray.createNew test"] = result

# test COLR constructor
colr = Table_COLR()
testResults["Table_COLR constructor test 1"] = (type(colr) == Table_COLR)
testResults["Table_COLR constructor test 2"] = (colr.tableTag == "COLR")
testResults["Table_COLR constructor test 3"] = (not hasattr(colr, "version"))

# createNew_COLR: check default values for version 0
colr = Table_COLR.createNew_COLR(0)
testResults["Table_COLR.createNew_COLR test 1"] = (type(colr) == Table_COLR)
result = True
expected = zip(Table_COLR._colr_0_fields, Table_COLR._colr_0_defaults)
for k, v in expected:
    val = getattr(colr, k)
    if val != v:
        result = False
        break
testResults["Table_COLR.createNew_COLR test 2"] = result

# createNew_COLR: check default values for version 1
colr = Table_COLR.createNew_COLR(1)
testResults["Table_COLR.createNew_COLR test 3"] = (type(colr) == Table_COLR)
result = True
expected = zip(Table_COLR._colr_1_all_fields, Table_COLR._colr_1_all_defaults)
for k, v in expected:
    val = getattr(colr, k)
    if val != v:
        result = False
        break
testResults["Table_COLR.createNew_COLR test 4"] = result

# test Table_COLR.tryReadFromFile using BungeeColor-Regular_colr_Windows.ttf
try:
    colr = bungeeColor_file.fonts[0].tables["COLR"]
except Exception:
    result = False
else:
    result = True
testResults["Table_COLR.tryReadFromFile test 1"] = result
testResults["Table_COLR.tryReadFromFile test 2"] = (type(colr) == Table_COLR)
bungeeColor_COLR_headerValues = (0, 288, 14, 1742, 576)
result = True
expected = zip(Table_COLR._colr_0_fields, bungeeColor_COLR_headerValues)
for k, v in expected:
    val = getattr(colr, k)
    if val != v:
        result = False
        break
testResults["Table_COLR.tryReadFromFile test 3"] = result
recordsArray = colr.baseGlyphRecords
testResults["Table_COLR.tryReadFromFile test 4"] = (len(recordsArray) == 288)
record = recordsArray[3]
keys = list(record)
result = (len(record) == 3)
result &= ("glyphID" in keys and "firstLayerIndex" in keys and "numLayers" in keys)
testResults["Table_COLR.tryReadFromFile test 5"] = result
result = (record["glyphID"] == 3 and record["firstLayerIndex"] == 6 and record["numLayers"] == 2)
testResults["Table_COLR.tryReadFromFile test 6"] = result
record = recordsArray[174]
result = (record["glyphID"] == 174 and record["firstLayerIndex"] == 348 and record["numLayers"] == 2)
testResults["Table_COLR.tryReadFromFile test 7"] = result
recordsArray = colr.layerRecords
testResults["Table_COLR.tryReadFromFile test 8"] = (len(recordsArray) == 576)
record = recordsArray[6]
keys = list(record)
result = (len(record) == 2)
result &= ("glyphID" in keys and "paletteIndex" in keys)
testResults["Table_COLR.tryReadFromFile test 9"] = result
result = (record["glyphID"] == 452 and record["paletteIndex"] == 0)
testResults["Table_COLR.tryReadFromFile test 10"] = result
record = recordsArray[401]
result = (record["glyphID"] == 451 and record["paletteIndex"] == 1)
testResults["Table_COLR.tryReadFromFile test 11"] = result


# tests for VarFixed, VarF2Dot14

testResults["Table_COLR VarFixed constants test 1"] = (VarFixed._packedFormat == (Fixed._packedFormat + "2H"))
testResults["Table_COLR VarFixed constants test 2"] = (VarFixed._packedSize == 8)
testResults["Table_COLR VarFixed constants test 3"] = (VarFixed._fieldNames == ("value", "varOuterIndex", "varInnerIndex"))
testResults["Table_COLR VarFixed constants test 4"] = (VarFixed._numPackedValues == 3)
try:
    x = VarFixed(0x1_8000, 4, 7)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFixed constructor test 1"] = result
try:
    x = VarFixed(Fixed.createFixedFromUint32(0x48000), -17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFixed constructor test 2"] = result
try:
    x = VarFixed(Fixed.createFixedFromUint32(0x48000), 17, -23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFixed constructor test 3"] = result
x = VarFixed(Fixed.createFixedFromUint32(0x48000),1,3)
testResults["Table_COLR VarFixed constructor test 4"] = (type(x.value) == Fixed and type(x.varOuterIndex) == int and type(x.varInnerIndex) == int)
testResults["Table_COLR VarFixed constructor test 5"] = (x.value == 4.5 and x.varOuterIndex == 1 and x.varInnerIndex == 3)
result = x.__repr__() == "{'value': 4.5, 'varOuterIndex': 1, 'varInnerIndex': 3}"
testResults["Table_COLR VarFixed __repr__ test"] = result
x = VarFixed.interpretUnpackedValues(0x1_8000, 4, 7)
testResults["Table_COLR VarFixed interpretUnpackedValues test 1"] = (len(x) == 3 and type(x[0]) == Fixed and type(x[1]) == int and type(x[2]) == int)
testResults["Table_COLR VarFixed interpretUnpackedValues test 2"] = (x[0]._rawBytes == b'\x00\x01\x80\x00' and x[1] == 4 and x[2] == 7)
x = VarFixed(*VarFixed.interpretUnpackedValues(0x1_8000, 4, 7))
testResults["Table_COLR VarFixed interpretUnpackedValues test 3"] = (type(x) == VarFixed and x.value._rawBytes == b'\x00\x01\x80\x00' and x.varOuterIndex == 4 and x.varInnerIndex == 7)

testResults["Table_COLR VarF2Dot14 constants test 1"] = (VarF2Dot14._packedFormat == (F2Dot14._packedFormat + "2H"))
testResults["Table_COLR VarF2Dot14 constants test 2"] = (VarF2Dot14._packedSize == 6)
testResults["Table_COLR VarF2Dot14 constants test 3"] = (VarF2Dot14._fieldNames == ("value", "varOuterIndex", "varInnerIndex"))
testResults["Table_COLR VarF2Dot14 constants test 4"] = (VarF2Dot14._numPackedValues == 3)
try:
    x = VarF2Dot14(0x6000, 4, 7)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarF2Dot14 constructor test 1"] = result
try:
    x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), -17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarF2Dot14 constructor test 2"] = result
try:
    x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), 17, -23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarF2Dot14 constructor test 3"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), 1, 3)
testResults["Table_COLR VarF2Dot14 constructor test 4"] = (type(x.value) == F2Dot14 and type(x.varOuterIndex) == int and type(x.varInnerIndex) == int)
testResults["Table_COLR VarF2Dot14 constructor test 5"] = (x.value == 1.5 and x.varOuterIndex == 1 and x.varInnerIndex == 3)
result = x.__repr__() == "{'value': 1.5, 'varOuterIndex': 1, 'varInnerIndex': 3}"
testResults["Table_COLR VarF2Dot14 __repr__ test"] = result
x = VarF2Dot14.interpretUnpackedValues(0x7000, 4, 7)
testResults["Table_COLR VarF2Dot14 interpretUnpackedValues test 1"] = (len(x) == 3 and type(x[0]) == F2Dot14 and type(x[1]) == int and type(x[2]) == int)
testResults["Table_COLR VarF2Dot14 interpretUnpackedValues test 2"] = (x[0]._rawBytes == b'\x70\x00' and x[1] == 4 and x[2] == 7)
x = VarF2Dot14(*VarF2Dot14.interpretUnpackedValues(0x7000, 4, 7))
testResults["Table_COLR VarF2Dot14 interpretUnpackedValues test 3"] = (type(x) == VarF2Dot14 and x.value._rawBytes == b'\x70\x00' and x.varOuterIndex == 4 and x.varInnerIndex == 7)

# tests for VarFWord, VarUFWord
testResults["Table_COLR VarFWord constants test 1"] = (VarFWord._packedFormat == ">h2H")
testResults["Table_COLR VarFWord constants test 2"] = (VarFWord._packedSize == 6)
testResults["Table_COLR VarFWord constants test 3"] = (VarFWord._fieldNames == ("coordinate", "varOuterIndex", "varInnerIndex"))
testResults["Table_COLR VarFWord constants test 4"] = (VarFWord._numPackedValues == 3)
x = VarFWord(-24, 17, 23)
testResults["Table_COLR VarFWord constructor test 1"] = (type(x) == VarFWord and type(x.coordinate) == int and type(x.varOuterIndex) == int and type(x.varInnerIndex) == int)
testResults["Table_COLR VarFWord constructor test 2"] = (x.coordinate == -24 and x.varOuterIndex == 17 and x.varInnerIndex == 23)
try:
    x = VarFWord(24, -17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFWord constructor test 3"] = result
try:
    x = VarFWord(24, 17, -23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFWord constructor test 4"] = result
testResults["Table_COLR VarFWord __repr__ test"] = (x.__repr__() == "{'coordinate': -24, 'varOuterIndex': 17, 'varInnerIndex': 23}")

testResults["Table_COLR VarUFWord constants test 1"] = (VarUFWord._packedFormat == ">3H")
testResults["Table_COLR VarUFWord constants test 2"] = (VarUFWord._packedSize == 6)
testResults["Table_COLR VarUFWord constants test 3"] = (VarUFWord._fieldNames == ("distance", "varOuterIndex", "varInnerIndex"))
testResults["Table_COLR VarUFWord constants test 4"] = (VarUFWord._numPackedValues == 3)
x = VarUFWord(24, 17, 23)
testResults["Table_COLR VarUFWord constructor test 1"] = (type(x) == VarUFWord and type(x.distance) == int and type(x.varOuterIndex) == int and type(x.varInnerIndex) == int)
testResults["Table_COLR VarUFWord constructor test 2"] = (x.distance == 24 and x.varOuterIndex == 17 and x.varInnerIndex == 23)
try:
    x = VarUFWord(-24, 17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarUFWord constructor test 3"] = result
try:
    x = VarUFWord(24, -17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarUFWord constructor test 4"] = result
try:
    x = VarUFWord(24, 17, -23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarUFWord constructor test 5"] = result
testResults["Table_COLR VarUFWord __repr__ test"] = (x.__repr__() == "{'distance': 24, 'varOuterIndex': 17, 'varInnerIndex': 23}")


# tests for ColorIndex

testResults["ColorIndex constants test 1"] = (ColorIndex._packedFormat == ">HH2H")
testResults["ColorIndex constants test 2"] = (ColorIndex._packedSize == 8)
testResults["ColorIndex constants test 3"] = (ColorIndex._fieldNames == ("paletteIndex", "alpha"))
testResults["ColorIndex constants test 4"] = (ColorIndex._numPackedValues == 4)

# constructor tests -- arg validations
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
try:
    y = ColorIndex(-24, x)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 1"] = result
try:
    y = ColorIndex(24, 42)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 2"] = result

# alpha out of range [0, 1]
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), 1, 3)
try:
    y = ColorIndex(24, x)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 2"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x8000), 1, 3)
try:
    y = ColorIndex(24, x)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 3"] = result

# good args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
y = ColorIndex(24, x)
testResults["Table_COLR ColorIndex constructor test 5"] = (type(y.paletteIndex) == int and type(y.alpha) == VarF2Dot14)
testResults["Table_COLR ColorIndex test constructor 6"] = (y.paletteIndex == 24 and y.alpha.value == 0.75 and y.alpha.varOuterIndex == 1 and y.alpha.varInnerIndex == 3)

x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
y = ColorIndex(24, x)
result = y.__repr__() == "{'paletteIndex': 24, 'alpha': {'value': 0.75, 'varOuterIndex': 1, 'varInnerIndex': 3}}"
testResults["Table_COLR ColorIndex __repr__ test"] = result

x = ColorIndex.interpretUnpackedValues(17, 0xC000, 3, 5)
result = (len(x) == 2 and type(x[0]) == int and type(x[1]) == VarF2Dot14)
testResults["Table_COLR ColorIndex interpretUnpackedValues test 1"] = result
x = ColorIndex(*ColorIndex.interpretUnpackedValues(17, 0x3000, 3, 5))
result = (type(x) == ColorIndex and x.paletteIndex == 17 and x.alpha.value.value == 0.75 and x.alpha.varOuterIndex == 3 and x.alpha.varInnerIndex == 5)
testResults["Table_COLR ColorIndex interpretUnpackedValues test 2"] = result


# tests for ColorStop

testResults["ColorStop constants test 1"] = (ColorStop._packedFormat == ">H2HHH2H")
testResults["ColorStop constants test 2"] = (ColorStop._packedSize == 14)
testResults["ColorStop constants test 3"] = (ColorStop._fieldNames == ("stopOffset", "color"))
testResults["ColorStop constants test 4"] = (ColorStop._numPackedValues == 7)

# arg validations
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x1000), 1, 3)
y = ColorIndex(24, x)
try:
    z = ColorStop(24, y)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 1"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
try:
    z = ColorStop(x, 24)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 2"] = result

# stopOffset out of range [0, 1]
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
y = ColorIndex(24, x)
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x4001), 1, 3)
try:
    z = ColorStop(x, y)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 3"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
y = ColorIndex(24, x)
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0xC001), 1, 3)
try:
    z = ColorStop(x, y)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 4"] = result

# good args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x1000), 1, 3)
y = ColorIndex(24, x)
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 0, 4)
z = ColorStop(x, y)
testResults["Table_COLR ColorStop constructor test 5"] = (type(z.stopOffset) == VarF2Dot14 and type(z.color) == ColorIndex)
testResults["Table_COLR ColorStop constructor test 6"] = (z.stopOffset.value == 0.75 and z.stopOffset.varOuterIndex == 0 and z.stopOffset.varInnerIndex == 4)
testResults["Table_COLR ColorStop constructor test 7"] = (z.color.paletteIndex == 24 and z.color.alpha.value == 0.25 and z.color.alpha.varOuterIndex == 1 and y.alpha.varInnerIndex == 3)
result = z.__repr__() == "{'stopOffset': {'value': 0.75, 'varOuterIndex': 0, 'varInnerIndex': 4}, 'color': {'paletteIndex': 24, 'alpha': {'value': 0.25, 'varOuterIndex': 1, 'varInnerIndex': 3}}}"
testResults["Table_COLR ColorStop __repr__ test"] = result

#interpretUnpackedValues
x = ColorStop.interpretUnpackedValues(0x3000, 0, 4, 24, 0x1000, 1, 3)
result = (len(x) == 2 and type(x[0]) == VarF2Dot14 and type(x[1]) == ColorIndex)
testResults["Table_COLR ColorStop interpretUnpackedValues test 1"] = result
x = ColorStop(*ColorStop.interpretUnpackedValues(0x3000, 0, 4, 24, 0x1000, 1, 3))
result = (type(x) == ColorStop and x.stopOffset.value.value == 0.75 and x.color.paletteIndex == 24)
testResults["Table_COLR ColorStop interpretUnpackedValues test 2"] = result


"""
Still need tests for
    - ColorLine
    - Affine2x2
    - PaintFormat1
    - PaintFormat2
    - PaintFormat3
    - tryReadSubtablesFromBuffer
    - tryReadMultiFormatSubtablesFromBuffer
    - LayersV1
    - BaseGlyphV1List
    - COLR V1
"""

f = notoHW_COLR1_rev2



#-------------------------------------------------------------
# Tests completed; report results.
print()
print("Number of test results:", len(testResults))
assert len(testResults) == 401

print()
print("{:<55} {:<}".format("Test", "result"))
print("===============================================================")
for k, v in testResults.items():
    print(f"{k:<55} {'Pass' if v else '!! FAIL !!'}")
print()
print(f"Number of test cases: {len(testResults)}")
print(f"Number of tests failing: {list(testResults.values()).count(False)}")
print()
if len(skippedTests) > 0:
    print("Tests skipped:")
    for x in skippedTests:
        print(f"    {x}")
    print()
