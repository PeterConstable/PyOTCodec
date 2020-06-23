from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from table_COLR_new import *


testResults = dict({})
skippedTests = []



#=============================================================
# tests for table_COLR
#=============================================================


#-------------------------------------------------------------
# tests for VarFixed
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(VarFixed)
except:
    result = False
else:
    result = True
testResults["Table_COLR VarFixed definition test"] = result

testResults["Table_COLR VarFixed constants test 1"] = (VarFixed.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["Table_COLR VarFixed constants test 2"] = (VarFixed.PACKED_FORMAT == (Fixed.PACKED_FORMAT + "HH"))
testResults["Table_COLR VarFixed constants test 3"] = (VarFixed.PACKED_SIZE == 8)
testResults["Table_COLR VarFixed constants test 4"] = (list(VarFixed.FIELDS.keys()) == ["scalar", "varOuterIndex", "varInnerIndex"])
testResults["Table_COLR VarFixed constants test 5"] = (list(VarFixed.FIELDS.values()) == [Fixed, uint16, uint16])

# constructor args
try:
    x = VarFixed(Fixed.createFixedFromUint32(0x48000), uint16(4))
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFixed constructor test 1"] = result
try:
    x = VarFixed(0x1_8000, uint16(4), uint16(7))
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFixed constructor test 2"] = result

x = VarFixed(Fixed.createFixedFromUint32(0x48000),uint16(1), uint16(3))
testResults["Table_COLR VarFixed constructor test 3"] = (type(x.scalar) == Fixed and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
testResults["Table_COLR VarFixed constructor test 4"] = (x.scalar == 4.5 and x.varOuterIndex == 1 and x.varInnerIndex == 3)

result = x.__repr__() == "{'scalar': 4.5, 'varOuterIndex': 1, 'varInnerIndex': 3}"
testResults["Table_COLR VarFixed __repr__ test"] = result



#-------------------------------------------------------------
# tests for VarF2Dot14
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(VarF2Dot14)
except:
    result = False
else:
    result = True
testResults["Table_COLR VarF2Dot14 definition test"] = result

testResults["Table_COLR VarF2Dot14 constants test 1"] = (VarF2Dot14.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["Table_COLR VarF2Dot14 constants test 2"] = (VarF2Dot14.PACKED_FORMAT == (F2Dot14.PACKED_FORMAT + "HH"))
testResults["Table_COLR VarF2Dot14 constants test 3"] = (VarF2Dot14.PACKED_SIZE == 6)
testResults["Table_COLR VarF2Dot14 constants test 4"] = (list(VarF2Dot14.FIELDS.keys()) == ["scalar", "varOuterIndex", "varInnerIndex"])
testResults["Table_COLR VarF2Dot14 constants test 5"] = (list(VarF2Dot14.FIELDS.values()) == [F2Dot14, uint16, uint16])

# constructor args
try:
    x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), uint16(4))
except:
    result = True
else:
    result = False
testResults["Table_COLR VarF2Dot14 constructor test 1"] = result
try:
    x = VarF2Dot14(0x6000, uint16(4), uint16(7))
except:
    result = True
else:
    result = False
testResults["Table_COLR VarF2Dot14 constructor test 2"] = result

x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), uint16(1), uint16(3))
testResults["Table_COLR VarF2Dot14 constructor test 3"] = (type(x.scalar) == F2Dot14 and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
testResults["Table_COLR VarF2Dot14 constructor test 4"] = (x.scalar == 1.5 and x.varOuterIndex == 1 and x.varInnerIndex == 3)

result = x.__repr__() == "{'scalar': 1.5, 'varOuterIndex': 1, 'varInnerIndex': 3}"
testResults["Table_COLR VarF2Dot14 __repr__ test"] = result



#-------------------------------------------------------------
# tests for VarFWord
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(VarFWord)
except:
    result = False
else:
    result = True
testResults["Table_COLR VarFWord definition test"] = result

testResults["Table_COLR VarFWord constants test 1"] = (VarFWord.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["Table_COLR VarFWord constants test 2"] = (VarFWord.PACKED_FORMAT == (FWord.PACKED_FORMAT + "HH"))
testResults["Table_COLR VarFWord constants test 3"] = (VarFWord.PACKED_SIZE == 6)
testResults["Table_COLR VarFWord constants test 4"] = (list(VarFWord.FIELDS.keys()) == ["coordinate", "varOuterIndex", "varInnerIndex"])
testResults["Table_COLR VarFWord constants test 5"] = (list(VarFWord.FIELDS.values()) == [FWord, uint16, uint16])

# constructor args
try:
    x = VarFWord(FWord(24), uint16(17))
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFWord constructor test 1"] = result
try:
    x = VarFWord(24.0, uint16(17), uint16(23))
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFWord constructor test 2"] = result

x = VarFWord(FWord(-24), uint16(17), uint16(23))
testResults["Table_COLR VarFWord constructor test 3"] = (type(x) == VarFWord and type(x.coordinate) == FWord and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
testResults["Table_COLR VarFWord constructor test 4"] = (x.coordinate == -24 and x.varOuterIndex == 17 and x.varInnerIndex == 23)

testResults["Table_COLR VarFWord __repr__ test"] = (x.__repr__() == "{'coordinate': -24, 'varOuterIndex': 17, 'varInnerIndex': 23}")


#-------------------------------------------------------------
# tests for VarUFWord
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(VarUFWord)
except:
    result = False
else:
    result = True
testResults["Table_COLR VarUFWord definition test"] = result

testResults["Table_COLR VarUFWord constants test 1"] = (VarUFWord.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["Table_COLR VarUFWord constants test 2"] = (VarUFWord.PACKED_FORMAT == (UFWord.PACKED_FORMAT + "HH"))
testResults["Table_COLR VarUFWord constants test 3"] = (VarUFWord.PACKED_SIZE == 6)
testResults["Table_COLR VarUFWord constants test 4"] = (list(VarUFWord.FIELDS.keys()) == ["distance", "varOuterIndex", "varInnerIndex"])
testResults["Table_COLR VarUFWord constants test 5"] = (list(VarUFWord.FIELDS.values()) == [UFWord, uint16, uint16])

# constructor args
try:
    x = VarUFWord(UFWord(24), uint16(17))
except:
    result = True
else:
    result = False
testResults["Table_COLR VarUFWord constructor test 1"] = result
try:
    x = VarUFWord(24, uint16(17), uint16(23))
except:
    result = True
else:
    result = False
testResults["Table_COLR VarUFWord constructor test 2"] = result

x = VarUFWord(UFWord(24), uint16(17), uint16(23))
testResults["Table_COLR VarUFWord constructor test 3"] = (type(x) == VarUFWord and type(x.distance) == UFWord and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
testResults["Table_COLR VarUFWord constructor test 4"] = (x.distance == 24 and x.varOuterIndex == 17 and x.varInnerIndex == 23)

testResults["Table_COLR VarUFWord __repr__ test"] = (x.__repr__() == "{'distance': 24, 'varOuterIndex': 17, 'varInnerIndex': 23}")



#-------------------------------------------------------------
# tests for Affine2x2
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(Affine2x2)
except:
    result = False
else:
    result = True
testResults["Table_COLR Affine2x2 definition test"] = result

testResults["Table_COLR Affine2x2 constants test 1"] = (Affine2x2.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT)
testResults["Table_COLR Affine2x2 constants test 2"] = (Affine2x2.PACKED_FORMAT == ">4sHH4sHH4sHH4sHH")
testResults["Table_COLR Affine2x2 constants test 3"] = (Affine2x2.PACKED_SIZE == (VarFixed.PACKED_SIZE * 4))
testResults["Table_COLR Affine2x2 constants test 4"] = (list(Affine2x2.FIELDS.keys()) == ["xx", "xy", "yx", "yy"])
testResults["Table_COLR Affine2x2 constants test 5"] = (list(Affine2x2.FIELDS.values()) == [VarFixed, VarFixed, VarFixed, VarFixed])

# constructor args
x = VarFixed(Fixed.createFixedFromUint32(0x1_8000), uint16(2), uint16(17))
try:
    y = Affine2x2(x, x, x)
except:
    result = True
else:
    result = False
testResults["Table_COLR Affine2x2 constructor test 1"] = result
try:
    y = Affine2x2(x, x, x, 24)
except:
    result = True
else:
    result = False
testResults["Table_COLR Affine2x2 constructor test 2"] = result

y = Affine2x2(x, x, x, x)
result = (type(y) == Affine2x2 and type(y.xx) == VarFixed and type(y.xy) == VarFixed and type(y.yx) == VarFixed and type(y.yy) == VarFixed)
testResults["Table_COLR Affine2x2 constructor test 3"] = result
result = (y.xx.scalar._rawBytes == b'\x00\01\x80\x00' and y.xx.varOuterIndex == 2 and y.xx.varInnerIndex == 17)
testResults["Table_COLR Affine2x2 constructor test 4"] = result

result = (y.__repr__() == "{'xx': {'scalar': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}, 'xy': {'scalar': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}, 'yx': {'scalar': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}, 'yy': {'scalar': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}}")
testResults["Table_COLR Affine2x2 __repr__ test"] = result



#-------------------------------------------------------------
# tests for ColorIndex
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(ColorIndex)
except:
    result = False
else:
    result = True
testResults["Table_COLR ColorIndex definition test"] = result

testResults["ColorIndex constants test 1"] = (ColorIndex.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT)
testResults["ColorIndex constants test 2"] = (ColorIndex.PACKED_FORMAT == ">H2sHH")
testResults["ColorIndex constants test 3"] = (ColorIndex.PACKED_SIZE == 8)
testResults["ColorIndex constants test 4"] = (list(ColorIndex.FIELDS.keys()) == ["paletteIndex", "alpha"])
testResults["ColorIndex constants test 5"] = (list(ColorIndex.FIELDS.values()) == [uint16, VarF2Dot14])

# constructor args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(1), uint16(3))
try:
    y = ColorIndex(uint16(24))
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 1"] = result
try:
    y = ColorIndex(uint16(24), 42)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 2"] = result
try:
    y = ColorIndex(24.0, x)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 3"] = result

# alpha out of range [0, 1]
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), uint16(1), uint16(3))
try:
    y = ColorIndex(uint16(24), x)
except ValueError:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 4"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x8000), uint16(1), uint16(3))
try:
    y = ColorIndex(uint16(24), x)
except ValueError:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 5"] = result

# good args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(1), uint16(3))
y = ColorIndex(uint16(24), x)
testResults["Table_COLR ColorIndex constructor test 6"] = (type(y.paletteIndex) == uint16 and type(y.alpha) == VarF2Dot14)
testResults["Table_COLR ColorIndex test constructor 7"] = (y.paletteIndex == 24 and y.alpha.scalar == 0.75 and y.alpha.varOuterIndex == 1 and y.alpha.varInnerIndex == 3)

x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(1), uint16(3))
y = ColorIndex(uint16(24), x)
result = y.__repr__() == "{'paletteIndex': 24, 'alpha': {'scalar': 0.75, 'varOuterIndex': 1, 'varInnerIndex': 3}}"
testResults["Table_COLR ColorIndex __repr__ test"] = result



#-------------------------------------------------------------
# tests for ColorStop
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(ColorIndex)
except:
    result = False
else:
    result = True
testResults["Table_COLR ColorStop definition test"] = result

testResults["Table_COLR ColorStop constants test 1"] = (ColorStop.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT)
testResults["Table_COLR ColorStop constants test 2"] = (ColorStop.PACKED_FORMAT == ">2sHHH2sHH")
testResults["Table_COLR ColorStop constants test 3"] = (ColorStop.PACKED_SIZE == 14)
testResults["Table_COLR ColorStop constants test 4"] = (list(ColorStop.FIELDS.keys()) == ["stopOffset", "color"])
testResults["Table_COLR ColorStop constants test 5"] = (list(ColorStop.FIELDS.values()) == [VarF2Dot14, ColorIndex])

# constructor arg validations
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(1), uint16(3))
y = ColorIndex(uint16(24), x)
try:
    z = ColorStop(x)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 1"] = result
try:
    z = ColorStop(24, y)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 2"] = result
try:
    z = ColorStop(x, 24)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 3"] = result

# stopOffset out of range [0, 1]
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x4001), uint16(1), uint16(3))
try:
    z = ColorStop(x, y)
except ValueError:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 4"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0xC001), uint16(1), uint16(3))
try:
    z = ColorStop(x, y)
except ValueError:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 5"] = result

# good args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x1000), uint16(1), uint16(3))
y = ColorIndex(uint16(24), x)
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(0), uint16(4))
z = ColorStop(x, y)
testResults["Table_COLR ColorStop constructor test 6"] = (type(z.stopOffset) == VarF2Dot14 and type(z.color) == ColorIndex)
testResults["Table_COLR ColorStop constructor test 7"] = (z.stopOffset.scalar == 0.75 and z.stopOffset.varOuterIndex == 0 and z.stopOffset.varInnerIndex == 4)
testResults["Table_COLR ColorStop constructor test 8"] = (z.color.paletteIndex == 24 and z.color.alpha.scalar == 0.25 and z.color.alpha.varOuterIndex == 1 and y.alpha.varInnerIndex == 3)

result = z.__repr__() == "{'stopOffset': {'scalar': 0.75, 'varOuterIndex': 0, 'varInnerIndex': 4}, 'color': {'paletteIndex': 24, 'alpha': {'scalar': 0.25, 'varOuterIndex': 1, 'varInnerIndex': 3}}}"
testResults["Table_COLR ColorStop __repr__ test"] = result



#-------------------------------------------------------------
# tests for ColorLine
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(ColorLine)
except:
    result = False
else:
    result = True
testResults["Table_COLR ColorLine definition test"] = result

testResults["Table_COLR ColorLine constants test 1"] = (ColorLine.TYPE_CATEGORY == otTypeCategory.VAR_LENGTH_STRUCT)
testResults["Table_COLR ColorLine constants test 2"] = (ColorLine.PACKED_FORMAT == ">HH")
testResults["Table_COLR ColorLine constants test 3"] = (ColorLine.PACKED_SIZE == 4)
testResults["Table_COLR ColorLine constants test 4"] = (list(ColorLine.FIELDS.keys()) == ["extend", "numStops"])
testResults["Table_COLR ColorLine constants test 5"] = (list(ColorLine.FIELDS.values()) == [uint16, uint16])




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
