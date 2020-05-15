from OTTypes import *
from OTFile import *
from OTFont import *










#-------------------------------------------------------------
# END -- anything that follows is temporary stuff for testing
#-------------------------------------------------------------



testResults = dict({})

from io import BytesIO
testBytes1 = b'\x02\x0F\x37\xDC\x9A\xA2\x0F\xE7\xDC\x9A\x02\xBF\x27\xDC\x9A\xB2\x0F\x37\xDC\x9A\x02\x0F\x37\xDC\x9A\x27\xDC\x27\xDC\x9A\xB2\x0F\x37\xDC\x9A\xB2'
testbio = BytesIO(testBytes1)
testResults["ReadRawBytes test"] = ReadRawBytes(testbio, 5) == b'\x02\x0F\x37\xDC\x9A'
testResults["ReadInt8 test"] = ReadInt8(testbio) == -94 # \xA2
testResults["ReadUint8 test"] = ReadUint8(testbio) == 0x0F
testResults["ReadInt16"] = ReadInt16(testbio) == -6180 # \xE7\xDC
testResults["ReadUint16"] = ReadUint16(testbio) == 0x9A02
testResults["ReadInt32"] = ReadInt32(testbio) == -1087906662 # \xBF\x27\xDC\x9A
testResults["ReadUint32"] = ReadUint32(testbio) == 0xB20F37DC
testResults["ReadInt64"] = ReadInt64(testbio) == -7349294909316519972 # \x9A\x02\x0F\x37\xDC\x9A\x27\xDC
testResults["ReadUint64"] = ReadUint64(testbio) == 0x27DC9AB20F37DC9A

try:
    ReadInt16(testbio)
except OTCodecError:
    result = True
else:
    result = False
testResults["Insufficient data test"] = result
x = Tag(b'\x00\x01')
testResults["Tag constructor test 1"] = (x == b'\x00\x01\x00\x00')
x = Tag(b'\x61\x62\x63\x64')
testResults["Tag constructor test 2"] = (x == "abcd")
x = Tag("ab")
testResults["Tag constructor test 3"] = (x == "ab  ")
x = Tag("abcd")
testResults["Tag constructor test 4"] = (x == "abcd")
try:
    Tag([0,1,0,0])
except OTCodecError:
    result = True
else:
    result = False
testResults["Tag invalid argument test 1"] = result
testResults["Tag validation test 1"] = Tag.validateTagString("abcd") == 0
testResults["Tag validation test 2"] = Tag.validateTagString("abc") == 0x01
testResults["Tag validation test 3"] = Tag.validateTagString("abcde") == 0x01
testResults["Tag validation test 4"] = Tag.validateTagString("ab€c") == 0x02
testResults["Tag validation test 5"] = Tag.validateTagString("ab c") == 0x04
testResults["Tag validation test 6"] = Tag.validateTagString(" €c") == 0x07


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
    x = OTFile("foo")
except OTCodecError:
    result = True
else:
    result = False
testResults["OTFile path test 3"] = result
try:
    x = OTFile("TestData")
except OTCodecError:
    result = True
else:
    result = False
testResults["OTFile path test 4"] = result

x = OTFile(r"TestData\selawk.ttf")
testResults["OTFile path test 5"] = (x.path.name == r"selawk.ttf")
testResults["OTFile read test 1"] = (x.sfntVersion == b'\x00\x01\x00\x00')
testResults["OTFile read test 2"] = (x.numFonts == 1)
testResults["OTFile read test 3"] = (x.IsCollection() == False)

x = x.fonts[0]
testResults["OTFont read test 1"] = x.offsetInFile == 0
testResults["OTFont read test 2"] = x.ttcIndex == None
testResults["OTFont read test 3"] = x.isInTtc == False
testResults["OTFont read test 4"] = x.defaultLabel == "selawk.ttf"

x = OTFile(r"TestData\CAMBRIA.TTC")
testResults["OTFile read test 4"] = (x.sfntVersion == "ttcf")
testResults["OTFile read test 5"] = (x.numFonts == 2)
testResults["OTFile read test 6"] = (x.IsCollection() == True)

y = x.ttcHeader
testResults["TTCHeader read test 1"] = (y.ttcTag == "ttcf")
testResults["TTCHeader read test 2"] = (y.majorVersion == 2)
testResults["TTCHeader read test 3"] = (y.minorVersion == 0)
testResults["TTCHeader read test 4"] = (y.numFonts == 2)
testResults["TTCHeader read test 5"] = (y.dsigTag == "DSIG")
testResults["TTCHeader read test 6"] = (y.dsigLength == 0x1778)
testResults["TTCHeader read test 7"] = (y.dsigOffset == 0x18AB54)

y = x.fonts[0]
testResults["OTFont read test 5"] = y.offsetInFile == 0x20
testResults["OTFont read test 6"] = y.ttcIndex == 0
testResults["OTFont read test 7"] = y.isInTtc == True
testResults["OTFont read test 8"] = y.defaultLabel == "CAMBRIA.TTC:0"

y = x.fonts[1]
testResults["OTFont read test 9"] = y.offsetInFile == 0x016C
testResults["OTFont read test 10"] = y.ttcIndex == 1
testResults["OTFont read test 11"] = y.isInTtc == True
testResults["OTFont read test 12"] = y.defaultLabel == "CAMBRIA.TTC:1"




print(x.sfntVersion)
print("file exists?", x.path.exists())
print("name:", x.path.name, x.path.is_file())
print("x.numFonts:", x.numFonts)
print("number of tables:", len(x.fonts[0].offsetTable.tableRecords))
print(x.fonts[0].defaultLabel)
print(x.fonts[0].ttcIndex)
x = OTFile(r"TestData\CAMBRIA.TTC")
print("x.numFonts:", x.numFonts)
print(x.fonts[0].defaultLabel)
print(x.fonts[0].ttcIndex)
