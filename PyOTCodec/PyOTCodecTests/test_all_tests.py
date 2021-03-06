from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

testModules = []
import PyOTCodecTests.test_ot_file
testModules.append(PyOTCodecTests.test_ot_file)
import PyOTCodecTests.test_ot_font
testModules.append(PyOTCodecTests.test_ot_font)
import PyOTCodecTests.test_ot_types
testModules.append(PyOTCodecTests.test_ot_types)
import PyOTCodecTests.test_table_COLR
testModules.append(PyOTCodecTests.test_table_COLR)
import PyOTCodecTests.test_table_fmtx
testModules.append(PyOTCodecTests.test_table_fmtx)
import PyOTCodecTests.test_table_hhea
testModules.append(PyOTCodecTests.test_table_hhea)
import PyOTCodecTests.test_table_maxp
testModules.append(PyOTCodecTests.test_table_maxp)






#-------------------------------------------------------------
# Tests completed; report results.


sumAllTests = 0
sumFailures = 0
sumSkipped = 0
print()
print("Summary:\n")
print("{:<32} {:<16} {:<16} {:<20}".format("Test Module", "# test results", "# failures", "# skipped tests"))
print("===================================================================================")
for tm in testModules:
    print(f"{tm.__name__:<32} {tm.numTestResults:<16} {tm.numFailures:<16} {tm.numSkipped}")
    sumAllTests += tm.numTestResults
    sumFailures += tm.numFailures
    sumSkipped += tm.numSkipped
print("===================================================================================")
print("{:<32} {:<16} {:<16} {:<20}".format("Totals", sumAllTests, sumFailures, sumSkipped))
print()
