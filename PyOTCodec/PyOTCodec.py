from ot_file import * # imports are transitive





#-------------------------------------------------------------
# END -- anything that follows is for testing
#-------------------------------------------------------------


def runAllTests():
    import PyOTCodecTests.test_all_tests


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "alltests":
            runAllTests()
        elif sys.argv[1] == "baseTypes":
            import PyOTCodecTests.test_ot_baseTypes
        elif sys.argv[1] == "structs":
            import PyOTCodecTests.test_ot_baseTypes
            import PyOTCodecTests.test_ot_structs
    else:
        print("Welcome to PyOTCodec")
    import table_COLR_new
