from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from ot_file import *


testResults = dict({})
skippedTests = []




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
selawk_file = getTestFontOTFile("Selawik")
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



# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

assert numTestResults == 13

printTestResultSummary("Tests for table_maxp", testResults, skippedTests)
