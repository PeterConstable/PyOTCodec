from ot_file import * # imports are transitive





#-------------------------------------------------------------
# END -- anything that follows is for testing
#-------------------------------------------------------------


def runAllTests():
    import PyOTCodecTests.test_all_tests


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "tests":
        runAllTests()
    else:
        print("Welcome to PyOTCodec")