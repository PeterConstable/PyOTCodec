from PyOTCodecTests.test_setup import getTestFontOTFile, printTestResultSummary

from ot_file import *


testResults = dict({})
skippedTests = []



#-------------------------------------------------------------
# tests for table_COLR
#-------------------------------------------------------------

# test BaseGlyphRecord

try:
    assertIsWellDefinedStruct(BaseGlyphRecord)
except:
    result = False
else:
    result = True
testResults["Table_COLR BaseGlyphRecord definition test"] = result

testResults["Table_COLR BaseGlyphRecord constants test 1"] = (BaseGlyphRecord._packedFormat == ">3H")
testResults["Table_COLR BaseGlyphRecord constants test 2"] = (BaseGlyphRecord._packedSize == 6)
testResults["Table_COLR BaseGlyphRecord constants test 3"] = (BaseGlyphRecord._numPackedValues == 3)
testResults["Table_COLR BaseGlyphRecord constants test 4"] = (BaseGlyphRecord._fieldNames == ("glyphID", "firstLayerIndex", "numLayers"))
testResults["Table_COLR BaseGlyphRecord constants test 5"] = (BaseGlyphRecord._fieldTypes == (int, int, int))

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
for f in BaseGlyphRecord._fieldNames:
    result &= hasattr(x, f)
testResults["Table_COLR BaseGlyphRecord constructor test 6"] = result
result = (x.glyphID == 2 and x.firstLayerIndex == 4 and x.numLayers == 17)
testResults["Table_COLR BaseGlyphRecord constructor test 7"] = result


# tests for LayerRecord

try:
    assertIsWellDefinedStruct(LayerRecord)
except:
    result = False
else:
    result = True
testResults["Table_COLR LayerRecord definition test"] = result

testResults["Table_COLR LayerRecord constants test 1"] = (LayerRecord._packedFormat == ">2H")
testResults["Table_COLR LayerRecord constants test 2"] = (LayerRecord._packedSize == 4)
testResults["Table_COLR LayerRecord constants test 3"] = (LayerRecord._numPackedValues == 2)
testResults["Table_COLR LayerRecord constants test 4"] = (LayerRecord._fieldNames == ("glyphID", "paletteIndex"))
testResults["Table_COLR LayerRecord constants test 5"] = (LayerRecord._fieldTypes == (int, int))

try:
    x = LayerRecord(2)
except:
    result = True
else:
    result = False
testResults["Table_COLR LayerRecord constructor test 1"] = result
try:
    x = LayerRecord(2.0, 17)
except:
    result = True
else:
    result = False
testResults["Table_COLR LayerRecord constructor test 2"] = result
try:
    x = LayerRecord(-2, 17)
except:
    result = True
else:
    result = False
testResults["Table_COLR LayerRecord constructor test 3"] = result
try:
    x = LayerRecord(2, -17)
except:
    result = True
else:
    result = False
testResults["Table_COLR LayerRecord constructor test 4"] = result
x = LayerRecord(2, 17)
result = (type(x) == LayerRecord)
for f in LayerRecord._fieldNames:
    result &= hasattr(x, f)
testResults["Table_COLR LayerRecord constructor test 5"] = result
result = (x.glyphID == 2 and x.paletteIndex == 17)
testResults["Table_COLR LayerRecord constructor test 6"] = result


# tests for BaseGlyphV1Record
try:
    assertIsWellDefinedStruct(BaseGlyphV1Record)
except:
    result = False
else:
    result = True
testResults["Table_COLR BaseGlyphV1Record definition test"] = result

testResults["Table_COLR BaseGlyphV1Record constants test 1"] = (BaseGlyphV1Record._packedFormat == ">HL")
testResults["Table_COLR BaseGlyphV1Record constants test 2"] = (BaseGlyphV1Record._packedSize == 6)
testResults["Table_COLR BaseGlyphV1Record constants test 3"] = (BaseGlyphV1Record._numPackedValues == 2)
testResults["Table_COLR BaseGlyphV1Record constants test 4"] = (BaseGlyphV1Record._fieldNames == ("glyphID", "layersV1Offset"))
testResults["Table_COLR BaseGlyphV1Record constants test 5"] = (BaseGlyphV1Record._fieldTypes == (int, int))

try:
    x = BaseGlyphV1Record(2)
except:
    result = True
else:
    result = False
testResults["Table_COLR BaseGlyphV1Record constructor test 1"] = result
try:
    x = BaseGlyphV1Record(2.0, 17)
except:
    result = True
else:
    result = False
testResults["Table_COLR BaseGlyphV1Record constructor test 2"] = result
try:
    x = BaseGlyphV1Record(-2, 17)
except:
    result = True
else:
    result = False
testResults["Table_COLR BaseGlyphV1Record constructor test 3"] = result
try:
    x = BaseGlyphV1Record(2, -17)
except:
    result = True
else:
    result = False
testResults["Table_COLR BaseGlyphV1Record constructor test 4"] = result

x = BaseGlyphV1Record(2, 17)
result = (type(x) == BaseGlyphV1Record)
for f in BaseGlyphV1Record._fieldNames:
    result &= hasattr(x, f)
testResults["Table_COLR BaseGlyphV1Record constructor test 5"] = result
result = (x.glyphID == 2 and x.layersV1Offset == 17)
testResults["Table_COLR BaseGlyphV1Record constructor test 6"] = result


# tests for LayerV1Record
try:
    assertIsWellDefinedStruct(LayerV1Record)
except:
    result = False
else:
    result = True
testResults["Table_COLR LayerV1Record definition test"] = result

testResults["Table_COLR LayerV1Record constants test 1"] = (LayerV1Record._packedFormat == ">HL")
testResults["Table_COLR LayerV1Record constants test 2"] = (LayerV1Record._packedSize == 6)
testResults["Table_COLR LayerV1Record constants test 3"] = (LayerV1Record._numPackedValues == 2)
testResults["Table_COLR LayerV1Record constants test 4"] = (LayerV1Record._fieldNames == ("glyphID", "paintOffset"))
testResults["Table_COLR LayerV1Record constants test 5"] = (LayerV1Record._fieldTypes == (int, int))

try:
    x = LayerV1Record(2)
except:
    result = True
else:
    result = False
testResults["Table_COLR LayerV1Record constructor test 1"] = result
try:
    x = LayerV1Record(2.0, 17)
except:
    result = True
else:
    result = False
testResults["Table_COLR LayerV1Record constructor test 2"] = result
try:
    x = LayerV1Record(-2, 17)
except:
    result = True
else:
    result = False
testResults["Table_COLR LayerV1Record constructor test 3"] = result
try:
    x = LayerV1Record(2, -17)
except:
    result = True
else:
    result = False
testResults["Table_COLR LayerV1Record constructor test 4"] = result
x = LayerV1Record(2, 17)
result = (type(x) == LayerV1Record)
for f in LayerV1Record._fieldNames:
    result &= hasattr(x, f)
testResults["Table_COLR LayerV1Record constructor test 5"] = result
result = (x.glyphID == 2 and x.paintOffset == 17)
testResults["Table_COLR LayerV1Record constructor test 6"] = result


# tests for VarFixed

try:
    assertIsWellDefinedStruct(VarFixed)
except:
    result = False
else:
    result = True
testResults["Table_COLR VarFixed definition test"] = result

testResults["Table_COLR VarFixed constants test 1"] = (VarFixed._packedFormat == (Fixed._packedFormat + "2H"))
testResults["Table_COLR VarFixed constants test 2"] = (VarFixed._packedSize == 8)
testResults["Table_COLR VarFixed constants test 3"] = (VarFixed._numPackedValues == 3)
testResults["Table_COLR VarFixed constants test 4"] = (VarFixed._fieldNames == ("value", "varOuterIndex", "varInnerIndex"))
testResults["Table_COLR VarFixed constants test 5"] = (VarFixed._fieldTypes == (Fixed, int, int))

try:
    x = VarFixed(Fixed.createFixedFromUint32(0x48000), 4)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFixed constructor test 1"] = result
try:
    x = VarFixed(0x1_8000, 4, 7)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFixed constructor test 2"] = result
try:
    x = VarFixed(Fixed.createFixedFromUint32(0x48000), -17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFixed constructor test 3"] = result
try:
    x = VarFixed(Fixed.createFixedFromUint32(0x48000), 17, -23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFixed constructor test 4"] = result
x = VarFixed(Fixed.createFixedFromUint32(0x48000),1,3)
testResults["Table_COLR VarFixed constructor test 5"] = (type(x.value) == Fixed and type(x.varOuterIndex) == int and type(x.varInnerIndex) == int)
testResults["Table_COLR VarFixed constructor test 6"] = (x.value == 4.5 and x.varOuterIndex == 1 and x.varInnerIndex == 3)

result = x.__repr__() == "{'value': 4.5, 'varOuterIndex': 1, 'varInnerIndex': 3}"
testResults["Table_COLR VarFixed __repr__ test"] = result

x = VarFixed.interpretUnpackedValues(0x1_8000, 4, 7)
testResults["Table_COLR VarFixed interpretUnpackedValues test 1"] = (len(x) == 3 and type(x[0]) == Fixed and type(x[1]) == int and type(x[2]) == int)
testResults["Table_COLR VarFixed interpretUnpackedValues test 2"] = (x[0]._rawBytes == b'\x00\x01\x80\x00' and x[1] == 4 and x[2] == 7)
x = VarFixed(*VarFixed.interpretUnpackedValues(0x1_8000, 4, 7))
testResults["Table_COLR VarFixed interpretUnpackedValues test 3"] = (type(x) == VarFixed and x.value._rawBytes == b'\x00\x01\x80\x00' and x.varOuterIndex == 4 and x.varInnerIndex == 7)


# tests for VarF2Dot14

try:
    assertIsWellDefinedStruct(VarF2Dot14)
except:
    result = False
else:
    result = True
testResults["Table_COLR VarF2Dot14 definition test"] = result

testResults["Table_COLR VarF2Dot14 constants test 1"] = (VarF2Dot14._packedFormat == (F2Dot14._packedFormat + "2H"))
testResults["Table_COLR VarF2Dot14 constants test 2"] = (VarF2Dot14._packedSize == 6)
testResults["Table_COLR VarF2Dot14 constants test 3"] = (VarF2Dot14._numPackedValues == 3)
testResults["Table_COLR VarF2Dot14 constants test 4"] = (VarF2Dot14._fieldNames == ("value", "varOuterIndex", "varInnerIndex"))
testResults["Table_COLR VarF2Dot14 constants test 5"] = (VarF2Dot14._fieldTypes == (F2Dot14, int, int))

try:
    x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), 4)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarF2Dot14 constructor test 1"] = result
try:
    x = VarF2Dot14(0x6000, 4, 7)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarF2Dot14 constructor test 2"] = result
try:
    x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), -17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarF2Dot14 constructor test 3"] = result
try:
    x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), 17, -23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarF2Dot14 constructor test 4"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), 1, 3)
testResults["Table_COLR VarF2Dot14 constructor test 5"] = (type(x.value) == F2Dot14 and type(x.varOuterIndex) == int and type(x.varInnerIndex) == int)
testResults["Table_COLR VarF2Dot14 constructor test 6"] = (x.value == 1.5 and x.varOuterIndex == 1 and x.varInnerIndex == 3)

result = x.__repr__() == "{'value': 1.5, 'varOuterIndex': 1, 'varInnerIndex': 3}"
testResults["Table_COLR VarF2Dot14 __repr__ test"] = result

x = VarF2Dot14.interpretUnpackedValues(0x7000, 4, 7)
testResults["Table_COLR VarF2Dot14 interpretUnpackedValues test 1"] = (len(x) == 3 and type(x[0]) == F2Dot14 and type(x[1]) == int and type(x[2]) == int)
testResults["Table_COLR VarF2Dot14 interpretUnpackedValues test 2"] = (x[0]._rawBytes == b'\x70\x00' and x[1] == 4 and x[2] == 7)
x = VarF2Dot14(*VarF2Dot14.interpretUnpackedValues(0x7000, 4, 7))
testResults["Table_COLR VarF2Dot14 interpretUnpackedValues test 3"] = (type(x) == VarF2Dot14 and x.value._rawBytes == b'\x70\x00' and x.varOuterIndex == 4 and x.varInnerIndex == 7)


# tests for VarFWord

try:
    assertIsWellDefinedStruct(VarFWord)
except:
    result = False
else:
    result = True
testResults["Table_COLR VarFWord definition test"] = result

testResults["Table_COLR VarFWord constants test 1"] = (VarFWord._packedFormat == ">h2H")
testResults["Table_COLR VarFWord constants test 2"] = (VarFWord._packedSize == 6)
testResults["Table_COLR VarFWord constants test 3"] = (VarFWord._numPackedValues == 3)
testResults["Table_COLR VarFWord constants test 4"] = (VarFWord._fieldNames == ("coordinate", "varOuterIndex", "varInnerIndex"))
testResults["Table_COLR VarFWord constants test 5"] = (VarFWord._fieldTypes == (int, int, int))

x = VarFWord(-24, 17, 23)
testResults["Table_COLR VarFWord constructor test 1"] = (type(x) == VarFWord and type(x.coordinate) == int and type(x.varOuterIndex) == int and type(x.varInnerIndex) == int)
testResults["Table_COLR VarFWord constructor test 2"] = (x.coordinate == -24 and x.varOuterIndex == 17 and x.varInnerIndex == 23)
try:
    x = VarFWord(24, -17)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFWord constructor test 3"] = result
try:
    x = VarFWord(24.0, 17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFWord constructor test 4"] = result
try:
    x = VarFWord(24, -17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFWord constructor test 5"] = result
try:
    x = VarFWord(24, 17, -23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarFWord constructor test 6"] = result

x = VarFWord(-24, 17, 23)
testResults["Table_COLR VarFWord __repr__ test"] = (x.__repr__() == "{'coordinate': -24, 'varOuterIndex': 17, 'varInnerIndex': 23}")


# tests for VarUFWord

try:
    assertIsWellDefinedStruct(VarUFWord)
except:
    result = False
else:
    result = True
testResults["Table_COLR VarUFWord definition test"] = result

testResults["Table_COLR VarUFWord constants test 1"] = (VarUFWord._packedFormat == ">3H")
testResults["Table_COLR VarUFWord constants test 2"] = (VarUFWord._packedSize == 6)
testResults["Table_COLR VarUFWord constants test 3"] = (VarUFWord._numPackedValues == 3)
testResults["Table_COLR VarUFWord constants test 4"] = (VarUFWord._fieldNames == ("distance", "varOuterIndex", "varInnerIndex"))
testResults["Table_COLR VarUFWord constants test 5"] = (VarUFWord._fieldTypes == (int, int, int))

x = VarUFWord(24, 17, 23)
testResults["Table_COLR VarUFWord constructor test 1"] = (type(x) == VarUFWord and type(x.distance) == int and type(x.varOuterIndex) == int and type(x.varInnerIndex) == int)
testResults["Table_COLR VarUFWord constructor test 2"] = (x.distance == 24 and x.varOuterIndex == 17 and x.varInnerIndex == 23)
try:
    x = VarUFWord(24, 17)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarUFWord constructor test 3"] = result
try:
    x = VarUFWord(-24, 17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarUFWord constructor test 4"] = result
try:
    x = VarUFWord(24, -17, 23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarUFWord constructor test 5"] = result
try:
    x = VarUFWord(24, 17, -23)
except:
    result = True
else:
    result = False
testResults["Table_COLR VarUFWord constructor test 6"] = result

x = VarUFWord(24, 17, 23)
testResults["Table_COLR VarUFWord __repr__ test"] = (x.__repr__() == "{'distance': 24, 'varOuterIndex': 17, 'varInnerIndex': 23}")


# tests for Affine2x2

try:
    assertIsWellDefinedStruct(Affine2x2)
except:
    result = False
else:
    result = True
testResults["Table_COLR Affine2x2 definition test"] = result

testResults["Table_COLR Affine2x2 constants test 1"] = (Affine2x2._packedFormat == ">L2HL2HL2HL2H")
testResults["Table_COLR Affine2x2 constants test 2"] = (Affine2x2._packedSize == (VarFixed._packedSize * 4))
testResults["Table_COLR Affine2x2 constants test 3"] = (Affine2x2._numPackedValues == 12)
testResults["Table_COLR Affine2x2 constants test 4"] = (Affine2x2._fieldNames == ("xx", "xy", "yx", "yy"))
testResults["Table_COLR Affine2x2 constants test 5"] = (Affine2x2._fieldTypes == (VarFixed, VarFixed, VarFixed, VarFixed))

x = VarFixed(Fixed.createFixedFromUint32(0x1_8000), 2, 17)
try:
    y = Affine2x2(x, x, x)
except:
    result = True
else:
    result = False
testResults["Table_COLR Affine2x2 constructor test 1"] = result
y = Affine2x2(x, x, x, x)
result = (type(y) == Affine2x2 and type(y.xx) == VarFixed and type(y.xy) == VarFixed and type(y.yx) == VarFixed and type(y.yy) == VarFixed)
testResults["Table_COLR Affine2x2 constructor test 2"] = result
result = (y.xx.value._rawBytes == b'\x00\01\x80\x00' and y.xx.varOuterIndex == 2 and y.xx.varInnerIndex == 17)
testResults["Table_COLR Affine2x2 constructor test 3"] = result

result = (y.__repr__() == "{'xx': {'value': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}, 'xy': {'value': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}, 'yx': {'value': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}, 'yy': {'value': 1.5, 'varOuterIndex': 2, 'varInnerIndex': 17}}")
testResults["Table_COLR Affine2x2 __repr__ test"] = result

# tryReadFromFile
buffer = b'\x00\x01\x80\x00'
try:
    x = Affine2x2.tryReadFromFile(buffer)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR Affine2x2 tryReadFromFile test 1"] = result
buffer = b'\x00\x01\x00\x00\x00\x02\x00\x17\x00\x00\x00\x00\x00\x00\x01\x17\xff\xff\x00\x00\x00\x04\x02\x17\x00\x01\xC0\x00\x00\x02\x00\x42\x00\x00'
#\x00\x01\x00\x00\x00\x02\x00\x17
#\x00\x00\x00\x00\x00\x00\x01\x17
#\xff\xff\x00\x00\x00\x04\x02\x17
#\x00\x01\xc0\x00\x00\x02\x00\x42
x = Affine2x2.tryReadFromFile(buffer)
result = (type(x) == Affine2x2)
result &=(x.xx.value._rawBytes == b'\x00\x01\x00\x00' and x.xx.varOuterIndex == 2 and x.xx.varInnerIndex == 0x17)
result &=(x.xy.value._rawBytes == b'\x00\x00\x00\x00' and x.xy.varOuterIndex == 0 and x.xy.varInnerIndex == 0x117)
result &=(x.yx.value._rawBytes == b'\xff\xff\x00\x00' and x.yx.varOuterIndex == 4 and x.yx.varInnerIndex == 0x217)
result &=(x.yy.value._rawBytes == b'\x00\x01\xc0\x00' and x.yy.varOuterIndex == 2 and x.yy.varInnerIndex == 0x42)
testResults["Table_COLR Affine2x2 tryReadFromFile test 2"] = result


# tests for ColorIndex

try:
    assertIsWellDefinedStruct(ColorIndex)
except:
    result = False
else:
    result = True
testResults["Table_COLR ColorIndex definition test"] = result

testResults["ColorIndex constants test 1"] = (ColorIndex._packedFormat == ">HH2H")
testResults["ColorIndex constants test 2"] = (ColorIndex._packedSize == 8)
testResults["ColorIndex constants test 3"] = (ColorIndex._numPackedValues == 4)
testResults["ColorIndex constants test 4"] = (ColorIndex._fieldNames == ("paletteIndex", "alpha"))
testResults["ColorIndex constants test 5"] = (ColorIndex._fieldTypes == (int, VarF2Dot14))

# constructor tests -- arg validations
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
try:
    y = ColorIndex(24)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 1"] = result
try:
    y = ColorIndex(24, 42)
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
try:
    y = ColorIndex(-24, x)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 4"] = result

# alpha out of range [0, 1]
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x6000), 1, 3)
try:
    y = ColorIndex(24, x)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 2"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x8000), 1, 3)
try:
    y = ColorIndex(24, x)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR ColorIndex constructor test 3"] = result

# good args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
y = ColorIndex(24, x)
testResults["Table_COLR ColorIndex constructor test 5"] = (type(y.paletteIndex) == int and type(y.alpha) == VarF2Dot14)
testResults["Table_COLR ColorIndex test constructor 6"] = (y.paletteIndex == 24 and y.alpha.value == 0.75 and y.alpha.varOuterIndex == 1 and y.alpha.varInnerIndex == 3)

x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
y = ColorIndex(24, x)
result = y.__repr__() == "{'paletteIndex': 24, 'alpha': {'value': 0.75, 'varOuterIndex': 1, 'varInnerIndex': 3}}"
testResults["Table_COLR ColorIndex __repr__ test"] = result

x = ColorIndex.interpretUnpackedValues(17, 0xC000, 3, 5)
result = (len(x) == 2 and type(x[0]) == int and type(x[1]) == VarF2Dot14)
testResults["Table_COLR ColorIndex interpretUnpackedValues test 1"] = result
x = ColorIndex(*ColorIndex.interpretUnpackedValues(17, 0x3000, 3, 5))
result = (type(x) == ColorIndex and x.paletteIndex == 17 and x.alpha.value.value == 0.75 and x.alpha.varOuterIndex == 3 and x.alpha.varInnerIndex == 5)
testResults["Table_COLR ColorIndex interpretUnpackedValues test 2"] = result


# tests for ColorStop

try:
    assertIsWellDefinedStruct(ColorIndex)
except:
    result = False
else:
    result = True
testResults["Table_COLR ColorStop definition test"] = result

testResults["Table_COLR ColorStop constants test 1"] = (ColorStop._packedFormat == ">H2HHH2H")
testResults["Table_COLR ColorStop constants test 2"] = (ColorStop._packedSize == 14)
testResults["Table_COLR ColorStop constants test 3"] = (ColorStop._numPackedValues == 7)
testResults["Table_COLR ColorStop constants test 4"] = (ColorStop._fieldNames == ("stopOffset", "color"))
testResults["Table_COLR ColorStop constants test 5"] = (ColorStop._fieldTypes == (VarF2Dot14, ColorIndex))

# constructor arg validations
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x1000), 1, 3)
y = ColorIndex(24, x)
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
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
try:
    z = ColorStop(x, 24)
except:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 3"] = result

# stopOffset out of range [0, 1]
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
y = ColorIndex(24, x)
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x4001), 1, 3)
try:
    z = ColorStop(x, y)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 4"] = result
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 1, 3)
y = ColorIndex(24, x)
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0xC001), 1, 3)
try:
    z = ColorStop(x, y)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR ColorStop constructor test 5"] = result

# good args
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x1000), 1, 3)
y = ColorIndex(24, x)
x = VarF2Dot14(F2Dot14.createF2Dot14FromUint16(0x3000), 0, 4)
z = ColorStop(x, y)
testResults["Table_COLR ColorStop constructor test 6"] = (type(z.stopOffset) == VarF2Dot14 and type(z.color) == ColorIndex)
testResults["Table_COLR ColorStop constructor test 7"] = (z.stopOffset.value == 0.75 and z.stopOffset.varOuterIndex == 0 and z.stopOffset.varInnerIndex == 4)
testResults["Table_COLR ColorStop constructor test 8"] = (z.color.paletteIndex == 24 and z.color.alpha.value == 0.25 and z.color.alpha.varOuterIndex == 1 and y.alpha.varInnerIndex == 3)

result = z.__repr__() == "{'stopOffset': {'value': 0.75, 'varOuterIndex': 0, 'varInnerIndex': 4}, 'color': {'paletteIndex': 24, 'alpha': {'value': 0.25, 'varOuterIndex': 1, 'varInnerIndex': 3}}}"
testResults["Table_COLR ColorStop __repr__ test"] = result

#interpretUnpackedValues
x = ColorStop.interpretUnpackedValues(0x3000, 0, 4, 24, 0x1000, 1, 3)
result = (len(x) == 2 and type(x[0]) == VarF2Dot14 and type(x[1]) == ColorIndex)
testResults["Table_COLR ColorStop interpretUnpackedValues test 1"] = result
x = ColorStop(*ColorStop.interpretUnpackedValues(0x3000, 0, 4, 24, 0x1000, 1, 3))
result = (type(x) == ColorStop and x.stopOffset.value.value == 0.75 and x.color.paletteIndex == 24)
testResults["Table_COLR ColorStop interpretUnpackedValues test 2"] = result


# tests for ColorLine

try:
    assertIsWellDefinedStruct(ColorLine)
except:
    result = False
else:
    result = True
testResults["Table_COLR ColorLine definition test"] = result

testResults["Table_COLR ColorLine constants test 1"] = (ColorLine._packedFormat == ">2H")
testResults["Table_COLR ColorLine constants test 2"] = (ColorLine._packedSize == 4)
testResults["Table_COLR ColorLine constants test 3"] = (ColorLine._numPackedValues == 2)
testResults["Table_COLR ColorLine constants test 4"] = (ColorLine._fieldNames == ("extend", "numStops"))
testResults["Table_COLR ColorLine constants test 5"] = (ColorLine._fieldTypes == (int, int))

# constructor, createNew_ColorLine
x = ColorLine()
testResults["Table_COLR ColorLine constructor test"] = (len(vars(x)) == 0)

x = ColorLine.createNew_ColorLine()
testResults["Table_COLR ColorLine createNew_ColorLine test"] = (vars(x) == {'extend': 0, 'numStops': 0})

# tryReadFromFile

# buffer too short for header
buffer = b'\x00\x00'
try:
    x = ColorLine.tryReadFromFile(buffer)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR ColorLine tryReadFromFile test 1"] = result

# header but no stops
buffer = b'\x00\x02\x00\x00'
x = ColorLine.tryReadFromFile(buffer)
result = (type(x) == ColorLine and vars(x) == {'extend': 2, 'numStops': 0, 'colorStops': []})
testResults["Table_COLR ColorLine tryReadFromFile test 2"] = result

# buffer too short for stops array
buffer = b'\x00\x00\x00\x01' b'\x00\x00'
try:
    x = ColorLine.tryReadFromFile(buffer)
except OTCodecError:
    result = True
else:
    result = False
testResults["Table_COLR ColorLine tryReadFromFile test 3"] = result

buffer = b'\x00\x00' b'\x00\x02' b'\x10\x00\x00\x02\x03\x00\x00\x15\x01\x00\x00\x03\x00\x07' + \
    b'\x38\x00\x01\x21\x00\xc2\x01\x42\x00\xff\x0d\x34\x21\x22'
# extend: \x00\x00
# numStops: \x00\x02
# ColorStop 0: \x10\x00 \x00\x02 \x03\x00 + \x00\x15 \x01\x00 \x00\x03 \x00\x07
# ColorStop 1: \x38\x00 \x01\x21 \x00\xc2 + \x01\x42 \x00\xff \x0d\x34 \x21\x22
x = ColorLine.tryReadFromFile(buffer)
result = (x.extend == 0 and x.numStops == 2)
result &= (type(x.colorStops) == list and len(x.colorStops) == 2)
result &= (type(x.colorStops[0]) == ColorStop and type(x.colorStops[1]) == ColorStop)
testResults["Table_COLR ColorLine tryReadFromFile test 4"] = result
y = x.colorStops[0]
result = (y.stopOffset.value == 0.25 and y.stopOffset.varOuterIndex == 2 and y.stopOffset.varInnerIndex == 0x300)
result &= (y.color.paletteIndex == 21 and y.color.alpha.value._rawBytes == b'\x01\x00' and y.color.alpha.varOuterIndex == 3 and y.color.alpha.varInnerIndex == 7)
testResults["Table_COLR ColorLine tryReadFromFile test 5"] = result
y = x.colorStops[1]
result = (y.stopOffset.value == 0.875 and y.stopOffset.varOuterIndex == 0x121 and y.stopOffset.varInnerIndex == 0xc2)
result &= (y.color.paletteIndex == 0x142 and y.color.alpha.value._rawBytes == b'\x00\xff' and y.color.alpha.varOuterIndex == 0xd34 and y.color.alpha.varInnerIndex == 0x2122)
testResults["Table_COLR ColorLine tryReadFromFile test 6"] = result




# test COLR constructor
colr = Table_COLR()
testResults["Table_COLR constructor test 1"] = (type(colr) == Table_COLR)
testResults["Table_COLR constructor test 2"] = (colr.tableTag == "COLR")
testResults["Table_COLR constructor test 3"] = (not hasattr(colr, "version"))

# createNew_COLR: check default values for version 0
colr = Table_COLR.createNew_COLR(0)
testResults["Table_COLR.createNew_COLR test 1"] = (type(colr) == Table_COLR)
result = True
expected = zip(Table_COLR._colr_0_fields, Table_COLR._colr_0_defaults)
for k, v in expected:
    val = getattr(colr, k)
    if val != v:
        result = False
        break
testResults["Table_COLR.createNew_COLR test 2"] = result

# createNew_COLR: check default values for version 1
colr = Table_COLR.createNew_COLR(1)
testResults["Table_COLR.createNew_COLR test 3"] = (type(colr) == Table_COLR)
result = True
expected = zip(Table_COLR._colr_1_all_fields, Table_COLR._colr_1_all_defaults)
for k, v in expected:
    val = getattr(colr, k)
    if val != v:
        result = False
        break
testResults["Table_COLR.createNew_COLR test 4"] = result

# test Table_COLR.tryReadFromFile using BungeeColor-Regular_colr_Windows.ttf
bungeeColor_file = getTestFontOTFile("BungeeColor")

try:
    colr = bungeeColor_file.fonts[0].tables["COLR"]
except Exception:
    result = False
else:
    result = True
testResults["Table_COLR.tryReadFromFile test 1"] = result
testResults["Table_COLR.tryReadFromFile test 2"] = (type(colr) == Table_COLR)
bungeeColor_COLR_headerValues = (0, 288, 14, 1742, 576)
result = True
expected = zip(Table_COLR._colr_0_fields, bungeeColor_COLR_headerValues)
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
    - PaintFormat1
    - PaintFormat2
    - PaintFormat3
    - LayersV1
    - BaseGlyphV1List
    - COLR V1
"""

notoHW_COLR1_rev2_file = getTestFontOTFile("NotoHW-COLR_1_rev2")




# END OF TESTS

numTestResults = len(testResults)
numFailures = list(testResults.values()).count(False)
numSkipped = len(skippedTests)

assert numTestResults == 183

printTestResultSummary("Tests for table_maxp", testResults, skippedTests)
