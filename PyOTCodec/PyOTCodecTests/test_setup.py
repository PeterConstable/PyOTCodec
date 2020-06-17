import ot_file




# Several tests will use selawk.ttf, SourceHanSans-Regular.TTC
selawk_path = r"TestData\selawk.ttf"
sourceHansSans_path = r"TestData\SourceHanSans-Regular.TTC"
bungeeColor_path = r"TestData\BungeeColor-Regular_colr_Windows.ttf"
notoHW_COLR1_rev2_path = r"TestData\noto-handwriting-colr_1_rev2.ttf"

_availableTestFonts = {
    "Selawik": selawk_path,
    "SourceHansSans": sourceHansSans_path,
    "BungeeColor": bungeeColor_path,
    "NotoHW-COLR_1_rev2": notoHW_COLR1_rev2_path
    }
_testFonts = {}

def getTestFontOTFile(name:str):
    if not name in _testFonts:
        _testFonts[name] = ot_file.OTFile(_availableTestFonts[name])
    return _testFonts[name]



def printTestResultSummary(heading:str, testResults:dict, skippedTests:list):
    numTestResults = len(testResults)
    numFailures = list(testResults.values()).count(False)
    numSkipped = len(skippedTests)

    print()
    print(f"{heading}:")
    print()
    print("{:<55} {:<}".format("Test", "result"))
    print("===============================================================")
    for k, v in testResults.items():
        print(f"{k:<55} {'Pass' if v else '!! FAIL !!'}")
    print()
    print(f"Number of test cases: {numTestResults}")
    print(f"Number of tests failing: {numFailures}")
    print()
    if numSkipped > 0:
        print("Tests skipped:")
        for x in skippedTests:
            print(f"    {x}")
        print()
    print()
