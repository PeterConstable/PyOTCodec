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
        
        Only the header is created; no record arrays or subtables are added.
        """

        if int(version) > 1:
            raise OTCodecError(f"Version {version} of the COLR table is not supported.")

        colr = Table_COLR()

        for k, v in zip(colr._colr_0_fields, colr._colr_0_defaults):
            setattr(colr, k, v)

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
            vals = struct.unpack(colr._colr_1_addl_format, tableBytes[colr._colr_0_size:])
            for k, v in zip(colr._colr_1_addl_fields, vals):
                setattr(colr, k, v)

        # calculate checksum (should match what's in TableRecord)
        from ot_file import calcCheckSum
        colr.calculatedCheckSum = calcCheckSum(tableBytes)

        # Finished with header fields. On to details...

        # BaseGlyphRecords array
        arrayLength = colr.numBaseGlyphRecords * BaseGlyphRecordsArray._baseGlyphRecord_size
        colr.baseGlyphRecords = []
        if colr.baseGlyphRecordsOffset > 0:
            colr.baseGlyphRecords = BaseGlyphRecordsArray.tryReadFromFile(
                tableBytes[colr.baseGlyphRecordsOffset: colr.baseGlyphRecordsOffset + arrayLength],
                colr.numBaseGlyphRecords
                )

        # LayerRecords array
        arrayLength = colr.numLayerRecords * LayerRecordsArray._layerRecord_size
        colr.layerRecords = []
        if colr.layerRecordsOffset > 0:
            colr.layerRecords = LayerRecordsArray.tryReadFromFile(
                tableBytes[colr.layerRecordsOffset:colr.layerRecordsOffset + arrayLength],
                colr.numLayerRecords
                )

        # version 1 data
        if colr.version > 0:
            # TO DO: IMPLEMENT!!
            pass


        # calculate checksum (should match what's in TableRecord)
        from ot_file import calcCheckSum
        colr.calculatedCheckSum = calcCheckSum(tableBytes)

        return colr
    # End of tryReadFromFile

# End of class Table_COLR



class BaseGlyphRecordsArray:

    _baseGlyphRecord_format = ">3H"
    _baseGlyphRecord_size = struct.calcsize(_baseGlyphRecord_format)

    _baseGlyphRecord_fields = ("glyphID", "firstLayerIndex", "numLayers")
    _baseGlyphRecord_defaults = (0, 0, 0)


    @staticmethod
    def createNew_BaseGlyphRecordsArray(numRecords):
        """Returns a list of BaseGlyphRecord dicts with default values."""

        return createNewRecordsArray(
            numRecords,
            BaseGlyphRecordsArray._baseGlyphRecord_fields, 
            BaseGlyphRecordsArray._baseGlyphRecord_defaults
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
            BaseGlyphRecordsArray._baseGlyphRecord_format,
            BaseGlyphRecordsArray._baseGlyphRecord_fields,
            "BaseGlyphRecords"
            )

        # check that array fits in the byte sequence provided
        arrayLength = numRecords * BaseGlyphRecordsArray._baseGlyphRecord_size
        if len(fileBytes) < arrayLength:
            raise OTCodecError(f"The table is not long enough for {numRecords} BaseGlyphRecords.")

        array = []
        for i in range(numRecords):
            bgr = {}
            vals = struct.unpack(
                BaseGlyphRecordsArray._baseGlyphRecord_format,
                fileBytes[:arrayLength]
                )
            for k, v in zip(BaseGlyphRecordsArray._baseGlyphRecord_fields, vals):
                bgr[k] = v
            array.append(bgr)

        return array


class LayerRecordsArray:

    _layerRecord_format = ">2H"
    _layerRecord_size = struct.calcsize(_layerRecord_format)

    _layerRecord_fields = ("glyphID", "paletteIndex")
    _layerRecord_defaults = (0, 0)


    @staticmethod
    def createNew_layerRecordsArray(numRecords):
        """Returns a list of LayerRecord dicts with default values."""

        return createNewRecordsArray(
            numRecords,
            LayerRecordsArray._layerRecord_fields, 
            LayerRecordsArray._layerRecord_defaults
            )


    @staticmethod
    def tryReadFromFile(fileBytes, numRecords):
        """Takes a byte sequence that begins at the LayerRecords array and
        returns a list of LayerRecord dicts read from the byte sequence."""

        # ot_types.tryReadRecordsArrayFromFile will validated array fits within fileBytes
        return tryReadRecordsArrayFromBuffer(
            fileBytes, 
            numRecords,
            LayerRecordsArray._layerRecord_format,
            LayerRecordsArray._layerRecord_fields,
            "LayerRecords"
            )

 
class BaseGlyphRecordsV1List:
    pass