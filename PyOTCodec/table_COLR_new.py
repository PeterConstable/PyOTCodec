from ot_structs import *
import inspect
import sys


# NOTE: Some class properties are derived from sub-class-specific attributes:
#
#  - PACKED_FORMAT, PACKED_SIZE are derifed from FIELDS
#  - ALL_FIELD_NAMES is derived from FIELDS, ARRAYS, SUBTABLES
#
# These attributes will get set in the base class.


class VarFixed(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("scalar", Fixed),
        ("varOuterIndex", uint16),
        ("varInnerIndex", uint16)
        ])

    def __repr__(self):
        return {"scalar": self.scalar, "varOuterIndex": self.varOuterIndex, "varInnerIndex": self.varInnerIndex}.__repr__()
# End of class VarFixed


class VarF2Dot14(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("scalar", F2Dot14),
        ("varOuterIndex", uint16),
        ("varInnerIndex", uint16)
        ])

    def __repr__(self):
        return {"scalar": self.scalar, 
                "varOuterIndex": self.varOuterIndex, 
                "varInnerIndex": self.varInnerIndex}.__repr__()
# End of class VarF2Dot14


class VarFWord(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("coordinate", FWord),
        ("varOuterIndex", uint16),
        ("varInnerIndex", uint16)
        ])

    def __repr__(self):
        return {"coordinate": self.coordinate, "varOuterIndex": self.varOuterIndex, "varInnerIndex": self.varInnerIndex}.__repr__()
# End of class VarFWord


class VarUFWord(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("distance", UFWord),
        ("varOuterIndex", uint16),
        ("varInnerIndex", uint16)
        ])

    def __repr__(self):
        return {"distance": self.distance, "varOuterIndex": self.varOuterIndex, "varInnerIndex": self.varInnerIndex}.__repr__()
# End of class VarUFWord


class Affine2x2(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("xx", VarFixed),
        ("xy", VarFixed),
        ("yx", VarFixed),
        ("yy", VarFixed)
        ])

    def __repr__(self):
        return {'xx': self.xx, 'xy': self.xy, 'yx': self.yx, 'yy': self.yy}.__repr__()
# End of class Affine2x2


class ColorIndex(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("paletteIndex", uint16),
        ("alpha", VarF2Dot14)
        ])

    def __init__(self, *args):
        init_setattributes(self, *args)
        if self.alpha.scalar < 0 or self.alpha.scalar > 1 :
            raise ValueError(f"Invalid alpha value, {self.alpha}: alpha.scalar must be between 0 and 1.")

    def __repr__(self):
        return {"paletteIndex": self.paletteIndex, "alpha": self.alpha}.__repr__()
# End of class ColorIndex


class ColorStop(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("stopOffset", VarF2Dot14),
        ("color", ColorIndex)
        ])

    def __init__(self, *args):
        init_setattributes(self, *args)
        if self.stopOffset.scalar < 0 or self.stopOffset.scalar > 1 :
            raise ValueError(f"Invalid stopOffset value, {self.stopOffset}: stopOffset.scalar must be between 0 and 1.")

    def __repr__(self):
        return {'stopOffset': self.stopOffset, 'color': self.color}.__repr__()
# End of class ColorStop


class extend(Enum):
    EXTEND_PAD = 0
    EXTEND_REPEAT = 1
    EXTEND_REFLECT = 2


class ColorLine(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT
    FIELDS = OrderedDict([
        ("extend", uint16),
        ("numStops", uint16)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    ARRAYS = [
        {"field": "colorStops", 
         "type": ColorStop, 
         "count": "numStops", 
         "offset": PACKED_SIZE}
        ]

    def __init__(self, *args):
        init_setattributes(self, *args)
        if self.extend not in [x.value for x in extend]:
            raise ValueError(f"Invalid extend value: {self.extend}")


class PaintFormat1(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("format", uint16),
        ("color", ColorIndex)
        ])

    def __repr__(self):
        return {'format': self.format, 'color': self.color}.__repr__()
# End of class PaintFormat1


class PaintFormat2(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
    FIELDS = OrderedDict([
        ("format", uint16),
        ("colorLineOffset", Offset32),
        ("x0", VarFWord),
        ("y0", VarFWord),
        ("x1", VarFWord),
        ("y1", VarFWord),
        ("x2", VarFWord),
        ("y2", VarFWord)
        ])
    SUBTABLES = [
        {"field": "colorLine", 
         "type": ColorLine, 
         "count": 1, 
         "offset": "colorLineOffset"}
        ]


class PaintFormat3(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
    FIELDS = OrderedDict([
        ("format", uint16),
        ("colorLineOffset", Offset32),
        ("x0", VarFWord),
        ("y0", VarFWord),
        ("x1", VarFWord),
        ("y1", VarFWord),
        ("r0", VarUFWord),
        ("r1", VarUFWord),
        ("transformOffset", Offset32)
        ])
    SUBTABLES = [
        {"field": "colorLine", 
         "type": ColorLine, 
         "count": 1, 
         "offset": "colorLineOffset"},
        {"field": "transform", 
         "type": Affine2x2, 
         "count": 1, 
         "offset": "transformOffset"}
        ]


class LayerV1Record(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("glyphID", uint16),
        ("paintOffset", Offset32)
        ])
    
    def __repr__(self):
        return {'glyphID': self.glyphID, 'paintOffset': self.paintOffset}.__repr__()
# End of class LayerV1Record


class LayersV1(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
    FIELDS = OrderedDict([
        ("numLayerV1Records", uint32)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    ARRAYS = [
        {"field": "layerV1Records", 
         "type": LayerV1Record, 
         "count": "numLayerV1Records", 
         "offset": PACKED_SIZE}
        ]
    SUBTABLES = [
        {"field": "paintTables", 
         "type": {
             "formatFieldType": uint16,
             "subtableFormats": {
                 1: PaintFormat1,
                 2: PaintFormat2,
                 3: PaintFormat3
                 }
             }, 
         "count": "numLayerV1Records", 
         "offset": {"parentField": "layerV1Records",
                    "recordField": "paintOffset"}
        }
        ]


class BaseGlyphV1Record(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("glyphID", uint16),
        ("layersV1Offset", Offset32)
        ])
    
    def __repr__(self):
        return {'glyphID': self.glyphID, 'layersV1Offset': self.layersV1Offset}.__repr__()
# End of class BaseGlyphV1Record


class BaseGlyphV1List(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.VAR_LENGTH_STRUCT_WITH_SUBTABLES
    FIELDS = OrderedDict([
        ("numBaseGlyphV1Records", uint32)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    ARRAYS = [
        {"field": "baseGlyphV1Records", 
         "type": BaseGlyphV1Record, 
         "count": "numBaseGlyphV1Records", 
         "offset": PACKED_SIZE}
        ]
    SUBTABLES = [
        {"field": "layerV1Tables", 
         "type": LayersV1, 
         "count": "numBaseGlyphV1Records", 
         "offset": {"parentField": "baseGlyphV1Records",
                    "recordField": "layersV1Offset"}
        }
        ]


class BaseGlyphRecord(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("glyphID", uint16),
        ("firstLayerIndex", uint16),
        ("numLayers", uint16)
        ])
    
    def __repr__(self):
        return {'glyphID': self.glyphID, 'firstLayerIndex': self.firstLayerIndex, 'numLayers': self.numLayers}.__repr__()
# End of class BaseGlyphRecord


class LayerRecord(structBaseClass):
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("glyphID", uint16),
        ("paletteIndex", uint16)
        ])
    
    def __repr__(self):
        return {'glyphID': self.glyphID, 'paletteIndex': self.paletteIndex}.__repr__()
# End of class LayerRecord


class Table_COLR_new:
    _expectedTag = Tag("COLR")

    TYPE_CATEGORY = otTypeCategory.VERSIONED_TABLE

    _fields0 = OrderedDict([
            ("version", uint16),
            ("numBaseGlyphRecords", uint16),
            ("baseGlyphRecordsOffset", Offset32),
            ("layerRecordsOffset", Offset32),
            ("numLayerRecords", uint16)
        ])
    _packedFormat0 = getPackedFormatFromFieldsDef(_fields0)
    _packedSize0 = struct.calcsize(_packedFormat0)
    _arrays0 = [
        {"field": "baseGlyphRecords",
         "type": BaseGlyphRecord,
         "count": "numBaseGlyphRecords",
         "offset": "baseGlyphRecordsOffset"},
        {"field": "layerRecords",
         "type": LayerRecord,
         "count": "numLayerRecords",
         "offset": "layerRecordsOffset"}
        ]

    _fields1_addl = OrderedDict([
            ("baseGlyphV1ListOffset", Offset32),
            ("itemVariationStoreOffset", Offset32)
        ])
    _packedFormat1_addl = getPackedFormatFromFieldsDef(_fields1_addl)
    _packedSize1_addl = struct.calcsize(_packedFormat1_addl)

    _subtables1 = [
        {"field": "baseGlyphV1List", 
         "type": BaseGlyphV1List, 
         "count": 1, 
         "offset": "baseGlyphV1ListOffset"
        } # ignoring ItemVariationStore for now
        ]

    FORMATS = {
        "versionType": otVersionType.UINT16_MINOR,
        "versions": {
            0: {
                "FIELDS": _fields0,
                "PACKED_FORMAT": _packedFormat0,
                "PACKED_SIZE": _packedSize0,
                "ARRAYS": _arrays0,
                "ALL_FIELD_NAMES": getCombinedFieldNames(_fields0, _arrays0)
                },
            1: {
                "FIELDS": OrderedDict(list(_fields0.items()) + list(_fields1_addl.items())),
                "PACKED_FORMAT": concatFormatStrings(_packedFormat0, _packedFormat1_addl),
                "PACKED_SIZE": _packedSize0 + _packedSize1_addl,
                "ARRAYS": _arrays0,
                "SUBTABLES": _subtables1,
                "ALL_FIELD_NAMES": getCombinedFieldNames(
                    OrderedDict(list(_fields0.items()) + list(_fields1_addl.items())),
                    _arrays0,
                    _subtables1
                    )
                }
            }
        }

    def __init__(self, *args):
        init_setattributes(self, *args)


    @staticmethod
    def tryReadFromFile(parentFont, tableRecord):

        from ot_font import OTFont, TableRecord
        if not (isinstance(parentFont, OTFont) and isinstance(tableRecord, TableRecord)):
            raise Exception()

        import ot_table
        ot_table.ValidateTableTag(tableRecord, Tag("COLR"))

        # get file bytes, then validate offset/length are in file bounds
        fileBytes = parentFont.fileBytes
        offsetInFile = tableRecord.offset
        ot_table.ValidateOffsetAndLength(
            len(fileBytes), offsetInFile, tableRecord.length
            )

        # get the table bytes: since offset length are in bounds, can get the expected length
        tableBytes = fileBytes[offsetInFile : offsetInFile + tableRecord.length]

        colr = tryReadVersionedTableFromBuffer(tableBytes, Table_COLR_new)

        colr.parentFont = parentFont
        colr.tableRecord = tableRecord

        return colr
    # End of tryReadFromFile

# End of class Table_COLR_new:



# Run validations on the above struct definitions
classmembers = inspect.getmembers(
    sys.modules[__name__], 
    lambda member: (inspect.isclass(member) 
        and member.__module__ == __name__
        and not issubclass(member,  Enum))
    )
for name, class_ in classmembers:
    assertIsWellDefinedOTType(class_)




