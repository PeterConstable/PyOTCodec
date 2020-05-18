from ot_file import * # imports are transitive











#-------------------------------------------------------------
# END -- anything that follows is for testing
#-------------------------------------------------------------


testResults = dict({})
skippedTests = []

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

# reading with insufficient data left from current position
try:
    ReadInt16(testbio)
except OTCodecError:
    result = True
else:
    result = False
testResults["Insufficient data test 1"] = result

# reading with insufficient data left from current position
testbio.seek(-1, 2)
try:
    ReadRawBytes(testbio, 2)
except OTCodecError:
    result = True
else:
    result = False
testResults["Insufficient data test 2"] = result


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

font = OTFile(r"TestData\selawk.ttf").fonts[0]
hhea = font.tables["hhea"]
tr_hhea = font.offsetTable.tryGetTableRecord("hhea")
testResults["calcChecksum test 10"] = (hhea.calculatedCheckSum == tr_hhea.checkSum)


# tests for Tag
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
testResults["Fixed constructor test 3"] = result

# good args
testResults["Fixed constructor test 4"] = (type(Fixed(bytearray([0,1,0,0]))) == Fixed)
testResults["Fixed constructor test 5"] = (type(Fixed(bytes(b'\xF0\x00\x80\x00'))) == Fixed)
testResults["Fixed constructor test 6"] = (Fixed(b'\xF0\x00\x80\x00') == -4095.5)

# Fixed.createNewFixedFromUint32: arg must be between 0 and 0xffff_ffff
try:
    Fixed.createNewFixedFromUint32(-1)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.createNewFixedFromUint32 test 1"] = result
try:
    Fixed.createNewFixedFromUint32(0x1_FFFF_FFFF)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.createNewFixedFromUint32 test 2"] = result

f = Fixed.createNewFixedFromUint32(0x0001_8000)
testResults["Fixed.createNewFixedFromUint32 test 3"] = (f == 1.5)
f = Fixed.createNewFixedFromUint32(0xF000_8000)
testResults["Fixed.createNewFixedFromUint32 test 4"] = (f == -4095.5)
f = Fixed.createNewFixedFromUint32(0x0001_5000)
testResults["Fixed.createNewFixedFromUint32 test 5"] = (f._rawBytes == bytes(b'\x00\x01\x50\x00'))

# Fixed.createNewFixedFromFloat
try:
    Fixed.createNewFixedFromFloat(-40000)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.createNewFixedFromFloat test 1"] = result
try:
    Fixed.createNewFixedFromFloat(40000)
except OTCodecError:
    result = True
else:
    result = False
testResults["Fixed.createNewFixedFromFloat test 2"] = result

f = Fixed.createNewFixedFromFloat(1.5)
testResults["Fixed.createNewFixedFromFloat test 3"] = (f._rawBytes == bytes(b'\x00\x01\x80\x00'))
f = Fixed.createNewFixedFromFloat(-4095.5)
testResults["Fixed.createNewFixedFromFloat test 4"] = (f._rawBytes == bytes(b'\xF0\x00\x80\x00'))
f = Fixed.createNewFixedFromFloat(1.3125)
testResults["Fixed.createNewFixedFromFloat test 5"] = (f._rawBytes == bytes(b'\x00\x01\x50\x00'))

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
testResults["Fixed members test 5"] = (f.value == -4095.5)
testResults["Fixed members test 6"] = (f.__str__() == "-4095.5")
testResults["Fixed members test 7"] = (f.__repr__() == "-4095.5")
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

# Fixed.tryReadFromBuffer: good arg
testResults["Fixed.tryReadFromBuffer test 3"] = (Fixed.tryReadFromBuffer(b'\xF0\x00\x80\x00') == -4095.5)


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


# tests for OffsetTable constructor
ot = OffsetTable()
testResults["OffsetTable() test 1"] = (type(ot) == OffsetTable)
testResults["OffsetTable() test 2"] = (ot.sfntVersion == None)
testResults["OffsetTable() test 3"] = (ot.searchRange == 0)
testResults["OffsetTable() test 4"] = (ot.entrySelector == 0)
testResults["OffsetTable() test 5"] = (ot.rangeShift == 0)

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

# tests for OffsetTable.AddTableRecord
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
font = OTFile(r"TestData\selawk.ttf").fonts[0]
try:
    font.offsetTable.addTableRecord(tr)
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.AddTableRecord test 7"] = result

# TableRecord read from file can be added to a new OffsetTable
tr = font.offsetTable.tableRecords["cmap"]
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

# None is no-op, even for OffsetTable read from file
font = OTFile(r"TestData\selawk.ttf").fonts[0]
try:
    font.offsetTable.removeTableRecord(None)
except Exception:
    result = False
else:
    result = True
testResults["OffsetTable.removeTableRecord test 6"] = result

# can't remove TableRecord from OffsetTable read from file
try:
    font.offsetTable.removeTableRecord("cmap")
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.removeTableRecord test 7"] = result

# even if not present, can't try to remove TableRecord from OffsetTable read from file
try:
    font.offsetTable.removeTableRecord("zzzz")
except OTCodecError:
    result = True
else:
    result = False
testResults["OffsetTable.removeTableRecord test 8"] = result



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


# tests for table_hhea
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
font = OTFile(r"TestData\selawk.ttf").fonts[0]
try:
    hhea = font.tables["hhea"]
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
tr = font.offsetTable.tryGetTableRecord("hhea")
testResults["Table_hhea.tryReadFromFile test 4"] = (hhea.calculatedCheckSum == tr.checkSum)

# test tryReadFromFile using SourceHanSans-Regular.TTC
font = OTFile(r"TestData\SourceHanSans-Regular.TTC").fonts[0]
try:
    hhea = font.tables["hhea"]
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
tr = font.offsetTable.tryGetTableRecord("hhea")
testResults["Table_hhea.tryReadFromFile test 8"] = (hhea.calculatedCheckSum == tr.checkSum)


# test tryReadFromFile offset/length checks
tr_s = font.offsetTable.tryGetTableRecord("hhea")

# offset out of bounds:
tr = TableRecord.createNewTableRecord("hhea", tr_s.checkSum, 0x7FFF_FFFF, tr_s.length)
try:
    hhea = Table_hhea.tryReadFromFile(font, tr)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_hhea.tryReadFromFile test 9"] = result

# length out of bounds:
tr = TableRecord.createNewTableRecord("hhea", tr_s.checkSum, tr_s.offset, 0x7FFF_FFFF)
try:
    hhea = Table_hhea.tryReadFromFile(font, tr)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_hhea.tryReadFromFile test 10"] = result

# wrong length:
tr = TableRecord.createNewTableRecord("hhea", tr_s.checkSum, tr_s.offset, tr_s.length + 1)
try:
    hhea = Table_hhea.tryReadFromFile(font, tr)
except Exception:
    result = True
else:
    result = False
testResults["Table_hhea.tryReadFromFile test 11"] = result


# tests for table_maxp
maxp = Table_maxp()
testResults["Table_maxp constructor test 1"] = (type(maxp) == Table_maxp)
testResults["Table_maxp constructor test 2"] = (maxp.tableTag == "maxp")
testResults["Table_maxp constructor test 3"] = (not hasattr(maxp, "version"))

# createNew_maxp: check default values for v0.5
maxp = Table_maxp.createNew_maxp(0.5)
testResults["Table_maxp.createNew_maxp test 1"] = (type(maxp) == Table_maxp)
result = True
expected = zip(Table_maxp._maxp_0_5_fields, [Fixed.createNewFixedFromUint32(0x0000_5000), 0])
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
expected = zip(Table_maxp._maxp_0_5_fields, [Fixed.createNewFixedFromUint32(0x0001_0000), 0])
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
font = OTFile(r"TestData\selawk.ttf").fonts[0]
try:
    maxp = font.tables["maxp"]
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
tr = font.offsetTable.tryGetTableRecord("maxp")
testResults["Table_maxp.tryReadFromFile test 4"] = (maxp.calculatedCheckSum == tr.checkSum)


# tests for table_fmtx
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
testResults["Table_maxp.createNew_fmtx test 2"] = result

# test Table_fmtx.tryReadFromFile using skia.ttf -- if present
try:
    font = OTFile(r"TestData\skia.ttf").fonts[0]
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




# Tests completed; report results.

print()
print("{:<45} {:<}".format("Test", "result"))
print("=====================================================")
for k, v in testResults.items():
    print(f"{k:<45} {'Pass' if v else '!! FAIL !!'}")
print()
print(f"Number of test cases: {len(testResults)}")
print(f"Number of tests failing: {list(testResults.values()).count(False)}")
print()
if len(skippedTests) > 0:
    print("Tests skipped:")
    for x in skippedTests:
        print(f"    {x}")
    print()
