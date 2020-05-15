from OTTypes import *
from OTFile import *
from OTFont import *










#-------------------------------------------------------------
# END -- anything that follows is for testing
#-------------------------------------------------------------



testResults = dict({})

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
testResults["Insufficient data test 1"] = result
testbio.seek(-1, 2)
try:
    ReadRawBytes(testbio, 2)
except OTCodecError:
    result = True
else:
    result = False
testResults["Insufficient data test 2"] = result


# tests for Tag
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
testResults["Tag validation test 1"] = Tag.validateTag("abcd") == 0
testResults["Tag validation test 2"] = Tag.validateTag("abc") == 0x01
testResults["Tag validation test 3"] = Tag.validateTag("abcde") == 0x01
testResults["Tag validation test 4"] = Tag.validateTag("ab€c") == 0x02
testResults["Tag validation test 5"] = Tag.validateTag("ab c") == 0x04
testResults["Tag validation test 6"] = Tag.validateTag(" €c") == 0x07


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


# tests for OTFile.IsSupportedSfntVersion
testResults["OTFile.IsSupportedSfntVersion test 1"] = (OTFile.isSupportedSfntVersion(b'\x00\x01\x00\x00') == True)
testResults["OTFile.IsSupportedSfntVersion test 2"] = (OTFile.isSupportedSfntVersion("OTTO") == True)
testResults["OTFile.IsSupportedSfntVersion test 3"] = (OTFile.isSupportedSfntVersion("true") == True)
testResults["OTFile.IsSupportedSfntVersion test 4"] = (OTFile.isSupportedSfntVersion("ttcf") == True)
testResults["OTFile.IsSupportedSfntVersion test 5"] = (OTFile.isSupportedSfntVersion("abcd") == False)


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


# tests for TableRecord constructor
tr = TableRecord()
testResults["TableRecord() test 1"] = (type(tr) == TableRecord)
testResults["TableRecord() test 2"] = (tr.tableTag == None)
testResults["TableRecord() test 3"] = (tr.checkSum == 0)
testResults["TableRecord() test 4"] = (tr.offset == 0)
testResults["TableRecord() test 5"] = (tr.length == 0)

# tests for TableRecord.createNewTableRecord
tr = TableRecord.createNewTableRecord("abcd")
testResults["TableRecord.createNewTableRecord test 1"] = (type(tr) == TableRecord)
testResults["TableRecord.createNewTableRecord test 2"] = (tr.tableTag == "abcd")
testResults["TableRecord.createNewTableRecord test 3"] = (tr.checkSum == 0)
tr = TableRecord.createNewTableRecord("bcde", 42)
testResults["TableRecord.createNewTableRecord test 4"] = (tr.tableTag == "bcde")
testResults["TableRecord.createNewTableRecord test 5"] = (tr.checkSum == 42)
testResults["TableRecord.createNewTableRecord test 6"] = (tr.offset == 0)
tr = TableRecord.createNewTableRecord("cdef", 42, 43, 44)
testResults["TableRecord.createNewTableRecord test 7"] = (tr.tableTag == "cdef")
testResults["TableRecord.createNewTableRecord test 8"] = (tr.checkSum == 42)
testResults["TableRecord.createNewTableRecord test 9"] = (tr.offset == 43)
testResults["TableRecord.createNewTableRecord test 10"] = (tr.length == 44)


# tests for OffsetTable constructor
ot = OffsetTable()
testResults["OffsetTable() test 1"] = (type(ot) == OffsetTable)
testResults["OffsetTable() test 2"] = (ot.sfntVersion == None)
testResults["OffsetTable() test 3"] = (ot.searchRange == 0)
testResults["OffsetTable() test 4"] = (ot.entrySelector == 0)
testResults["OffsetTable() test 5"] = (ot.rangeShift == 0)

# tests for OffsetTable.createNewOffsetTable
ot = OffsetTable.createNewOffsetTable("abcd")
testResults["OffsetTable.createNewOffsetTable test 1"] = (type(ot) == OffsetTable)
testResults["OffsetTable.createNewOffsetTable test 1"] = (ot.sfntVersion == "abcd")
testResults["OffsetTable.createNewOffsetTable test 1"] = (ot.searchRange == 0)
ot = OffsetTable.createNewOffsetTable("abcd", 42)
testResults["OffsetTable.createNewOffsetTable test 1"] = (ot.sfntVersion == "abcd")
testResults["OffsetTable.createNewOffsetTable test 1"] = (ot.searchRange == 42)
testResults["OffsetTable.createNewOffsetTable test 1"] = (ot.entrySelector == 0)
ot = OffsetTable.createNewOffsetTable("abcd", 42, 42, 44)
testResults["OffsetTable.createNewOffsetTable test 1"] = (ot.sfntVersion == "abcd")
testResults["OffsetTable.createNewOffsetTable test 1"] = (ot.searchRange == 42)
testResults["OffsetTable.createNewOffsetTable test 1"] = (ot.entrySelector == 43)
testResults["OffsetTable.createNewOffsetTable test 1"] = (ot.rangeShift == 44)

# tests for OffsetTable.AddTableRecord
try:
    ot.addTableRecord(None)
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.AddTableRecord test 1"] = result

tr = TableRecord()
try:
    ot.addTableRecord(tr)
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.AddTableRecord test 2"] = result

tr = TableRecord.createNewTableRecord("abcd", 42)
ot.addTableRecord(tr)
testResults["OffsetTable.AddTableRecord test 3"] = (len(ot.tableRecords) == 1)
testResults["OffsetTable.AddTableRecord test 4"] = (ot.tableRecords["abcd"].checkSum == 42)

font = OTFile(r"TestData\selawk.ttf").fonts[0]
try:
    font.offsetTable.addTableRecord(tr)
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.AddTableRecord test 5"] = result
tr = font.offsetTable.tableRecords["cmap"]
ot.addTableRecord(tr)
testResults["OffsetTable.AddTableRecord test 6"] = (len(ot.tableRecords) == 2)
testResults["OffsetTable.AddTableRecord test 7"] = (ot.tableRecords["cmap"].checkSum == 0x22F2_F74C)


# tests for OTFile, OTFont, OffsetTable, TableRecord using selawk.ttf
file = OTFile(r"TestData\selawk.ttf")
testResults["OTFile path test 5"] = (file.path.name == r"selawk.ttf")
testResults["OTFile read test 1"] = (file.sfntVersion == b'\x00\x01\x00\x00')
testResults["OTFile read test 2"] = (file.numFonts == 1)
testResults["OTFile read test 3"] = (file.isCollection() == False)

font = file.fonts[0]
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


offtbl = font.offsetTable
testResults["OffsetTable test 1"] = (offtbl.offsetInFile == 0)
testResults["OffsetTable test 2"] = (offtbl.sfntVersion == b'\x00\x01\x00\x00')
testResults["OffsetTable test 3"] = (offtbl.numTables == 15)
testResults["OffsetTable test 4"] = (offtbl.searchRange == 0x80)
testResults["OffsetTable test 5"] = (offtbl.entrySelector == 0x03)
testResults["OffsetTable test 6"] = (offtbl.rangeShift == 0x70)

testResults["OffsetTable.TryGetTableRecord test 1"] = (type(offtbl.tryGetTableRecord("cmap")) == TableRecord)
testResults["OffsetTable.TryGetTableRecord test 2"] = (offtbl.tryGetTableRecord("zzzz") == None)


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


# tests for OTFile, TTCHeader, OTFont, OffsetTable, TableRecord using SourceHanSans-Regular.TTC
file = OTFile(r"TestData\SourceHanSans-Regular.TTC")
testResults["OTFile read test 4"] = (file.sfntVersion == "ttcf")
testResults["OTFile read test 5"] = (file.numFonts == 10)
testResults["OTFile read test 6"] = (file.isCollection() == True)

ttchdr = file.ttcHeader
testResults["TTCHeader read test 1"] = (ttchdr.ttcTag == "ttcf")
testResults["TTCHeader read test 2"] = (ttchdr.majorVersion == 1)
testResults["TTCHeader read test 3"] = (ttchdr.minorVersion == 0)
testResults["TTCHeader read test 4"] = (ttchdr.numFonts == 10)

font = file.fonts[0]
testResults["OTFont read test 6"] = (font.offsetInFile == 0x34)
testResults["OTFont read test 7"] = (font.sfntVersionTag() == "OTTO")
testResults["OTFont read test 8"] = (font.ttcIndex == 0)
testResults["OTFont read test 9"] = (font.isWithinTtc == True)
testResults["OTFont read test 10"] = (font.defaultLabel == "SourceHanSans-Regular.TTC:0")

offtbl = font.offsetTable
testResults["OffsetTable test 7"] = (offtbl.offsetInFile == 0x34)
testResults["OffsetTable test 8"] = (offtbl.sfntVersion == "OTTO")
testResults["OffsetTable test 9"] = (offtbl.numTables == 16)
testResults["OffsetTable test 10"] = (offtbl.searchRange == 0x0100)
testResults["OffsetTable test 11"] = (offtbl.entrySelector == 0x0004)
testResults["OffsetTable test 12"] = (offtbl.rangeShift == 0x0000)

tblrec = list(offtbl.tableRecords.values())[3]
testResults["TableRecord test 9"] = (tblrec.tableTag == "GPOS")
testResults["TableRecord test 10"] = (tblrec.checkSum == 0x0D16_AD78)
testResults["TableRecord test 11"] = (tblrec.offset == 0x00F8_CB20)
testResults["TableRecord test 12"] = (tblrec.length == 0x0000_B91A)

font = file.fonts[1]
testResults["OTFont read test 11"] = (font.offsetInFile == 0x0140)
testResults["OTFont read test 12"] = (font.sfntVersionTag() == "OTTO")
testResults["OTFont read test 13"] = (font.ttcIndex == 1)
testResults["OTFont read test 14"] = (font.isWithinTtc == True)
testResults["OTFont read test 15"] = (font.defaultLabel == "SourceHanSans-Regular.TTC:1")

offtbl = font.offsetTable
testResults["OffsetTable test 13"] = (offtbl.offsetInFile == 0x140)
testResults["OffsetTable test 14"] = (offtbl.sfntVersion == "OTTO")
testResults["OffsetTable test 15"] = (offtbl.numTables == 16)
testResults["OffsetTable test 16"] = (offtbl.searchRange == 0x100)
testResults["OffsetTable test 17"] = (offtbl.entrySelector == 0x04)
testResults["OffsetTable test 18"] = (offtbl.rangeShift == 0x00)



print()
print("{:<45} {:<}".format("Test", "result"))
print("=====================================================")
for k, v in testResults.items():
    print(f"{k:<45} {'Pass' if v else '!! FAIL !!'}")
print()
print(f"Number of test cases: {len(testResults)}")
print(f"Number of tests failing: {list(testResults.values()).count(False)}")
print()
