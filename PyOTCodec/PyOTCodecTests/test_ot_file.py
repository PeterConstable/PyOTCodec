from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from ot_file import *


testResults = dict({})
skippedTests = []



#-------------------------------------------------------------
# Tests for low-level stuff: 
#   - file read methods
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


selawk_file = getTestFontOTFile("Selawik")

hhea = selawk_file.fonts[0].tables["hhea"]
tr_hhea = selawk_file.fonts[0].offsetTable.tryGetTableRecord("hhea")
testResults["calcChecksum test 10"] = (hhea.calculatedCheckSum == tr_hhea.checkSum)




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


sourceHansSans_file = getTestFontOTFile("SourceHansSans")

testResults["OTFile read test 4"] = (sourceHansSans_file.sfntVersion == "ttcf")
testResults["OTFile read test 5"] = (sourceHansSans_file.numFonts == 10)
testResults["OTFile read test 6"] = (sourceHansSans_file.isCollection() == True)

ttchdr = sourceHansSans_file.ttcHeader
testResults["TTCHeader read test 1"] = (ttchdr.ttcTag == "ttcf")
testResults["TTCHeader read test 2"] = (ttchdr.majorVersion == 1)
testResults["TTCHeader read test 3"] = (ttchdr.minorVersion == 0)
testResults["TTCHeader read test 4"] = (ttchdr.numFonts == 10)









# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

assert numTestResults == 41

printTestResultSummary("Tests for table_maxp", testResults, skippedTests)


