import struct
from io import BytesIO
from ot_types import *
#inline below: 
#  from ot_font import OTFont, TableRecord



class Table_hhea:

    _expectedTag = "hhea"

    # hhea v1.0 format
    _hhea_1_0_format = ">HH" + "hhh" + "H" + 11 * "h" + "H"
    """ Structure:
        (big endian)                >
        majorVersion: uint16        H
        minorVersion: uint16        H
        ascender: int16             h
        descender: int16            h
        lineGap: int16              h
        advanceWidthMax: uint16     H
        minLeftSideBearing: int16   h
        minRightSideBearing: int16  h
        xMaxExtent: int16           h
        caretSlopeRise: int16       h
        caretSlopeRun: int16        h
        caretOffset: int16          h
        reserved0: int16            h
        reserved1: int16            h
        reserved2: int16            h
        reserved3: int16            h
        metricDataFormat: int16     h
        numberOfHMetrics: uint16    H
    """
    _hhea_1_0_size = struct.calcsize(_hhea_1_0_format)

    _hhea_1_0_fields = (
        "majorVersion",
        "minorVersion",
        "ascender",
        "descender",
        "lineGap",
        "advanceWidthMax",
        "minLeftSideBearing",
        "minRightSideBearing",
        "xMaxExtent",
        "caretSlopeRise",
        "caretSlopeRun",
        "caretOffset",
        "reserved0",
        "reserved1",
        "reserved2",
        "reserved3",
        "metricDataFormat",
        "numberOfHMetrics"
        )

    _hhea_1_0_defaults = (
        1, # majorVersion
        0, # minorVersion
        0, # ascender
        0, # descender
        0, # lineGap
        0, # advanceWidthMax
        0, # minLeftSideBearing
        0, # minRightSideBearing
        0, # xMaxExtent
        0, # caretSlopeRise 
        0, # caretSlopeRun 
        0, # caretOffset 
        0, # reserved0 
        0, # reserved1 
        0, # reserved2 
        0, # reserved3 
        0, # metricDataFormat 
        0  # numberOfHMetrics 
        )

    def __init__(self):
        self.tableTag = Tag(self._expectedTag)


    @staticmethod
    def createNew_hhea():
        """Creates a new version 1.0 hhea table with default values."""

        hhea = Table_hhea()
        for k, v in zip(hhea._hhea_1_0_fields, hhea._hhea_1_0_defaults):
            setattr(hhea, k, v)
        return hhea


    @staticmethod
    def tryReadFromFile(parentFont, tableRecord):
        """Returns a Table_hhea constructed from data in fileBytes. 
        
        Exceptions may be raised if tableRecord.tableTag doesn't match,
        or if tableRecord.offset or .length do not fit within the file."""

        from ot_font import OTFont, TableRecord
        if not (isinstance(parentFont, OTFont) and isinstance(tableRecord, TableRecord)):
            raise Exception()

        hhea = Table_hhea()

        import ot_table
        ot_table.ValidateTableTag(tableRecord, hhea._expectedTag)

        hhea.parentFont = parentFont
        hhea.tableRecord = tableRecord

        # get file bytes, then validate offset/length are in file bounds
        # and that length is as expected for hhea
        fileBytes = parentFont.otFile.fileBytes
        offsetInFile = tableRecord.offset
        ot_table.ValidateOffsetAndLength(
            len(fileBytes), offsetInFile, tableRecord.length,
            hhea._hhea_1_0_size, "hhea"
            )

        # get the table bytes: since offset length are in bounds, get get the expected length
        tableBytes = fileBytes[offsetInFile : offsetInFile + tableRecord.length]
        assert(len(tableBytes) == hhea._hhea_1_0_size)

        # unpack
        vals = struct.unpack(hhea._hhea_1_0_format, tableBytes)
        for k, v in zip(hhea._hhea_1_0_fields, vals):
            setattr(hhea, k, v)

        return hhea
    # End of tryReadFromFile


