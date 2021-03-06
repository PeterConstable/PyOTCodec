from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from ot_file import *


testResults = dict({})
skippedTests = []



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

selawk_file = getTestFontOTFile("Selawik")
sourceHansSans_file = getTestFontOTFile("SourceHansSans")

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



# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

assert numTestResults == 114

printTestResultSummary("Tests for table_maxp", testResults, skippedTests)


