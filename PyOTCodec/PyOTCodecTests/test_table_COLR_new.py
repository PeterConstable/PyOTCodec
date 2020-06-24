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
testResults["VarFixed definition test"] = result

testResults["VarFixed constants test 1"] = (VarFixed.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["VarFixed constants test 2"] = (VarFixed.PACKED_FORMAT == (Fixed.PACKED_FORMAT + "HH"))
testResults["VarFixed constants test 3"] = (VarFixed.PACKED_SIZE == 8)
testResults["VarFixed constants test 4"] = (list(VarFixed.FIELDS.keys()) == ["scalar", "varOuterIndex", "varInnerIndex"])
testResults["VarFixed constants test 5"] = (list(VarFixed.FIELDS.values()) == [Fixed, uint16, uint16])

# constructor args
try:
    x = VarFixed(Fixed.createFixedFromUint32(0x48000), uint16(4))
except:
    result = True
else:
    result = False
testResults["VarFixed constructor test 1"] = result
try:
    x = VarFixed(0x1_8000, uint16(4), uint16(7))
except:
    result = True
else:
    result = False
testResults["VarFixed constructor test 2"] = result

x = VarFixed(Fixed.createFixedFromUint32(0x48000),uint16(1), uint16(3))
result = (type(x.scalar) == Fixed and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
result &= (x.scalar == 4.5 and x.varOuterIndex == 1 and x.varInnerIndex == 3)
testResults["VarFixed constructor test 3"] = result

result = x.__repr__() == "{'scalar': 4.5, 'varOuterIndex': 1, 'varInnerIndex': 3}"
testResults["VarFixed __repr__ test"] = result

buffer = b'\x00\x03\x80\x00\x00\xa0\x00\xa1\xf0\xf0'
x = tryReadFixedLengthStructFromBuffer(buffer, VarFixed)
result = type(x) == VarFixed
result &= (type(x.scalar) == Fixed and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
result &= (x.scalar == 3.5 and x.varOuterIndex == 160 and x.varInnerIndex == 161)
testResults["VarFixed tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for VarF2Dot14
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(VarF2Dot14)
except:
    result = False
else:
    result = True
testResults["VarF2Dot14 definition test"] = result

testResults["VarF2Dot14 constants test 1"] = (VarF2Dot14.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["VarF2Dot14 constants test 2"] = (VarF2Dot14.PACKED_FORMAT == (F2Dot14.PACKED_FORMAT + "HH"))
testResults["VarF2Dot14 constants test 3"] = (VarF2Dot14.PACKED_SIZE == 6)
testResults["VarF2Dot14 constants test 4"] = (list(VarF2Dot14.FIELDS.keys()) == ["scalar", "varOuterIndex", "varInnerIndex"])
testResults["VarF2Dot14 constants test 5"] = (list(VarF2Dot14.FIELDS.values()) == [F2Dot14, uint16, uint16])

# constructor args
try:
    x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), uint16(4))
except:
    result = True
else:
    result = False
testResults["VarF2Dot14 constructor test 1"] = result
try:
    x = VarF2Dot14(0x6000, uint16(4), uint16(7))
except:
    result = True
else:
    result = False
testResults["VarF2Dot14 constructor test 2"] = result

x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), uint16(1), uint16(3))
testResults["VarF2Dot14 constructor test 3"] = (type(x.scalar) == F2Dot14 and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
testResults["VarF2Dot14 constructor test 4"] = (x.scalar == 1.5 and x.varOuterIndex == 1 and x.varInnerIndex == 3)

result = x.__repr__() == "{'scalar': 1.5, 'varOuterIndex': 1, 'varInnerIndex': 3}"
testResults["VarF2Dot14 __repr__ test"] = result

buffer = b'\x60\x00\x00\xa0\x00\xa1\xf0\xf0'
x = tryReadFixedLengthStructFromBuffer(buffer, VarF2Dot14)
result = type(x) == VarF2Dot14
result &= (type(x.scalar) == F2Dot14 and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
result &= (x.scalar == 1.5 and x.varOuterIndex == 160 and x.varInnerIndex == 161)
testResults["VarF2Dot14 tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for VarFWord
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(VarFWord)
except:
    result = False
else:
    result = True
testResults["VarFWord definition test"] = result

testResults["VarFWord constants test 1"] = (VarFWord.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["VarFWord constants test 2"] = (VarFWord.PACKED_FORMAT == (FWord.PACKED_FORMAT + "HH"))
testResults["VarFWord constants test 3"] = (VarFWord.PACKED_SIZE == 6)
testResults["VarFWord constants test 4"] = (list(VarFWord.FIELDS.keys()) == ["coordinate", "varOuterIndex", "varInnerIndex"])
testResults["VarFWord constants test 5"] = (list(VarFWord.FIELDS.values()) == [FWord, uint16, uint16])

# constructor args
try:
    x = VarFWord(FWord(24), uint16(17))
except:
    result = True
else:
    result = False
testResults["VarFWord constructor test 1"] = result
try:
    x = VarFWord(24.0, uint16(17), uint16(23))
except:
    result = True
else:
    result = False
testResults["VarFWord constructor test 2"] = result

x = VarFWord(FWord(-24), uint16(17), uint16(23))
testResults["VarFWord constructor test 3"] = (type(x) == VarFWord and type(x.coordinate) == FWord and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
testResults["VarFWord constructor test 4"] = (x.coordinate == -24 and x.varOuterIndex == 17 and x.varInnerIndex == 23)

testResults["VarFWord __repr__ test"] = (x.__repr__() == "{'coordinate': -24, 'varOuterIndex': 17, 'varInnerIndex': 23}")

buffer = b'\x01\x00\x00\xa0\x00\xa1\xf0\xf0'
x = tryReadFixedLengthStructFromBuffer(buffer, VarFWord)
result = type(x) == VarFWord
result &= (type(x.coordinate) == FWord and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
result &= (x.coordinate == 256 and x.varOuterIndex == 160 and x.varInnerIndex == 161)
testResults["VarFWord tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for VarUFWord
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(VarUFWord)
except:
    result = False
else:
    result = True
testResults["VarUFWord definition test"] = result

testResults["VarUFWord constants test 1"] = (VarUFWord.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["VarUFWord constants test 2"] = (VarUFWord.PACKED_FORMAT == (UFWord.PACKED_FORMAT + "HH"))
testResults["VarUFWord constants test 3"] = (VarUFWord.PACKED_SIZE == 6)
testResults["VarUFWord constants test 4"] = (list(VarUFWord.FIELDS.keys()) == ["distance", "varOuterIndex", "varInnerIndex"])
testResults["VarUFWord constants test 5"] = (list(VarUFWord.FIELDS.values()) == [UFWord, uint16, uint16])

# constructor args
try:
    x = VarUFWord(UFWord(24), uint16(17))
except:
    result = True
else:
    result = False
testResults["VarUFWord constructor test 1"] = result
try:
    x = VarUFWord(24, uint16(17), uint16(23))
except:
    result = True
else:
    result = False
testResults["VarUFWord constructor test 2"] = result

x = VarUFWord(UFWord(24), uint16(17), uint16(23))
testResults["VarUFWord constructor test 3"] = (type(x) == VarUFWord and type(x.distance) == UFWord and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
testResults["VarUFWord constructor test 4"] = (x.distance == 24 and x.varOuterIndex == 17 and x.varInnerIndex == 23)

testResults["VarUFWord __repr__ test"] = (x.__repr__() == "{'distance': 24, 'varOuterIndex': 17, 'varInnerIndex': 23}")

buffer = b'\x01\x00\x00\xa0\x00\xa1\xf0\xf0'
x = tryReadFixedLengthStructFromBuffer(buffer, VarUFWord)
result = type(x) == VarUFWord
result &= (type(x.distance) == UFWord and type(x.varOuterIndex) == uint16 and type(x.varInnerIndex) == uint16)
result &= (x.distance == 256 and x.varOuterIndex == 160 and x.varInnerIndex == 161)
testResults["VarUFWord tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for Affine2x2
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(Affine2x2)
except:
    result = False
else:
    result = True
testResults["Affine2x2 definition test"] = result

testResults["Affine2x2 constants test 1"] = (Affine2x2.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT)
testResults["Affine2x2 constants test 2"] = (Affine2x2.PACKED_FORMAT == ">4sHH4sHH4sHH4sHH")
testResults["Affine2x2 constants test 3"] = (Affine2x2.PACKED_SIZE == (VarFixed.PACKED_SIZE * 4))
testResults["Affine2x2 constants test 4"] = (list(Affine2x2.FIELDS.keys()) == ["xx", "xy", "yx", "yy"])
testResults["Affine2x2 constants test 5"] = (list(Affine2x2.FIELDS.values()) == [VarFixed, VarFixed, VarFixed, VarFixed])

# constructor args
x = VarFixed(Fixed.createFixedFromUint32(0x1_8000), uint16(2), uint16(17))
try:
    y = Affine2x2(x, x, x)
except:
    result = True
else:
    result = False
testResults["Affine2x2 constructor test 1"] = result
try:
    y = Affine2x2(x, x, x, 24)
except:
    result = True
else:
    result = False
testResults["Affine2x2 constructor test 2"] = result

y = Affine2x2(x, x, x, x)
result = (type(y) == Affine2x2 and type(y.xx) == VarFixed and type(y.xy) == VarFixed and type(y.yx) == VarFixed and type(y.yy) == VarFixed)
testResults["Affine2x2 constructor test 3"] = result
result = (y.xx.scalar._rawBytes == b'\x00\01\x80\x00' and y.xx.varOuterIndex == 2 and y.xx.varInnerIndex == 17)
testResults["Affine2x2 constructor test 4"] = result

result = (y.__repr__() == "{'xx': {'scalar': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}, 'xy': {'scalar': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}, 'yx': {'scalar': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}, 'yy': {'scalar': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}}")
testResults["Affine2x2 __repr__ test"] = result

buffer = (b'\x01\x00\x50\x00\x00\xa0\x00\xb0'
          b'\x01\x01\x50\x00\x00\xa1\x00\xb1'
          b'\x01\x02\x50\x00\x00\xa2\x00\xb2'
          b'\x01\x03\x50\x00\x00\xa3\x00\xb3'
          b'\xf0\xf0')
x = tryReadFixedLengthStructFromBuffer(buffer, Affine2x2)
result = type(x) == Affine2x2
result &= (type(x.xx) == VarFixed and type(x.xy) == VarFixed and type(x.yx) == VarFixed and type (x.yy) == VarFixed)
y = x.xx
result &= (y.scalar == 256.3125 and y.varOuterIndex == 160 and y.varInnerIndex == 176)
y = x.xy
result &= (y.scalar == 257.3125 and y.varOuterIndex == 161 and y.varInnerIndex == 177)
y = x.yx
result &= (y.scalar == 258.3125 and y.varOuterIndex == 162 and y.varInnerIndex == 178)
y = x.yy
result &= (y.scalar == 259.3125 and y.varOuterIndex == 163 and y.varInnerIndex == 179)
testResults["Affine2x2 tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for ColorIndex
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(ColorIndex)
except:
    result = False
else:
    result = True
testResults["ColorIndex definition test"] = result

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
testResults["ColorIndex constructor test 1"] = result
try:
    y = ColorIndex(uint16(24), 42)
except:
    result = True
else:
    result = False
testResults["ColorIndex constructor test 2"] = result
try:
    y = ColorIndex(24.0, x)
except:
    result = True
else:
    result = False
testResults["ColorIndex constructor test 3"] = result

# alpha out of range [0, 1]
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), uint16(1), uint16(3))
try:
    y = ColorIndex(uint16(24), x)
except ValueError:
    result = True
else:
    result = False
testResults["ColorIndex constructor test 4"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x8000), uint16(1), uint16(3))
try:
    y = ColorIndex(uint16(24), x)
except ValueError:
    result = True
else:
    result = False
testResults["ColorIndex constructor test 5"] = result

# good args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(1), uint16(3))
y = ColorIndex(uint16(24), x)
testResults["ColorIndex constructor test 6"] = (type(y.paletteIndex) == uint16 and type(y.alpha) == VarF2Dot14)
testResults["ColorIndex test constructor 7"] = (y.paletteIndex == 24 and y.alpha.scalar == 0.75 and y.alpha.varOuterIndex == 1 and y.alpha.varInnerIndex == 3)

x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(1), uint16(3))
y = ColorIndex(uint16(24), x)
result = y.__repr__() == "{'paletteIndex': 24, 'alpha': {'scalar': 0.75, 'varOuterIndex': 1, 'varInnerIndex': 3}}"
testResults["ColorIndex __repr__ test"] = result

buffer = b'\x01\x03\x30\x00\x00\xa0\x00\xa1\xf0\xf0'
x = tryReadFixedLengthStructFromBuffer(buffer, ColorIndex)
result = type(x) == ColorIndex
result &= (type(x.paletteIndex) == uint16 and type(x.alpha) == VarF2Dot14)
result &= (x.paletteIndex == 259 and x.alpha.scalar == 0.75 and x.alpha.varOuterIndex == 160 and x.alpha.varInnerIndex == 161)
testResults["ColorIndex tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for ColorStop
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(ColorIndex)
except:
    result = False
else:
    result = True
testResults["ColorStop definition test"] = result

testResults["ColorStop constants test 1"] = (ColorStop.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT)
testResults["ColorStop constants test 2"] = (ColorStop.PACKED_FORMAT == ">2sHHH2sHH")
testResults["ColorStop constants test 3"] = (ColorStop.PACKED_SIZE == 14)
testResults["ColorStop constants test 4"] = (list(ColorStop.FIELDS.keys()) == ["stopOffset", "color"])
testResults["ColorStop constants test 5"] = (list(ColorStop.FIELDS.values()) == [VarF2Dot14, ColorIndex])

# constructor arg validations
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(1), uint16(3))
y = ColorIndex(uint16(24), x)
try:
    z = ColorStop(x)
except:
    result = True
else:
    result = False
testResults["ColorStop constructor test 1"] = result
try:
    z = ColorStop(24, y)
except:
    result = True
else:
    result = False
testResults["ColorStop constructor test 2"] = result
try:
    z = ColorStop(x, 24)
except:
    result = True
else:
    result = False
testResults["ColorStop constructor test 3"] = result

# stopOffset out of range [0, 1]
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x4001), uint16(1), uint16(3))
try:
    z = ColorStop(x, y)
except ValueError:
    result = True
else:
    result = False
testResults["ColorStop constructor test 4"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0xC001), uint16(1), uint16(3))
try:
    z = ColorStop(x, y)
except ValueError:
    result = True
else:
    result = False
testResults["ColorStop constructor test 5"] = result

# good args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x1000), uint16(1), uint16(3))
y = ColorIndex(uint16(24), x)
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(0), uint16(4))
z = ColorStop(x, y)
testResults["ColorStop constructor test 6"] = (type(z.stopOffset) == VarF2Dot14 and type(z.color) == ColorIndex)
testResults["ColorStop constructor test 7"] = (z.stopOffset.scalar == 0.75 and z.stopOffset.varOuterIndex == 0 and z.stopOffset.varInnerIndex == 4)
testResults["ColorStop constructor test 8"] = (z.color.paletteIndex == 24 and z.color.alpha.scalar == 0.25 and z.color.alpha.varOuterIndex == 1 and y.alpha.varInnerIndex == 3)

result = z.__repr__() == "{'stopOffset': {'scalar': 0.75, 'varOuterIndex': 0, 'varInnerIndex': 4}, 'color': {'paletteIndex': 24, 'alpha': {'scalar': 0.25, 'varOuterIndex': 1, 'varInnerIndex': 3}}}"
testResults["ColorStop __repr__ test"] = result

buffer = b'\x30\x00\x00\xa0\x00\xa1\x00\x11\x30\x00\x00\xb0\x00\xb1\xf0\xf0'
x = tryReadFixedLengthStructFromBuffer(buffer, ColorStop)
result = type(x) == ColorStop
result &= (type(x.stopOffset) == VarF2Dot14 and type(x.color) == ColorIndex)
result &= (x.stopOffset.scalar == 0.75 and x.stopOffset.varOuterIndex == 160 and x.stopOffset.varInnerIndex == 161)
result &= (x.color.paletteIndex == 17 and x.color.alpha.scalar == 0.75
           and x.color.alpha.varOuterIndex == 176 and x.color.alpha.varInnerIndex == 177)
testResults["ColorStop tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for ColorLine
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(ColorLine)
except:
    result = False
else:
    result = True
testResults["ColorLine definition test"] = result

testResults["ColorLine constants test 1"] = (ColorLine.TYPE_CATEGORY == otTypeCategory.VAR_LENGTH_STRUCT)
testResults["ColorLine constants test 2"] = (ColorLine.PACKED_FORMAT == ">HH")
testResults["ColorLine constants test 3"] = (ColorLine.PACKED_SIZE == 4)
testResults["ColorLine constants test 4"] = (list(ColorLine.FIELDS.keys()) == ["extend", "numStops"])
testResults["ColorLine constants test 5"] = (list(ColorLine.FIELDS.values()) == [uint16, uint16])
testResults["ColorLine constants test 6"] = (ColorLine.ALL_FIELD_NAMES == ["extend", "numStops", "colorStops"])
testResults["ColorLine constants test 7"] = getCombinedFieldTypes(ColorLine) == [uint16, uint16, list]

# constructor args
buffer = b'\x30\x00\x00\xa0\x00\xa1\x00\x11\x30\x00\x00\xb0\x00\xb1\xf0\xf0'
x = tryReadFixedLengthStructFromBuffer(buffer, ColorStop)

try:
    y = ColorLine(uint16(1), uint16(2))
except TypeError:
    result = True
else:
    result = False
testResults["ColorLine constructor test 1"] = result

try:
    y = ColorLine(1, uint16(2), [x, x])
except TypeError:
    result = True
else:
    result = False
testResults["ColorLine constructor test 2"] = result

try:
    y = ColorLine(uint16(1), 2, [x, x])
except TypeError:
    result = True
else:
    result = False
testResults["ColorLine constructor test 3"] = result

try:
    y = ColorLine(uint16(1), uint16(2), (x, x))
except TypeError:
    result = True
else:
    result = False
testResults["ColorLine constructor test 4"] = result

y = ColorLine(uint16(1), uint16(2), [x, x])
result = (type(y) == ColorLine and type(y.extend) == uint16 and type(y.numStops) == uint16 and type(y.colorStops) == list)
result &= y.extend == 1 and y.numStops == 2
result &= len(y.colorStops) == 2 and type(y.colorStops[0]) == ColorStop
z = y.colorStops[0]
result &= z.stopOffset.scalar == 0.75 and z.stopOffset.varOuterIndex == 160 and z.stopOffset.varInnerIndex == 161
result &= (z.color.paletteIndex == 17 and z.color.alpha.scalar == 0.75 
           and z.color.alpha.varOuterIndex == 176 and z.color.alpha.varInnerIndex == 177)
testResults["ColorLine constructor test 5"] = result


buffer = (b'\x00\x01\x00\x02' 
          b'\x30\x00\x00\xa0\x00\xa1\x00\x11\x30\x00\x00\xb0\x00\xb1'
          b'\x30\x00\x00\xa0\x00\xa1\x00\x11\x30\x00\x00\xb0\x00\xb1'
          b'\xf0\xf0')
y = tryReadVarLengthStructFromBuffer(buffer, ColorLine)
result = (type(y) == ColorLine and type(y.extend) == uint16 and type(y.numStops) == uint16 and type(y.colorStops) == list)
result &= y.extend == 1 and y.numStops == 2
result &= len(y.colorStops) == 2 and type(y.colorStops[0]) == ColorStop
z = y.colorStops[0]
result &= z.stopOffset.scalar == 0.75 and z.stopOffset.varOuterIndex == 160 and z.stopOffset.varInnerIndex == 161
result &= (z.color.paletteIndex == 17 and z.color.alpha.scalar == 0.75 
           and z.color.alpha.varOuterIndex == 176 and z.color.alpha.varInnerIndex == 177)
testResults["ColorLine tryReadFixedLengthStructFromBuffer test 1"] = result

buffer = (b'\x00\x00' b'\x00\x02' 
          b'\x10\x00\x00\x02\x03\x00\x00\x15\x01\x00\x00\x03\x00\x07'
          b'\x38\x00\x01\x21\x00\xc2\x01\x42\x00\xff\x0d\x34\x21\x22')
# extend: \x00\x00
# numStops: \x00\x02
# ColorStop 0: \x10\x00 \x00\x02 \x03\x00 + \x00\x15 \x01\x00 \x00\x03 \x00\x07
# ColorStop 1: \x38\x00 \x01\x21 \x00\xc2 + \x01\x42 \x00\xff \x0d\x34 \x21\x22
x = tryReadVarLengthStructFromBuffer(buffer, ColorLine)
result = (x.extend == 0 and x.numStops == 2)

y = x.colorStops[0]
result &= (y.stopOffset.scalar == 0.25 and y.stopOffset.varOuterIndex == 2 and y.stopOffset.varInnerIndex == 0x300)
result &= (y.color.paletteIndex == 21 and y.color.alpha.scalar._rawBytes == b'\x01\x00' and y.color.alpha.varOuterIndex == 3 and y.color.alpha.varInnerIndex == 7)

y = x.colorStops[1]
result &= (y.stopOffset.scalar == 0.875 and y.stopOffset.varOuterIndex == 0x121 and y.stopOffset.varInnerIndex == 0xc2)
result &= (y.color.paletteIndex == 0x142 and y.color.alpha.scalar._rawBytes == b'\x00\xff' and y.color.alpha.varOuterIndex == 0xd34 and y.color.alpha.varInnerIndex == 0x2122)

testResults["ColorLine tryReadFixedLengthStructFromBuffer test 2"] = result


#-------------------------------------------------------------
# tests for PaintFormat1
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(PaintFormat1)
except:
    result = False
else:
    result = True
testResults["ColorStop definition test"] = result

testResults["PaintFormat1 constants test 1"] = (PaintFormat1.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT)
testResults["PaintFormat1 constants test 2"] = (PaintFormat1.PACKED_FORMAT == ">HH2sHH")
testResults["PaintFormat1 constants test 3"] = (PaintFormat1.PACKED_SIZE == 10)
testResults["PaintFormat1 constants test 4"] = (list(PaintFormat1.FIELDS.keys()) == ["format", "color"])
testResults["PaintFormat1 constants test 5"] = (list(PaintFormat1.FIELDS.values()) == [uint16, ColorIndex])

# constructor args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(1), uint16(3))
y = ColorIndex(uint16(24), x)
try:
    z = PaintFormat1(uint16(1))
except:
    result = True
else:
    result = False
testResults["PaintFormat1 constructor test 1"] = result
try:
    z = PaintFormat1(uint16(1), 42)
except:
    result = True
else:
    result = False
testResults["PaintFormat1 constructor test 2"] = result
try:
    z = PaintFormat1(24.0, y)
except:
    result = True
else:
    result = False
testResults["PaintFormat1 constructor test 3"] = result

# wrong format
try:
    z = PaintFormat1(uint16(2), y)
except ValueError:
    result = True
else:
    result = False
testResults["PaintFormat1 constructor test 4"] = result

# good args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), uint16(1), uint16(3))
y = ColorIndex(uint16(24), x)
z = PaintFormat1(uint16(1), y)

result = (type(z.format) == uint16 and type(z.color) == ColorIndex)
y = z.color
result &= (y.paletteIndex == 24 and y.alpha.scalar == 0.75 and y.alpha.varOuterIndex == 1 and y.alpha.varInnerIndex == 3)
testResults["PaintFormat1 test constructor 5"] = result

result = y.__repr__() == "{'paletteIndex': 24, 'alpha': {'scalar': 0.75, 'varOuterIndex': 1, 'varInnerIndex': 3}}"
testResults["PaintFormat1 __repr__ test"] = result

buffer = (b'\x00\x01'
          b'\x01\x03' b'\x30\x00\x00\xa0\x00\xa1'
          b'\xf0\xf0')
x = tryReadFixedLengthStructFromBuffer(buffer, PaintFormat1)
result = type(x) == PaintFormat1
result &= (type(x.format) == uint16 and type(x.color) == ColorIndex)
result &= x.format == 1
y = x.color
result &= (y.paletteIndex == 259 and y.alpha.scalar == 0.75 and y.alpha.varOuterIndex == 160 and y.alpha.varInnerIndex == 161)
testResults["PaintFormat1 tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for PaintFormat2
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(PaintFormat2)
except:
    result = False
else:
    result = True
testResults["PaintFormat2 definition test"] = result

testResults["PaintFormat2 constants test 1"] = (PaintFormat2.TYPE_CATEGORY == otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES)
testResults["PaintFormat2 constants test 2"] = (PaintFormat2.PACKED_FORMAT == ">HLhHHhHHhHHhHHhHHhHH")
testResults["PaintFormat2 constants test 3"] = (PaintFormat2.PACKED_SIZE == 42)
testResults["PaintFormat2 constants test 4"] = (list(PaintFormat2.FIELDS.keys()) == ["format", "colorLineOffset", "x0", "y0", "x1", "y1", "x2", "y2"])
testResults["PaintFormat2 constants test 5"] = (list(PaintFormat2.FIELDS.values()) == [uint16, Offset32, VarFWord, VarFWord, VarFWord, VarFWord, VarFWord, VarFWord])
testResults["PaintFormat2 constants test 6"] = (PaintFormat2.ALL_FIELD_NAMES == ["format", "colorLineOffset", "x0", "y0", "x1", "y1", "x2", "y2", "colorLine"])
testResults["PaintFormat2 constants test 7"] = getCombinedFieldTypes(PaintFormat2) == [uint16, Offset32, VarFWord, VarFWord, VarFWord, VarFWord, VarFWord, VarFWord, ColorLine]

# constructor args
buffer = b'\x01\x00\x00\xa0\x00\xa1\xf0\xf0'
x = tryReadFixedLengthStructFromBuffer(buffer, VarFWord)

buffer = (b'\x00\x00' b'\x00\x02' 
          b'\x10\x00\x00\x02\x03\x00\x00\x15\x01\x00\x00\x03\x00\x07'
          b'\x38\x00\x01\x21\x00\xc2\x01\x42\x00\xff\x0d\x34\x21\x22')
# extend: \x00\x00
# numStops: \x00\x02
# ColorStop 0: \x10\x00 \x00\x02 \x03\x00 + \x00\x15 \x01\x00 \x00\x03 \x00\x07
# ColorStop 1: \x38\x00 \x01\x21 \x00\xc2 + \x01\x42 \x00\xff \x0d\x34 \x21\x22
y = tryReadVarLengthStructFromBuffer(buffer, ColorLine)

try:
    z = PaintFormat2(uint16(2), Offset32(0), x, x, x, x, x, x)
except:
    result = True
else:
    result = False
testResults["PaintFormat2 constructor test 1"] = result

try:
    z = PaintFormat2(2, Offset32(0), x, x, x, x, x, x, y)
except:
    result = True
else:
    result = False
testResults["PaintFormat2 constructor test 2"] = result

try:
    z = PaintFormat2(uint16(2), 0, x, x, x, x, x, x, y)
except:
    result = True
else:
    result = False
testResults["PaintFormat2 constructor test 3"] = result

try:
    z = PaintFormat2(uint16(2), Offset32(0), 2, x, x, x, x, x, y)
except:
    result = True
else:
    result = False
testResults["PaintFormat2 constructor test 4"] = result

# good args
z = PaintFormat2(uint16(2), Offset32(0), x, x, x, x, x, x, y)
result = True
for f in z.ALL_FIELD_NAMES:
    result &= hasattr(z, f)
result &= type(z.format) == uint16 and type(z.colorLineOffset) == Offset32
result &= (type(z.x0) == VarFWord and type(z.y0) == VarFWord 
           and type(z.x1) == VarFWord and type(z.y1) == VarFWord
           and type(z.x2) == VarFWord and type(z.y2) == VarFWord
           and type(z.colorLine) == ColorLine)
result &= z.format == 2 and z.colorLineOffset == 0

x = z.x0
result &= (x.coordinate == 256 and x.varOuterIndex == 160 and x.varInnerIndex == 161)

x = z.colorLine
result = (x.extend == 0 and x.numStops == 2)

y = x.colorStops[0]
result &= (y.stopOffset.scalar == 0.25 and y.stopOffset.varOuterIndex == 2 and y.stopOffset.varInnerIndex == 0x300)
result &= (y.color.paletteIndex == 21 and y.color.alpha.scalar._rawBytes == b'\x01\x00' and y.color.alpha.varOuterIndex == 3 and y.color.alpha.varInnerIndex == 7)

y = x.colorStops[1]
result &= (y.stopOffset.scalar == 0.875 and y.stopOffset.varOuterIndex == 0x121 and y.stopOffset.varInnerIndex == 0xc2)
result &= (y.color.paletteIndex == 0x142 and y.color.alpha.scalar._rawBytes == b'\x00\xff' and y.color.alpha.varOuterIndex == 0xd34 and y.color.alpha.varInnerIndex == 0x2122)

testResults["PaintFormat2 constructor test 5"] = result


buffer = (b'\x00\x02' b'\x00\x00\x00\x2a'
          b'\x01\x00\x00\xa0\x00\xa1'
          b'\x01\x00\x00\xa0\x00\xa1'
          b'\x01\x00\x00\xa0\x00\xa1'
          b'\x01\x00\x00\xa0\x00\xa1'
          b'\x01\x00\x00\xa0\x00\xa1'
          b'\x01\x00\x00\xa0\x00\xa1'
          b'\x00\x00' b'\x00\x02' 
            b'\x10\x00\x00\x02\x03\x00\x00\x15\x01\x00\x00\x03\x00\x07'
            b'\x38\x00\x01\x21\x00\xc2\x01\x42\x00\xff\x0d\x34\x21\x22')
x = tryReadVarLengthStructWithSubtablesFromBuffer(buffer, PaintFormat2)
result = type(x) == PaintFormat2
for f in x.ALL_FIELD_NAMES:
    result &= hasattr(x, f)
result &= type(x.format) == uint16 and type(x.colorLineOffset) == Offset32
result &= (type(x.x0) == VarFWord and type(x.y0) == VarFWord 
           and type(x.x1) == VarFWord and type(x.y1) == VarFWord
           and type(x.x2) == VarFWord and type(x.y2) == VarFWord
           and type(x.colorLine) == ColorLine)
result &= x.format == 2 and x.colorLineOffset == 42

y = x.x0
result &= (y.coordinate == 256 and y.varOuterIndex == 160 and y.varInnerIndex == 161)

y = x.colorLine
result = (y.extend == 0 and y.numStops == 2)

z = y.colorStops[0]
result &= (z.stopOffset.scalar == 0.25 and z.stopOffset.varOuterIndex == 2 and z.stopOffset.varInnerIndex == 0x300)
result &= (z.color.paletteIndex == 21 and z.color.alpha.scalar._rawBytes == b'\x01\x00' and z.color.alpha.varOuterIndex == 3 and z.color.alpha.varInnerIndex == 7)

z = y.colorStops[1]
result &= (z.stopOffset.scalar == 0.875 and z.stopOffset.varOuterIndex == 0x121 and z.stopOffset.varInnerIndex == 0xc2)
result &= (z.color.paletteIndex == 0x142 and z.color.alpha.scalar._rawBytes == b'\x00\xff' and z.color.alpha.varOuterIndex == 0xd34 and z.color.alpha.varInnerIndex == 0x2122)

testResults["PaintFormat2 tryReadVarLengthStructWithSubtablesFromBuffer test "] = result



#-------------------------------------------------------------
# tests for PaintFormat3
#-------------------------------------------------------------



#-------------------------------------------------------------
# tests for BaseGlyphRecord
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(BaseGlyphRecord)
except:
    result = False
else:
    result = True
testResults["BaseGlyphRecord definition test"] = result

testResults["BaseGlyphRecord constants test 1"] = (BaseGlyphRecord.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["BaseGlyphRecord constants test 2"] = (BaseGlyphRecord.PACKED_FORMAT == ">HHH")
testResults["BaseGlyphRecord constants test 3"] = (BaseGlyphRecord.PACKED_SIZE == 6)
testResults["BaseGlyphRecord constants test 5"] = (list(BaseGlyphRecord.FIELDS.keys()) == ["glyphID", "firstLayerIndex", "numLayers"])
testResults["BaseGlyphRecord constants test 6"] = (list(BaseGlyphRecord.FIELDS.values()) == [uint16, uint16, uint16])

# constructor args
try:
    x = BaseGlyphRecord(uint16(2), uint16(4))
except:
    result = True
else:
    result = False
testResults["BaseGlyphRecord constructor test 1"] = result
try:
    x = BaseGlyphRecord(2.0, uint16(4), uint16(17))
except:
    result = True
else:
    result = False
testResults["BaseGlyphRecord constructor test 2"] = result

x = BaseGlyphRecord(uint16(2), uint16(4), uint16(17))
result = (type(x) == BaseGlyphRecord)
for f in BaseGlyphRecord.FIELDS:
    result &= hasattr(x, f)
result &= (x.glyphID == 2 and x.firstLayerIndex == 4 and x.numLayers == 17)
testResults["BaseGlyphRecord constructor test 3"] = result

buffer = b'\x00\x02\x00\x04\x00\x11'
x = tryReadFixedLengthStructFromBuffer(buffer, BaseGlyphRecord)
result = (type(x) == BaseGlyphRecord)
for f in BaseGlyphRecord.FIELDS:
    result &= hasattr(x, f)
result &= (x.glyphID == 2 and x.firstLayerIndex == 4 and x.numLayers == 17)
testResults["BaseGlyphRecord tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for LayerRecord
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(LayerRecord)
except:
    result = False
else:
    result = True
testResults["LayerRecord definition test"] = result

testResults["LayerRecord constants test 1"] = (LayerRecord.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["LayerRecord constants test 2"] = (LayerRecord.PACKED_FORMAT == ">HH")
testResults["LayerRecord constants test 3"] = (LayerRecord.PACKED_SIZE == 4)
testResults["LayerRecord constants test 4"] = (list(LayerRecord.FIELDS.keys()) == ["glyphID", "paletteIndex"])
testResults["LayerRecord constants test 5"] = (list(LayerRecord.FIELDS.values()) == [uint16, uint16])

# constructor args
try:
    x = LayerRecord(uint16(2))
except:
    result = True
else:
    result = False
testResults["LayerRecord constructor test 1"] = result
try:
    x = LayerRecord(2.0, uint16(17))
except:
    result = True
else:
    result = False
testResults["LayerRecord constructor test 2"] = result

x = LayerRecord(uint16(2), uint16(17))
result = (type(x) == LayerRecord)
for f in LayerRecord.FIELDS:
    result &= hasattr(x, f)
result &= (x.glyphID == 2 and x.paletteIndex == 17)
testResults["LayerRecord constructor test 3"] = result

buffer = b'\x00\x02\x00\x11'
x = tryReadFixedLengthStructFromBuffer(buffer, LayerRecord)
result = (type(x) == LayerRecord)
for f in LayerRecord.FIELDS:
    result &= hasattr(x, f)
result &= (x.glyphID == 2 and x.paletteIndex == 17)
testResults["LayerRecord tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for BaseGlyphV1Record
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(BaseGlyphV1Record)
except:
    result = False
else:
    result = True
testResults["BaseGlyphV1Record definition test"] = result

testResults["BaseGlyphV1Record constants test 1"] = (BaseGlyphV1Record.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["BaseGlyphV1Record constants test 2"] = (BaseGlyphV1Record.PACKED_FORMAT == ">HL")
testResults["BaseGlyphV1Record constants test 3"] = (BaseGlyphV1Record.PACKED_SIZE == 6)
testResults["BaseGlyphV1Record constants test 4"] = (list(BaseGlyphV1Record.FIELDS.keys()) == ["glyphID", "layersV1Offset"])
testResults["BaseGlyphV1Record constants test 5"] = (list(BaseGlyphV1Record.FIELDS.values()) == [uint16, Offset32])

try:
    x = BaseGlyphV1Record(uint16(2))
except TypeError:
    result = True
else:
    result = False
testResults["BaseGlyphV1Record constructor test 1"] = result
try:
    x = BaseGlyphV1Record(2.0, Offset32(17))
except TypeError:
    result = True
else:
    result = False
testResults["BaseGlyphV1Record constructor test 2"] = result

x = BaseGlyphV1Record(uint16(2), Offset32(17))
result = (type(x) == BaseGlyphV1Record)
for f in BaseGlyphV1Record.FIELDS:
    result &= hasattr(x, f)
result &= (x.glyphID == 2 and x.layersV1Offset == 17)
testResults["BaseGlyphV1Record constructor test 3"] = result

buffer = b'\x00\x02\x00\x00\x00\x11'
x = tryReadFixedLengthStructFromBuffer(buffer, BaseGlyphV1Record)
result = (type(x) == BaseGlyphV1Record)
for f in BaseGlyphV1Record.FIELDS:
    result &= hasattr(x, f)
result &= (x.glyphID == 2 and x.layersV1Offset == 17)
testResults["BaseGlyphV1Record tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for LayerV1Record
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(LayerV1Record)
except:
    result = False
else:
    result = True
testResults["LayerV1Record definition test"] = result

testResults["LayerV1Record constants test 1"] = (LayerV1Record.TYPE_CATEGORY == otTypeCategory.FIXED_LENGTH_BASIC_STRUCT)
testResults["LayerV1Record constants test 2"] = (LayerV1Record.PACKED_FORMAT == ">HL")
testResults["LayerV1Record constants test 3"] = (LayerV1Record.PACKED_SIZE == 6)
testResults["LayerV1Record constants test 4"] = (list(LayerV1Record.FIELDS.keys()) == ["glyphID", "paintOffset"])
testResults["LayerV1Record constants test 5"] = (list(LayerV1Record.FIELDS.values()) == [uint16, Offset32])

try:
    x = LayerV1Record(uint16(2))
except:
    result = True
else:
    result = False
testResults["LayerV1Record constructor test 1"] = result
try:
    x = LayerV1Record(2.0, Offset32(17))
except:
    result = True
else:
    result = False
testResults["LayerV1Record constructor test 2"] = result

x = LayerV1Record(uint16(2), Offset32(17))
result = (type(x) == LayerV1Record)
for f in LayerV1Record.FIELDS:
    result &= hasattr(x, f)
result &= (x.glyphID == 2 and x.paintOffset == 17)
testResults["LayerV1Record constructor test 3"] = result

buffer = b'\x00\x02\x00\x00\x00\x11'
x = tryReadFixedLengthStructFromBuffer(buffer, LayerV1Record)
result = (type(x) == LayerV1Record)
for f in LayerV1Record.FIELDS:
    result &= hasattr(x, f)
result &= (x.glyphID == 2 and x.paintOffset == 17)
testResults["LayerV1Record tryReadFixedLengthStructFromBuffer test"] = result



#-------------------------------------------------------------
# tests for LayersV1
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(LayersV1)
except:
    result = False
else:
    result = True
testResults["LayersV1 definition test"] = result

testResults["LayersV1 constants test 1"] = (LayersV1.TYPE_CATEGORY == otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES)
testResults["LayersV1 constants test 2"] = (LayersV1.PACKED_FORMAT == ">L")
testResults["LayersV1 constants test 3"] = (LayersV1.PACKED_SIZE == 4)
testResults["LayersV1 constants test 4"] = (list(LayersV1.FIELDS.keys()) == ["numLayerV1Records"])
testResults["LayersV1 constants test 5"] = (list(LayersV1.FIELDS.values()) == [uint32])
testResults["LayersV1 constants test 6"] = (LayersV1.ALL_FIELD_NAMES == ["numLayerV1Records", "layerV1Records", "paintTables"])
testResults["LayersV1 constants test 7"] = getCombinedFieldTypes(LayersV1) == [uint32, list, list]

# constructor args

buffer = b'\x00\x01\x00\x00\x00\x11'
x = tryReadFixedLengthStructFromBuffer(buffer, LayerV1Record)

buffer = (b'\x00\x01' b'\x01\x03' b'\x30\x00\x00\xa0\x00\xa1')
y = tryReadFixedLengthStructFromBuffer(buffer, PaintFormat1)

try:
    z = LayersV1(uint16(1), [x])
except TypeError:
    result = True
else:
    result = False
testResults["LayersV1 constructor test 1"] = result

try:
    z = LayersV1(1, [x], [y])
except TypeError:
    result = True
else:
    result = False
testResults["LayersV1 constructor test 2"] = result

try:
    z = LayersV1(uint16(1), x, [y])
except TypeError:
    result = True
else:
    result = False
testResults["LayersV1 constructor test 3"] = result

try:
    z = LayersV1(uint16(1), [x], y)
except TypeError:
    result = True
else:
    result = False
testResults["LayersV1 constructor test 4"] = result

# good args
z = LayersV1(uint32(1), [x], [y])
result = type(z) == LayersV1
for n in z.ALL_FIELD_NAMES:
    result &= hasattr(z, n)
result &= (type(z.numLayerV1Records) == uint32 and type(z.layerV1Records) == list and type(z.paintTables) == list)
result &= z.numLayerV1Records == 1
result &= len(z.layerV1Records) == 1 and type(z.layerV1Records[0]) == LayerV1Record
result &= len(z.paintTables) == 1 and type(z.paintTables[0]) == PaintFormat1

x = z.layerV1Records[0]
result &= x.glyphID == 1 and x.paintOffset == 17
y = z.paintTables[0]
result &= y.format == 1 and y.color.paletteIndex == 259
result &= y.color.alpha.scalar == 0.75 and y.color.alpha.varOuterIndex == 160 and y.color.alpha.varInnerIndex == 161
testResults["LayersV1 constructor test 5"] = result


buffer = (b'\x00\x00\x00\x01'
            b'\x00\x01\x00\x00\x00\x0a'
            b'\x00\x01' b'\x01\x03' b'\x30\x00\x00\xa0\x00\xa1')
x = tryReadStructWithSubtablesFromBuffer(buffer, LayersV1)
result = type(x) == LayersV1
for n in x.ALL_FIELD_NAMES:
    result &= hasattr(x, n)
result &= (type(x.numLayerV1Records) == uint32 and type(x.layerV1Records) == list and type(x.paintTables) == list)
result &= x.numLayerV1Records == 1
result &= len(x.layerV1Records) == 1 and type(x.layerV1Records[0]) == LayerV1Record
result &= len(x.paintTables) == 1 and type(x.paintTables[0]) == PaintFormat1

y = x.layerV1Records[0]
result &= y.glyphID == 1 and y.paintOffset == 10
y = x.paintTables[0]
result &= y.format == 1 and y.color.paletteIndex == 259
result &= y.color.alpha.scalar == 0.75 and y.color.alpha.varOuterIndex == 160 and y.color.alpha.varInnerIndex == 161
testResults["LayersV1 tryReadStructWithSubtablesFromBuffer test "] = result



#-------------------------------------------------------------
# tests for BaseGlyphV1List
#-------------------------------------------------------------




#-------------------------------------------------------------
# tests for Table_COLR
#-------------------------------------------------------------

try:
    assertIsWellDefinedOTType(Table_COLR_new)
except:
    result = False
else:
    result = True
testResults["Table_COLR definition test"] = result

testResults["Table_COLR constants test 1"] = (Table_COLR_new.TYPE_CATEGORY == otTypeCategory.VERSIONED_TABLE)
result = hasattr(Table_COLR_new, 'FORMATS')
result &= "versionType" in Table_COLR_new.FORMATS
result &= Table_COLR_new.FORMATS["versionType"] == otVersionType.UINT16_MINOR
result &= "versions" in Table_COLR_new.FORMATS
result &= 0 in Table_COLR_new.FORMATS["versions"]
result &= 1 in Table_COLR_new.FORMATS["versions"]
testResults["Table_COLR constants test 2"] = result

# constructor args

try:
    x = Table_COLR_new()
except:
    result = True
else:
    result = False
testResults["Table_COLR_new constructor test 1"] = result

try:
    x = Table_COLR_new(version = 0)
except:
    result = True
else:
    result = False
testResults["Table_COLR_new constructor test 2"] = result

try:
    x = Table_COLR_new(uint16(0), uint16(0), Offset32(0), Offset32(0), version = 0)
except:
    result = True
else:
    result = False
testResults["Table_COLR_new constructor test 3"] = result

x = Table_COLR_new(uint16(0), uint16(0), Offset32(0), Offset32(0), uint16(0), [], [], version = 0)
result = hasattr(x, "FIELDS")
result &= hasattr(x, "PACKED_FORMAT")
result &= hasattr(x, "PACKED_SIZE")
result &= hasattr(x, "ARRAYS")
result &= hasattr(x, "ALL_FIELD_NAMES")
testResults["Table_COLR_new constructor test 4"] = result

"""
x = Table_COLR_new(uint16(0), uint16(0), Offset32(0), Offset32(0), uint16(0), [], [], [], version = 1)
result = hasattr(x, "FIELDS")
result &= hasattr(x, "PACKED_FORMAT")
result &= hasattr(x, "PACKED_SIZE")
result &= hasattr(x, "ARRAYS")
result &= hasattr(x, "SUBTABLES")
result &= hasattr(x, "ALL_FIELD_NAMES")
testResults["Table_COLR_new constructor test 5"] = result
"""


# test Table_COLR.tryReadFromFile using BungeeColor-Regular_colr_Windows.ttf
bungeeColor_file = getTestFontOTFile("BungeeColor")

try:
    colr = bungeeColor_file.fonts[0].tables["COLR"]
except:
    result = False
else:
    result = True
testResults["Table_COLR.tryReadFromFile test 1"] = result
testResults["Table_COLR.tryReadFromFile test 2"] = (type(colr) == Table_COLR_new)
bungeeColor_COLR_headerValues = (0, 288, 14, 1742, 576)
result = True
expected = zip(colr.FIELDS, bungeeColor_COLR_headerValues)
for k, v in expected:
    val = getattr(colr, k)
    if val != v:
        result = False
        break
testResults["Table_COLR.tryReadFromFile test 3"] = result

recordsArray = colr.baseGlyphRecords
testResults["Table_COLR.tryReadFromFile test 4"] = (len(recordsArray) == 288)

record = recordsArray[3]
fields = list(vars(record))
result = (len(fields) == 3)
result &= ("glyphID" in fields and "firstLayerIndex" in fields and "numLayers" in fields)
testResults["Table_COLR.tryReadFromFile test 5"] = result

result = (record.glyphID == 3 and record.firstLayerIndex == 6 and record.numLayers == 2)
testResults["Table_COLR.tryReadFromFile test 6"] = result

record = recordsArray[174]
result = (record.glyphID == 174 and record.firstLayerIndex == 348 and record.numLayers == 2)
testResults["Table_COLR.tryReadFromFile test 7"] = result

recordsArray = colr.layerRecords
testResults["Table_COLR.tryReadFromFile test 8"] = (len(recordsArray) == 576)

record = recordsArray[6]
fields = list(vars(record))
result = (len(fields) == 2)
result &= ("glyphID" in fields and "paletteIndex" in fields)
testResults["Table_COLR.tryReadFromFile test 9"] = result

result = (record.glyphID == 452 and record.paletteIndex == 0)
testResults["Table_COLR.tryReadFromFile test 10"] = result

record = recordsArray[401]
result = (record.glyphID == 451 and record.paletteIndex == 1)
testResults["Table_COLR.tryReadFromFile test 11"] = result





"""
Still need tests for
    - PaintFormat3
    - BaseGlyphV1List
    - COLR V1
"""




notoHW_COLR1_rev2_file = getTestFontOTFile("NotoHW-COLR_1_rev2")






# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

#assert numTestResults == 183

printTestResultSummary("Tests for table_COLR", testResults, skippedTests)
