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








notoHW_COLR1_rev2_file = getTestFontOTFile("NotoHW-COLR_1_rev2")






# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

#assert numTestResults == 183

printTestResultSummary("Tests for table_COLR", testResults, skippedTests)
