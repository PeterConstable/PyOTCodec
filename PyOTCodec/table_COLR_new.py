from ot_structs import *


class VarFixed:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("scalar", Fixed),
        ("varOuterIndex", uint16),
        ("varInnerIndex", uint16)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

    def __repr__(self):
        return {"scalar": self.scalar, "varOuterIndex": self.varOuterIndex, "varInnerIndex": self.varInnerIndex}.__repr__()
# End of class VarFixed


class VarF2Dot14:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("scalar", F2Dot14),
        ("varOuterIndex", uint16),
        ("varInnerIndex", uint16)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

    def __repr__(self):
        return {"scalar": self.scalar, 
                "varOuterIndex": self.varOuterIndex, 
                "varInnerIndex": self.varInnerIndex}.__repr__()
# End of class VarF2Dot14


class VarFWord:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("coordinate", FWord),
        ("varOuterIndex", uint16),
        ("varInnerIndex", uint16)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

    def __repr__(self):
        return {"coordinate": self.coordinate, "varOuterIndex": self.varOuterIndex, "varInnerIndex": self.varInnerIndex}.__repr__()
# End of class VarFWord


class VarUFWord:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("scalar", UFWord),
        ("varOuterIndex", uint16),
        ("varInnerIndex", uint16)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

    def __repr__(self):
        return {"distance": self.distance, "varOuterIndex": self.varOuterIndex, "varInnerIndex": self.varInnerIndex}.__repr__()
# End of class VarUFWord


class Affine2x2:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("xx", VarFixed),
        ("xy", VarFixed),
        ("yx", VarFixed),
        ("yy", VarFixed)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

    def __repr__(self):
        return {'xx': self.xx, 'xy': self.xy, 'yx': self.yx, 'yy': self.yy}.__repr__()
# End of class Affine2x2


class ColorIndex:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("paletteIndex", uint16),
        ("alpha", VarF2Dot14)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

    def __repr__(self):
        return {"paletteIndex": self.paletteIndex, "alpha": self.alpha}.__repr__()
# End of class ColorIndex


class ColorStop:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("stopOffset", VarF2Dot14),
        ("color", ColorIndex)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

    def __repr__(self):
        return {'stopOffset': self.stopOffset, 'color': self.color}.__repr__()
# End of class ColorStop


class extend(Enum):
    EXTEND_PAD = 0
    EXTEND_REPEAT = 1
    EXTEND_REFLECT = 2


class ColorLine:
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
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS)

    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)
        if self.extend not in [x.value for x in extend]:
            raise ValueError(f"Invalid extend value: {self.extend}")


class PaintFormat1:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_COMPLEX_STRUCT
    FIELDS = OrderedDict([
        ("format", uint16),
        ("color", ColorIndex)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

    def __repr__(self):
        return {'format': self.format, 'color': self.color}.__repr__()
# End of class PaintFormat1


class PaintFormat2:
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
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    SUBTABLES = [
        {"field": "colorLine", 
         "type": ColorLine, 
         "count": 1, 
         "offset": "colorLineOffset"}
        ]
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, subtables = SUBTABLES)

    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)


class PaintFormat3:
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
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
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
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, subtables = SUBTABLES)

    def __init__(self, *args):
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)


class LayerV1Record:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("glyphID", uint16),
        ("paintOffset", Offset32)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)
    def __repr__(self):
        return {'glyphID': self.glyphID, 'paintOffset': self.paintOffset}.__repr__()
# End of class LayerV1Record


class LayersV1:
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
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS, SUBTABLES)

    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)


class BaseGlyphV1Record:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("glyphID", uint16),
        ("layersV1Offset", Offset32)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

    def __repr__(self):
        return {'glyphID': self.glyphID, 'layersV1Offset': self.layersV1Offset}.__repr__()
# End of class BaseGlyphV1Record


class BaseGlyphV1List:
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
    ALL_FIELD_NAMES = getCombinedFieldNames(FIELDS, ARRAYS, SUBTABLES)

    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)


class BaseGlyphRecord:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("glyphID", uint16),
        ("firstLayerIndex", uint16),
        ("numLayers", uint16)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

    def __repr__(self):
        return {'glyphID': self.glyphID, 'firstLayerIndex': self.firstLayerIndex, 'numLayers': self.numLayers}.__repr__()
# End of class BaseGlyphRecord


class LayerRecord:
    TYPE_CATEGORY = otTypeCategory.FIXED_LENGTH_BASIC_STRUCT
    FIELDS = OrderedDict([
        ("glyphID", uint16),
        ("paletteIndex", uint16)
        ])
    PACKED_FORMAT = getPackedFormatFromFieldsDef(FIELDS)
    PACKED_SIZE = struct.calcsize(PACKED_FORMAT)
    
    def __init__(self, *args):
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.FIELDS, args):
            setattr(self, f, a)

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
        if not validateArgs(self, *args):
            raise TypeError(f"Wrong arguments were passed to the {type(self)} constructor.")
        for f, a in zip(self.ALL_FIELD_NAMES, args):
            setattr(self, f, a)

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

assertIsWellDefinedOTType(Table_COLR_new)