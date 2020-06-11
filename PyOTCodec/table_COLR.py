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
    # End of tryReadFromFile

# End of class BaseGlyphRecordsArray



class LayerRecordsArray:
    # The OT spec doesn't define the array as its own struct type, but a class
    # with static methods is used to contain related functionality.

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
    # End of tryReadFromFile

# End of class BaseGlyphRecordsArray


 
class BaseGlyphV1List:
    
    #format/size for List header (not for contained array, which is variable)
    _baseGlyphV1List_format = ">L"
    _baseGlyphV1List_size = struct.calcsize(_baseGlyphV1List_format)
    _baseGlyphV1List_fields = ("numBaseGlyphV1Records",)
    _baseGlyphV1List_defaults = (0)

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

        bgv1List = BaseGlyphV1List()
        bgv1List.numRecords = numRecords
        bgv1List.baseGlyphV1Records = []
        if numRecords > 0:
            bgv1List.baseGlyphV1Records = createNewRecordsArray(
                numRecords,
                BaseGlyphV1List._baseGlyphV1Record_fields,
                BaseGlyphV1List._baseGlyphV1Record_defaults
                )

        return bgv1List
    # End of createNew_BaseGlyphV1List


    @staticmethod
    def tryReadFromFile(fileBytes):
        """Takes a byte sequence and returns a BaseGlyphV1List object read from
        the byte sequence.
        
        The fileBytes argument is assumed to start at the beginning of the 
        BaseGlyphV1List and to contain the header, records array and all
        referenced subtables.
        """

        bgv1List = BaseGlyphV1List()

        # start with header fields -- check length first
        if len(fileBytes) < BaseGlyphV1List._baseGlyphV1List_size:
            raise OTCodecError("The data is not long enough to read the BaseGlyphV1List header fields.")

        vals = struct.unpack(
            BaseGlyphV1List._baseGlyphV1List_format,
            fileBytes[:BaseGlyphV1List._baseGlyphV1List_size]
            )
        for k, v in zip(BaseGlyphV1List._baseGlyphV1List_fields, vals):
            setattr(bgv1List, k, v)
        
        # get records array
        bgv1List.baseGlyphV1Records = tryReadRecordsArrayFromBuffer(
            fileBytes[BaseGlyphV1List._baseGlyphV1List_size:],
            bgv1List.numBaseGlyphV1Records,
            BaseGlyphV1List._baseGlyphV1Record_format,
            BaseGlyphV1List._baseGlyphV1Record_fields,
            "BaseGlyphV1Records"
            )

        # get corresponding LayerV1 tables
        offsets = [d["layersV1Offset"] for d in bgv1List.baseGlyphV1Records]
        bgv1List.layerV1Tables = tryReadSubtablesFromBuffer(
            fileBytes,
            LayersV1,
            offsets
            )

        # TO DO: implement!!

        return bgv1List
    # End of tryReadFromFile

# End of class BaseGlyphV1List



class LayersV1:

    _layersV1List_format = ">L"
    _layersV1List_size = struct.calcsize(_layersV1List_format)
    _layersV1List_fields = ("numLayerV1Records",)
    _layersV1List_defaults = (0)

    # format/size for records
    _layerV1Record_format = ">HL"
    _layerV1Record_size = struct.calcsize(_layerV1Record_format)
    _layerV1Record_fields = ("glyphID", "paintOffset")
    _layerV1Record_defaults = (0, 0)


    @staticmethod
    def createNew_LayersV1():
        pass
        # !!! TO DO: IMPLEMENT !!!


    @staticmethod
    def tryReadFromFile(fileBytes):

        layersv1 = LayersV1()

        # start with header fields -- check length first
        if len(fileBytes) < LayersV1._layersV1List_size:
            raise OTCodecError("The data is not long enough to read the LayersV1 header fields.")

        vals = struct.unpack(
            LayersV1._layersV1List_format,
            fileBytes[:LayersV1._layersV1List_size]
            )
        for k, v in zip(LayersV1._layersV1List_fields, vals):
            setattr(layersv1, k, v)

        # get records array
        layersv1.layerV1Records = tryReadRecordsArrayFromBuffer(
            fileBytes[LayersV1._layersV1List_size:],
            layersv1.numLayerV1Records,
            LayersV1._layerV1Record_format,
            LayersV1._layerV1Record_fields,
            "LayerV1Records"
            )

        # get corresponding Paint tables
        pass
        # !!! TO DO: IMPLEMENT !!!

        return layersv1
    # End of tryReadFromFile

# End of class LayersV1