from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from ot_file import *


testResults = dict({})
skippedTests = []



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
selawk_file = getTestFontOTFile("Selawik")

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
sourceHansSans_file = getTestFontOTFile("SourceHansSans")

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




# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

assert numTestResults == 16

printTestResultSummary("Tests for table_maxp", testResults, skippedTests)
