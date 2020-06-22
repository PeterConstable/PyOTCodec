from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from table_COLR_new import *


testResults = dict({})
skippedTests = []



#-------------------------------------------------------------
# tests for table_COLR
#-------------------------------------------------------------

# test BaseGlyphRecord

try:
    assertIsWellDefinedOTType(BaseGlyphRecord)
except:
    result = False
else:
    result = True
testResults["Table_COLR BaseGlyphRecord definition test"] = result

testResults["Table_COLR BaseGlyphRecord constants test 1"] = (BaseGlyphRecord.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["Table_COLR BaseGlyphRecord constants test 2"] = (BaseGlyphRecord.PACKED_FORMAT == ">HHH")
testResults["Table_COLR BaseGlyphRecord constants test 3"] = (BaseGlyphRecord.PACKED_SIZE == 6)
testResults["Table_COLR BaseGlyphRecord constants test 5"] = (list(BaseGlyphRecord.FIELDS.keys()) == ["glyphID", "firstLayerIndex", "numLayers"])
testResults["Table_COLR BaseGlyphRecord constants test 6"] = (list(BaseGlyphRecord.FIELDS.values()) == [uint16, uint16, uint16])


try:
    x = BaseGlyphRecord(2, 4)
except:
    result = True
else:
    result = False
testResults["Table_COLR BaseGlyphRecord constructor test 1"] = result
try:
    x = BaseGlyphRecord(2.0, 4, 17)
except:
    result = True
else:
    result = False
testResults["Table_COLR BaseGlyphRecord constructor test 2"] = result
try:
    x = BaseGlyphRecord(-2, 4, 17)
except:
    result = True
else:
    result = False
testResults["Table_COLR BaseGlyphRecord constructor test 3"] = result
try:
    x = BaseGlyphRecord(2, -4, 17)
except:
    result = True
else:
    result = False
testResults["Table_COLR BaseGlyphRecord constructor test 4"] = result
try:
    x = BaseGlyphRecord(2, 4, -17)
except:
    result = True
else:
    result = False
testResults["Table_COLR BaseGlyphRecord constructor test 5"] = result
x = BaseGlyphRecord(2, 4, 17)
result = (type(x) == BaseGlyphRecord)
for f in BaseGlyphRecord.FIELDS:
    result &= hasattr(x, f)
testResults["Table_COLR BaseGlyphRecord constructor test 6"] = result
result = (x.glyphID == 2 and x.firstLayerIndex == 4 and x.numLayers == 17)
testResults["Table_COLR BaseGlyphRecord constructor test 7"] = result






notoHW_COLR1_rev2_file = getTestFontOTFile("NotoHW-COLR_1_rev2")






# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

#assert numTestResults == 183

printTestResultSummary("Tests for table_COLR", testResults, skippedTests)
