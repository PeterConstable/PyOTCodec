import struct
from io import BytesIO
from ot_types import *


class Table_COLR:

    
    _expectedTag = "COLR"

    _colr_version = ">H"
    _colr_version_size = struct.calcsize(_colr_version)

    _colr_0_format = ">HHLLH"
    """ Structure:
        (big endian)                        >
        version                 uint16      H
        numBaseGlyphRecords     uint16      H
        baseGlyphRecordsOffset  Offset32    L
        layerRecordsOffset      Offset32    L
        numLayerRecords         uint16      H
    """

    _colr_0_size = struct.calcsize(_colr_0_format)

    _colr_0_fields = (
        "version",
        "numBaseGlyphRecords",
        "baseGlyphRecordsOffset",
        "layerRecordsOffset",
        "numLayerRecords"
        )

    _colr_0_defaults = (0, 0, 0, 0, 0)

    
    # COLR version 1 format is preliminary

    _colr_1_addl_format = ">LL"
    """ Structure:
        baseGlyphV1ListOffset    Offset32   L
        itemVariationStoreOffset Offset32   L
    """

    _colr_1_addl_size = struct.calcsize(_colr_1_addl_format)

    _colr_1_addl_fields = (
        "baseGlyphV1ListOffset",
        "itemVariationStoreOffset"
        )

    _colr_1_addl_defaults = (0, 0)

    _colr_1_all_fields = _colr_0_fields + _colr_1_addl_fields
    _colr_1_all_defaults = _colr_0_defaults + _colr_1_addl_defaults



    def __init__(self):
        self.tableTag = Tag(self._expectedTag)


    @staticmethod
    def createNew_COLR(version:int):
        """Creates a new version 0 or version 1 COLR table with default values.
        
        Only the header and empry record arrays are created; no records or 
        subtables are added.
        """

        if int(version) > 1:
            raise OTCodecError(f"Version {version} of the COLR table is not supported.")

        colr = Table_COLR()

        for k, v in zip(colr._colr_0_fields, colr._colr_0_defaults):
            setattr(colr, k, v)

        colr.baseGlyphRecords = []
        colr.layerRecords = []

        if version == 1:
            for k, v in zip(colr._colr_1_addl_fields, colr._colr_1_addl_defaults):
                setattr(colr, k, v)

        return colr
    # End of createNew_colr


    @staticmethod
    def tryReadFromFile(parentFont, tableRecord):
        """Returns a Table_colr constructed from data in fileBytes.
        
        Exceptions may be raised if tableRecord.tableTag doesn't match,
        or if tableRecord.offset or .length do not fit within the file.
        """

        colr = Table_COLR()

        from ot_font import OTFont, TableRecord
        if not (isinstance(parentFont, OTFont) and isinstance(tableRecord, TableRecord)):
            raise Exception()

        import ot_table
        ot_table.ValidateTableTag(tableRecord, colr._expectedTag)

        colr.parentFont = parentFont
        colr.tableRecord = tableRecord

        # get file bytes, then validate offset/length are in file bounds
        fileBytes = parentFont.fileBytes
        offsetInFile = tableRecord.offset
        ot_table.ValidateOffsetAndLength(
            len(fileBytes), offsetInFile, tableRecord.length
            )

        # get the table bytes: since offset length are in bounds, can get the expected length
        tableBytes = fileBytes[offsetInFile : offsetInFile + tableRecord.length]

        # only minor versions, so at least version 0 fields are supported
        if len(tableBytes) < colr._colr_0_size:
            raise OTCodecError("File isn't long enough to read COLR version 0 fields.")
        vals = struct.unpack(colr._colr_0_format, tableBytes[:colr._colr_0_size])
        for k, v in zip(colr._colr_0_fields, vals):
            setattr(colr, k, v)

        if colr.version > 0:
            # at least version 1 fields are supported
            vals = struct.unpack(
                colr._colr_1_addl_format, 
                tableBytes[colr._colr_0_size : colr._colr_0_size + colr._colr_1_addl_size]
                )
            for k, v in zip(colr._colr_1_addl_fields, vals):
                setattr(colr, k, v)


        # Finished with header fields. On to arrays and subtables...

        # BaseGlyphRecords array
        colr.baseGlyphRecords = []
        if colr.baseGlyphRecordsOffset > 0:
            colr.baseGlyphRecords = BaseGlyphRecordsArray.tryReadFromFile(
                tableBytes[colr.baseGlyphRecordsOffset: ],
                colr.numBaseGlyphRecords
                )

        # LayerRecords array
        colr.layerRecords = []
        if colr.layerRecordsOffset > 0:
            colr.layerRecords = LayerRecordsArray.tryReadFromFile(
                tableBytes[colr.layerRecordsOffset:],
                colr.numLayerRecords
                )

        # version 1 data
        if colr.version > 0:
            if colr.baseGlyphV1ListOffset > 0:
                colr.baseGlyphV1 = BaseGlyphV1List.tryReadFromFile(
                    tableBytes[colr.baseGlyphV1ListOffset:]
                    )

            if colr.itemVariationStoreOffset > 0:
                # !!! TO DO: IMPLEMENT !!!
                pass


        # calculate checksum (should match what's in TableRecord)
        from ot_file import calcCheckSum
        colr.calculatedCheckSum = calcCheckSum(tableBytes)

        return colr
    # End of tryReadFromFile

# End of class Table_COLR



class BaseGlyphRecordsArray:
    # The OT spec doesn't define the array as its own struct type, but a class
    # with static methods is used to contain related functionality.

    _packedFormat = ">3H"
    _packedSize = struct.calcsize(_packedFormat)

    _fieldNames = ("glyphID", "firstLayerIndex", "numLayers")
    _defaultValues = (0, 0, 0)


    @staticmethod
    def createNew_BaseGlyphRecordsArray(numRecords):
        """Returns a list of BaseGlyphRecord dicts with default values."""

        return createNewRecordsArray(
            numRecords,
            BaseGlyphRecordsArray._fieldNames, 
            BaseGlyphRecordsArray._defaultValues
            )


    @staticmethod
    def tryReadFromFile(fileBytes, numRecords):
        """Takes a byte sequence that comprises the BaseGlyphRecords array from
        the font file and returns a list of BaseGlyphRecord dicts read from the 
        byte sequence."""

        # ot_types.tryReadRecordsArrayFromBuffer will validated array fits within fileBytes
        return tryReadRecordsArrayFromBuffer(
            fileBytes, 
            numRecords,
            BaseGlyphRecordsArray._packedFormat,
            BaseGlyphRecordsArray._fieldNames,
            "BaseGlyphRecords"
            )

# End of class BaseGlyphRecordsArray



class LayerRecordsArray:
    # The OT spec doesn't define the array as its own struct type, but a class
    # with static methods is used to contain related functionality.

    _packedFormat = ">2H"
    _packedSize = struct.calcsize(_packedFormat)

    _fieldNames = ("glyphID", "paletteIndex")
    _defaultValues = (0, 0)


    @staticmethod
    def createNew_layerRecordsArray(numRecords):
        """Returns a list of LayerRecord dicts with default values."""

        return createNewRecordsArray(
            numRecords,
            LayerRecordsArray._fieldNames, 
            LayerRecordsArray._defaultValues
            )


    @staticmethod
    def tryReadFromFile(fileBytes, numRecords):
        """Takes a byte sequence that begins at the LayerRecords array and
        returns a list of LayerRecord dicts read from the byte sequence."""

        # ot_types.tryReadRecordsArrayFromFile will validated array fits within fileBytes
        return tryReadRecordsArrayFromBuffer(
            fileBytes, 
            numRecords,
            LayerRecordsArray._packedFormat,
            LayerRecordsArray._fieldNames,
            "LayerRecords"
            )

# End of class BaseGlyphRecordsArray



class VarFixed:
    """Representation of OpenType Fixed type combined with an ItemVariationStore index."""

    _packedFormat = Fixed._packedFormat + "2H"
    """ Structure:
        (big endian)            >
        value           Fixed
        varOuterIndex   uint16  H
        varInnerIndex   uint16  H
    """
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("value", "varOuterIndex", "varInnerIndex")
    _numUnpackedValues = Fixed._numUnpackedValues + 2


    def __init__(self, fixedNum:int, varOuterIndex:int, varInnerIndex:int):
        self.value = Fixed.createNewFixedFromUint32(fixedNum)
        self.varOuterIndex = varOuterIndex
        self.varInnerIndex = varInnerIndex


    @staticmethod
    def interpretUnpackedValues(*vals):
        """Takes a tuple of raw values obtained from struct.unpack() and returns
        a tuple of derived values corresponding to the structure fields."""

        assert len(vals) == VarFixed._numUnpackedValues
        value = Fixed.interpretUnpackedValues(*vals[:Fixed._numUnpackedValues])
        return value, vals[1], vals[2]


    def __repr__(self):
        return {"value": self.value, "varOuterIndex": self.varOuterIndex, "varInnerIndex": self.varInnerIndex}.__repr__()

# End of class VarFixed



class VarF2Dot14:
    """Representation of OpenType F2Dot14 type combined with an ItemVariationStore index."""

    _packedFormat = F2Dot14._packedFormat + "2H"
    """ Structure:
        (big endian)            >
        value           F2Dot14
        varOuterIndex   uint16  H
        varInnerIndex   uint16  H
    """
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("value", "varOuterIndex", "varInnerIndex")
    _numUnpackedValues = F2Dot14._numUnpackedValues + 2


    @staticmethod
    def interpretUnpackedValues(*vals):
        """Takes a tuple of raw values obtained from struct.unpack() and returns
        a tuple of derived values corresponding to the structure fields."""

        assert len(vals) == VarF2Dot14._numUnpackedValues
        value = F2Dot14.interpretUnpackedValues(*vals[:F2Dot14._numUnpackedValues])
        return value, vals[1], vals[2]


    def __init__(self, f2Dot14Num:int, varOuterIndex:int, varInnerIndex:int):
        self.value = F2Dot14.createNewF2Dot14FromUint16(f2Dot14Num)
        self.varOuterIndex = varOuterIndex
        self.varInnerIndex = varInnerIndex

    def __repr__(self):
        return {"value": self.value, "varOuterIndex": self.varOuterIndex, "varInnerIndex": self.varInnerIndex}.__repr__()

# End of class VarF2Dot14



class VarFWord:
    """Representation of OpenType FWord type combined with an ItemVariationStore index."""

    _packedFormat = ">h2H"
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("coordinate", "varOuterIndex", "varInnerIndex")
    _numPackedValues = 3


    def __init__(self, coordinate, varOuterIndex, varInnerIndex):
        self.coordinate = coordinate
        self.varOuterIndex = varOuterIndex
        self.varInnerIndex = varInnerIndex

    def __repr__(self):
        return {"coordinate": self.coordinate, "varOuterIndex": self.varOuterIndex, "varInnerIndex": self.varInnerIndex}.__repr__()

# End of class VarFWord



class VarUFWord:
    """Representation of OpenType UFWord type combined with an ItemVariationStore index."""

    _packedFormat = ">3H"
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("distance", "varOuterIndex", "varInnerIndex")
    _numPackedValues = 3


    def __init__(self, distance, varOuterIndex, varInnerIndex):
        self.distance = distance
        self.varOuterIndex = varOuterIndex
        self.varInnerIndex = varInnerIndex

    def __repr__(self):
        return {"distance": self.distance, "varOuterIndex": self.varOuterIndex, "varInnerIndex": self.varInnerIndex}.__repr__()

# End of class VarUFWord



class Affine2x2:

    _packedFormat = concatFormatStrings(
        VarFixed._packedFormat,
        VarFixed._packedFormat,
        VarFixed._packedFormat,
        VarFixed._packedFormat
        )
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("xx", "xy", "yx", "yy")


    def __init__(self, xx:VarFixed, xy:VarFixed, yx:VarFixed, yy:VarFixed):
        self.xx = xx
        self.xy = xy
        self.yx = yx
        self.yy = yy

    @staticmethod
    def interpretUnpackedValues(*vals):
        """Takes a tuple of raw values obtained from struct.unpack() and returns
        a tuple of derived values corresponding to the structure fields."""

        assert len(vals) == Affine2x2._numUnpackedValues

        xx = VarFixed.interpretUnpackedValues(*vals[:VarFixed._numUnpackedValues])
        xy = VarFixed.interpretUnpackedValues(*vals[VarFixed._numUnpackedValues : 2 * VarFixed._numUnpackedValues])
        yx = VarFixed.interpretUnpackedValues(*vals[2 * VarFixed._numUnpackedValues : 3 * VarFixed._numUnpackedValues])
        yy = VarFixed.interpretUnpackedValues(*vals[3 * VarFixed._numUnpackedValues : ])

        return xx, xy, yx, yy

    def tryReadFromFile(fileBytes):

        if len(fileBytes) < Affine2x2._packedSize:
            raise OTCodecError("The data is not long enough to read the Affine2x2 table.")

        vals = struct.unpack(Affine2x2._packedFormat, fileBytes[:Affine2x2._packedSize])
        tableVals = []
        for i in range(4):
            tableVals.append(
                VarFixed.interpretUnpackedValues(*vals[i * VarFixed._numUnpackedValues: (i + 1) * VarFixed._numUnpackedValues])
                )
        return Affine2x2(*tableVals)


    def __repr__(self):
        return {'xx': self.xx, 'xy': self.xy, 'yx': self.yx, 'yy': self.yy}.__repr__()

# End of class Affine2x2



class ColorIndex:
    """Representation of a palette index combined with an alpha that is variable."""

    _packedFormat = concatFormatStrings(">H", VarF2Dot14._packedFormat)
    """ Structure:
        (big endian)                >
        paletteIndex    uint16      H
        alpha           VarF2Dot14
    """
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("paletteIndex", "alpha")
    _numUnpackedValues = 1 + VarF2Dot14._numUnpackedValues


    def __init__(self, paletteIndex:int, alpha:VarF2Dot14):
        if alpha.value.value < 0 or alpha.value.value > 1:
            raise OTCodecError(f"The alpha argument is invalid: value must be in the range [0, 1].")
        self.paletteIndex = paletteIndex
        self.alpha = alpha


    @staticmethod
    def interpretUnpackedValues(*vals):
        """Takes a tuple of raw values obtained from struct.unpack() and returns
        a tuple of derived values corresponding to the structure fields."""

        assert len(vals) == ColorIndex._numUnpackedValues

        alpha = VarF2Dot14.interpretUnpackedValues(*vals[1:])
        return vals[0], alpha


    def __repr__(self):
        return {"paletteIndex": self.paletteIndex, "alpha": self.alpha}.__repr__()

# End of class ColorIndex



class ColorStop:
    """Representation of a color stop: a variable stop offset (range [0, 1]) plus a ColorIndex."""

    _packedFormat = concatFormatStrings(VarF2Dot14._packedFormat, ColorIndex._packedFormat)
    """ Structure:
        (big endian)                >
        stopOffset      VarF2Dot14
        color           ColorIndex
    """
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("stopOffset", "color")
    _numUnpackedValues = VarF2Dot14._numUnpackedValues + ColorIndex._numUnpackedValues


    def __init__(self, stopOffset:VarF2Dot14, color:ColorIndex):
        if stopOffset.value.value < 0 or stopOffset.value.value > 1:
            raise OTCodecError(f"The stopOffset argument is invalid: value must be in the range [0, 1].")
        self.stopOffset = stopOffset
        self.color = color


    @staticmethod
    def interpretUnpackedValues(*vals):
        """Takes a tuple of raw values obtained from struct.unpack() and returns
        a tuple of derived values corresponding to the structure fields."""

        assert len(vals) == ColorStop._numUnpackedValues

        stopOffset = VarF2Dot14.interpretUnpackedValues(*vals[:VarF2Dot14._numUnpackedValues])
        color = ColorIndex.interpretUnpackedValues(*vals[VarF2Dot14._numUnpackedValues:])
        return stopOffset, color


    def __repr__(self):
        return {'stopOffset': self.stopOffset, 'color': self.color}.__repr__()

# End of class ColorStop



class ColorLine:

    #format size for ColorLine header (not for contained ColorStop array)
    _packedFormat = ">2H"
    """ Structure:
        (big endian)            >
        extend          uint16  H
        numStops        uint16  H
    """
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("extend", "numStops")
    _defaultValues = (0, 0)


    @staticmethod
    def createNew_ColorLine():
        """Returns a ColorLine object initialized with default values.
        
        The returned ColorLine object will have an empty colorStops list.
        """
        colorLine = ColorLine()
        for k, v in zip(ColorLine._fieldNames, ColorLine._defaultValues):
            setattr(colorLine, k, v)

        return colorLine

    @staticmethod
    def tryReadFromFile(fileBytes):

        colorLine = ColorLine()

        # start with header fields -- check length first
        if len(fileBytes) < ColorLine._packedSize:
            raise OTCodecError("The data is not long enough to read the ColorLine header fields.")

        vals = struct.unpack(
            ColorLine._packedFormat,
            fileBytes[:ColorLine._packedSize]
            )
        for k, v in zip(ColorLine._fieldNames, vals):
            setattr(colorLine, k, v)

        # now get array of ColorStop records
        colorLine.colorStops = []
        if colorLine.numStops > 0:
            colorLine.colorStops = tryReadComplexRecordsArrayFromBuffer(
                fileBytes[ColorLine._packedSize:],
                colorLine.numStops,
                ColorStop._packedFormat,
                ColorStop._fieldNames,
                ColorStop,
                "colorStops"
                )

        return colorLine
# End of class ColorLine



class PaintFormat1:

    _packedFormat = concatFormatStrings(">H", ColorIndex._packedFormat)
    """ Structure:
        (big endian)                >
        format          uint16      H
        color           ColorIndex
    """
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("format", "color")
    

    def tryReadFromFile(fileBytes):

        if len(fileBytes) < PaintFormat1._packedSize:
            raise OTCodecError("The data is not long enough to read the PaintFormat1 table.")

        paint = PaintFormat1()

        vals = struct.unpack(
            PaintFormat1._packedFormat,
            fileBytes[:PaintFormat1._packedSize]
            )

        color = ColorIndex.interpretUnpackedValues(*vals[1:])

        for k, v in zip(PaintFormat1._fieldNames, (vals[0], color)):
            setattr(paint, k, v)

        return paint

# End of class PaintFormat1



class PaintFormat2:
    
    _packedFormat = concatFormatStrings(
        ">HL", 
        VarFWord._packedFormat, 
        VarFWord._packedFormat, 
        VarFWord._packedFormat, 
        VarFWord._packedFormat, 
        VarFWord._packedFormat, 
        VarFWord._packedFormat
        )
    """ Structure:
        (big endian)                >
        format          uint16      H
        colorLineOffset Offset32    L
        x0              VarFWord
        y0              VarFWord
        x1              VarFWord
        y1              VarFWord
        x2              VarFWord
        y2              VarFWord
    """
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("format", "colorLineOffset", "x0", "y0", "x1", "y1", "x2", "y2")


    def tryReadFromFile(fileBytes):

        if len(fileBytes) < PaintFormat2._packedSize:
            raise OTCodecError("The data is not long enough to read the PaintFormat1 table.")

        paint = PaintFormat2()

        vals = struct.unpack(
            PaintFormat2._packedFormat,
            fileBytes[:PaintFormat2._packedSize]
            )
        tableVals = [*vals[:2]]
        for i in range(2, len(vals), VarFWord._numPackedValues):
            tableVals.append(VarFWord(*vals[i : i + VarFWord._numPackedValues]))

        for k, v in zip(PaintFormat2._fieldNames, tableVals):
            setattr(paint, k, v)

        # get ColorLine
        paint.colorLine = None
        if paint.colorLineOffset > 0:
            paint.colorLine = ColorLine.tryReadFromFile(fileBytes[paint.colorLineOffset:])

        return paint

# End of class PaintFormat2



class PaintFormat3:
    _packedFormat = concatFormatStrings(
        ">hL",
        VarFWord._packedFormat,
        VarFWord._packedFormat,
        VarFWord._packedFormat,
        VarFWord._packedFormat,
        VarUFWord._packedFormat,
        VarUFWord._packedFormat,
        "L"
        )
    """ Structure:
        (big endian)                >
        format          uint16      H
        colorLineOffset Offset32    L
        x0              VarFWord
        y0              VarFWord
        x1              VarFWord
        y1              VarFWord
        radius0         VarUFWord
        radius1         VarUFWord
        transformOffset Offset32    L
    """
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("format", "colorLineOffset", "x0", "y0", "x1", "y1", "radius0", "radius1", "transformOffset")


    def tryReadFromFile(fileBytes):

        if len(fileBytes) < PaintFormat3._packedSize:
            raise OTCodecError("The data is not long enough to read the PaintFormat1 table.")

        paint = PaintFormat3()

        vals = struct.unpack(
            PaintFormat3._packedFormat,
            fileBytes[:PaintFormat3._packedSize]
            )
        tableVals = [*vals[:2]]
        for i in range(2, 2 + 4 * VarFWord._numPackedValues, VarFWord._numPackedValues):
            tableVals.append(VarFWord(*vals[i : i + VarFWord._numPackedValues]))
        for i in range(
                2 + 4 * VarFWord._numPackedValues, 
                2 + 4 * VarFWord._numPackedValues + 2 * VarUFWord._numPackedValues, 
                VarUFWord._numPackedValues
                ):
            tableVals.append(VarUFWord(*vals[i : i + VarUFWord._numPackedValues]))
        tableVals.append(*vals[-1:])

        for k, v in zip(PaintFormat3._fieldNames, tableVals):
            setattr(paint, k, v)

        # get ColorLine
        paint.colorLine = None
        if paint.colorLineOffset > 0:
            paint.colorLine = ColorLine.tryReadFromFile(fileBytes[paint.colorLineOffset:])

        # get transform
        paint.transform = None
        if paint.transformOffset > 0:
            paint.transform = Affine2x2.tryReadFromFile(fileBytes[paint.transformOffset:])

        return paint

# End of class PaintFormat3



class BaseGlyphV1List:

    #format/size for List header (not for contained array, which is variable)
    _packedFormat = ">L"
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("numBaseGlyphV1Records",)
    _defaultValues = (0)

    # format/size for records
    _baseGlyphV1Record_format = ">HL"
    _baseGlyphV1Record_size = struct.calcsize(_baseGlyphV1Record_format)
    _baseGlyphV1Record_fields = ("glyphID", "layersV1Offset")
    _baseGlyphV1Record_defaults = (0, 0)


    @staticmethod
    def createNew_BaseGlyphV1List(numRecords):
        """Returns a BaseGlyphV1List object initialized with default values.
        
        An array of records with default values is created, but no
        corresponding array of LayersV1 subtables is created."""

        bgV1List = BaseGlyphV1List()
        bgV1List.numRecords = numRecords
        bgV1List.baseGlyphV1Records = []
        if numRecords > 0:
            bgV1List.baseGlyphV1Records = createNewRecordsArray(
                numRecords,
                BaseGlyphV1List._baseGlyphV1Record_fields,
                BaseGlyphV1List._baseGlyphV1Record_defaults
                )

        return bgV1List
    # End of createNew_BaseGlyphV1List


    @staticmethod
    def tryReadFromFile(fileBytes):
        """Takes a byte sequence and returns a BaseGlyphV1List object read from
        the byte sequence.
        
        The fileBytes argument is assumed to start at the beginning of the 
        BaseGlyphV1List and to contain the header, records array and all
        referenced subtables.
        """

        bgV1List = BaseGlyphV1List()

        # start with header fields -- check length first
        if len(fileBytes) < BaseGlyphV1List._packedSize:
            raise OTCodecError("The data is not long enough to read the BaseGlyphV1List header fields.")

        vals = struct.unpack(
            BaseGlyphV1List._packedFormat,
            fileBytes[:BaseGlyphV1List._packedSize]
            )
        for k, v in zip(BaseGlyphV1List._fieldNames, vals):
            setattr(bgV1List, k, v)
        
        # get records array
        if bgV1List.numBaseGlyphV1Records > 0:

            bgV1List.baseGlyphV1Records = tryReadRecordsArrayFromBuffer(
                fileBytes[BaseGlyphV1List._packedSize:],
                bgV1List.numBaseGlyphV1Records,
                BaseGlyphV1List._baseGlyphV1Record_format,
                BaseGlyphV1List._baseGlyphV1Record_fields,
                "BaseGlyphV1Records"
                )

            # get corresponding LayerV1 tables
            offsets = [d["layersV1Offset"] for d in bgV1List.baseGlyphV1Records]
            bgV1List.layerV1Tables = tryReadSubtablesFromBuffer(
                fileBytes,
                LayersV1,
                offsets
                )

        return bgV1List
    # End of tryReadFromFile

# End of class BaseGlyphV1List



class LayersV1:

    _packedFormat = ">L"
    _packedSize = struct.calcsize(_packedFormat)
    _fieldNames = ("numLayerV1Records",)
    _defaultValues = (0)

    # format/size for records
    _layerV1Record_format = ">HL"
    _layerV1Record_size = struct.calcsize(_layerV1Record_format)
    _layerV1Record_fields = ("glyphID", "paintOffset")
    _layerV1Record_defaults = (0, 0)


    @staticmethod
    def createNew_LayersV1(numRecords):
        """Returns a BaseGlyphV1List object initialized with default values.
        
        An array of records with default values is created, but no
        corresponding array of LayersV1 subtables is created."""

        layersV1 = LayersV1()
        layersV1.numRecords = numRecords
        layersV1.layerV1Records = []
        if numRecords > 0:
            layersV1.layerV1Records = createNewRecordsArray(
                numRecords,
                LayersV1._fieldNames,
                LayersV1._defaultValues
                )

        return layersV1
    # End of createNew_LayersV1


    @staticmethod
    def tryReadFromFile(fileBytes):

        layersV1 = LayersV1()

        # start with header fields -- check length first
        if len(fileBytes) < LayersV1._packedSize:
            raise OTCodecError("The data is not long enough to read the LayersV1 header fields.")

        vals = struct.unpack(
            LayersV1._packedFormat,
            fileBytes[:LayersV1._packedSize]
            )
        for k, v in zip(LayersV1._fieldNames, vals):
            setattr(layersV1, k, v)

        # get records array
        layersV1.layerV1Records = tryReadRecordsArrayFromBuffer(
            fileBytes[LayersV1._packedSize:],
            layersV1.numLayerV1Records,
            LayersV1._layerV1Record_format,
            LayersV1._layerV1Record_fields,
            "LayerV1Records"
            )

        # get corresponding Paint tables
        offsets = [d["paintOffset"] for d in layersV1.layerV1Records]
        paintClasses = {1: PaintFormat1, 2: PaintFormat2, 3: PaintFormat3}
        layersV1.paintTableFormats, layersV1.paintTables = tryReadMultiFormatSubtablesFromBuffer(
            fileBytes,
            paintClasses,
            offsets
            )

        return layersV1
    # End of tryReadFromFile

# End of class LayersV1