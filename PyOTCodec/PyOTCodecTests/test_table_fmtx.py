from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from ot_file import *


testResults = dict({})
skippedTests = []


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




# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

assert numTestResults == 8

printTestResultSummary("Tests for table_maxp", testResults, skippedTests)
