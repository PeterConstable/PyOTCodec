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

file = OTFile(r"TestData\selawk.ttf")
testResults["OTFile path test 5"] = (file.path.name == r"selawk.ttf")
testResults["OTFile read test 1"] = (file.sfntVersion == b'\x00\x01\x00\x00')
testResults["OTFile read test 2"] = (file.numFonts == 1)
testResults["OTFile read test 3"] = (file.IsCollection() == False)

font = file.fonts[0]
testResults["OTFont read test 1"] = font.offsetInFile == 0
testResults["OTFont read test 2"] = font.ttcIndex == None
testResults["OTFont read test 3"] = font.isInTtc == False
testResults["OTFont read test 4"] = font.defaultLabel == "selawk.ttf"

offtbl = font.offsetTable
testResults["OffsetTable test 1"] = (offtbl.offsetInFile == 0)
testResults["OffsetTable test 2"] = (offtbl.sfntVersion == b'\x00\x01\x00\x00')
testResults["OffsetTable test 3"] = (offtbl.numTables == 15)
testResults["OffsetTable test 4"] = (offtbl.searchRange == 0x80)
testResults["OffsetTable test 5"] = (offtbl.entrySelector == 0x03)
testResults["OffsetTable test 6"] = (offtbl.rangeShift == 0x70)

tblrec = offtbl.tableRecords[0]
testResults["TableRecord test 1"] = (tblrec.tableTag == "DSIG")
testResults["TableRecord test 2"] = (tblrec.checkSum == 0xF054_3E26)
testResults["TableRecord test 3"] = (tblrec.offset == 0x0000_91E4)
testResults["TableRecord test 4"] = (tblrec.length == 0x0000_1ADC)

tblrec = offtbl.tableRecords[5]
testResults["TableRecord test 5"] = (tblrec.tableTag == "cmap")
testResults["TableRecord test 6"] = (tblrec.checkSum == 0x22F2_F74C)
testResults["TableRecord test 7"] = (tblrec.offset == 0x0000_0758)
testResults["TableRecord test 8"] = (tblrec.length == 0x0000_0606)


file = OTFile(r"TestData\SourceHanSans-Regular.TTC")
testResults["OTFile read test 4"] = (file.sfntVersion == "ttcf")
testResults["OTFile read test 5"] = (file.numFonts == 10)
testResults["OTFile read test 6"] = (file.IsCollection() == True)

ttchdr = file.ttcHeader
testResults["TTCHeader read test 1"] = (ttchdr.ttcTag == "ttcf")
testResults["TTCHeader read test 2"] = (ttchdr.majorVersion == 1)
testResults["TTCHeader read test 3"] = (ttchdr.minorVersion == 0)
testResults["TTCHeader read test 4"] = (ttchdr.numFonts == 10)

font = file.fonts[0]
testResults["OTFont read test 5"] = font.offsetInFile == 0x34
testResults["OTFont read test 6"] = font.ttcIndex == 0
testResults["OTFont read test 7"] = font.isInTtc == True
testResults["OTFont read test 8"] = font.defaultLabel == "SourceHanSans-Regular.TTC:0"

offtbl = font.offsetTable
testResults["OffsetTable test 7"] = (offtbl.offsetInFile == 0x34)
testResults["OffsetTable test 8"] = (offtbl.sfntVersion == "OTTO")
testResults["OffsetTable test 9"] = (offtbl.numTables == 16)
testResults["OffsetTable test 10"] = (offtbl.searchRange == 0x0100)
testResults["OffsetTable test 11"] = (offtbl.entrySelector == 0x0004)
testResults["OffsetTable test 12"] = (offtbl.rangeShift == 0x0000)

tblrec = offtbl.tableRecords[3]
testResults["TableRecord test 9"] = (tblrec.tableTag == "GPOS")
testResults["TableRecord test 10"] = (tblrec.checkSum == 0x0D16_AD78)
testResults["TableRecord test 11"] = (tblrec.offset == 0x00F8_CB20)
testResults["TableRecord test 12"] = (tblrec.length == 0x0000_B91A)

font = file.fonts[1]
testResults["OTFont read test 9"] = font.offsetInFile == 0x0140
testResults["OTFont read test 10"] = font.ttcIndex == 1
testResults["OTFont read test 11"] = font.isInTtc == True
testResults["OTFont read test 12"] = font.defaultLabel == "SourceHanSans-Regular.TTC:1"

offtbl = font.offsetTable
testResults["OffsetTable test 13"] = (offtbl.offsetInFile == 0x140)
testResults["OffsetTable test 14"] = (offtbl.sfntVersion == "OTTO")
testResults["OffsetTable test 15"] = (offtbl.numTables == 16)
testResults["OffsetTable test 16"] = (offtbl.searchRange == 0x100)
testResults["OffsetTable test 17"] = (offtbl.entrySelector == 0x04)
testResults["OffsetTable test 18"] = (offtbl.rangeShift == 0x00)



print("{:<35} {:<}".format("Test", "result"))
print("===========================================")
for k, v in testResults.items():
    print("{:<35} {!r}".format(k, v))

