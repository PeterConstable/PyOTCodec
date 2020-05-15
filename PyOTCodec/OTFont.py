import struct
from pathlib import Path
from io import BytesIO
from OTTypes import *
from OTFile import *

class OTFont:
    """Represents a font resource: one font within a TTC, or the font of the entire file if not a TTC."""

    def __init__(self, otFile, offsetInFile: int = 0, ttcIndex: int = None):
        self.otFile = otFile
        if offsetInFile > len(otFile.fileBytes):
            raise OTCodecError("The file offset for the font is greater than the length of the file")
        self.offsetInFile = offsetInFile
        if ttcIndex is not None and ttcIndex >= otFile.numFonts:
            raise OTCodecError("The ttcIndex argument is greater than the last font index (numFonts - 1)")
        self.ttcIndex = ttcIndex
        self.isWithinTtc = False if ttcIndex is None else True
        self.offsetTable = OffsetTable(otFile.fileBytes, offsetInFile)
        self.tables: dict = {}
        self.defaultLabel = otFile.path.name if ttcIndex is None \
                            else otFile.path.name + ":" + str(ttcIndex)

    def sfntVersionTag(self):
        return self.offsetTable.sfntVersion

    def ContainsTable(self, tag:Tag):
        return (tag in self.offsetTable.tableRecords)

    def TryGetTableOffset(self, tag:Tag):
        """If the specified table is present in the font, gets the offset from the start of the font. 
        
        If the specified table is not present, returns None.
        """
        tableRecord = self.offsetTable.TryGetTableRecord(tag)
        if tableRecord is None:
            return None
        else:
            return tableRecord.offset

    @staticmethod
    def IsSupportedSfntVersion(tag:Tag):
        if tag not in (b'\x00\x01\x00\x00', "OTTO", "true"):
            return False
        else:
            return True

    @staticmethod
    def IsKnownTableType(tag:Tag):
        if tag in (
                    # OT tables:
                    "avar", "BASE", "CBDT", "CBLC", "CFF ", "CFF2", "cmap", "COLR", 
                    "CPAL", "cvar", "cvt ", "DSIG", "EBDT", "EBLC", "EBSC", "fpgm", 
                    "fvar", "gasp", "GDEF", "glyf", "GPOS", "GSUB", "gvar", "hdmx", 
                    "head", "hhea", "hmtx", "HVAR", "JSTF", "kern", "loca", "LTSH", 
                    "MATH", "maxp", "MERG", "meta", "MVAR", "name", "OS/2", "PCLT", 
                    "post", "prep", "sbix", "STAT", "SVG ", "VDMX", "vhea", "vmtx", 
                    "VORG", "VVAR",

                    # Apple-specific tables:
                    "acnt", "ankr", "bdat", "bhed", "bloc", "bsln", "fdsc", "feat", 
                    "fmtx", "fond", "gcid", "hsty", "just", "lcar", "ltag", "mort", 
                    "morx", "opbd", "prop", "trak", "xref", "Zapf", 

                    # SIL Graphite tables:
                    "Feat", "Glat", "Gloc", "Sill", "Silf", 

                    # VOLT, VTT source tables:
                    "TSIV", "TSI0", "TSI1", "TSI2", "TSI3", "TSI5"
                    ):
            return True
        else:
            return False

    @staticmethod
    def IsSupportedTableType(tag:Tag):
        if tag in ("hhea"):
            return True
        else:
            return False


# End of class OTFont



class TableRecord:

    _tableRecordFormat = ">4sLLL"
    """ Structure:
        (big-endian)        >
        tableTag: Tag       L
        checkSum: uint32    L
        offset: uint32      L
        length: uint32      L
    """
    size = struct.calcsize(_tableRecordFormat)

    def __init__(self, buffer:bytearray):
        assert (len(buffer) == TableRecord.size), "Wrong size of buffer for TableRecord"
        tmp = struct.unpack(TableRecord._tableRecordFormat, buffer)
        self.tableTag = Tag(tmp[0])
        self.checkSum, self.offset, self.length = tmp[1:4]


class OffsetTable:

    # fields prior to the TableRecords array
    _offsetTableHeaderFormat = ">4sHHHH"
    """ Structure:
        (big-endian)            >
        sfntVersion: Tag        4s
        numTables: uint16       H
        searchRange: uint16     H
        entrySelector: uint16   H
        rangeShift: uint16      H
    """
    _offsetTableHeaderSize = struct.calcsize(_offsetTableHeaderFormat)


    def __init__(self, fileBytes:bytearray, offsetInFile: int):
        self.offsetInFile = offsetInFile
        self.sfntVersion: Tag = None
        self.numTables, self.searchRange, self.entrySelector, self.rangeShift = 0, 0, 0, 0
        self.tableRecords: dict = {}

        # get the header
        headerBytes = fileBytes[offsetInFile : offsetInFile + OffsetTable._offsetTableHeaderSize]
        if len(headerBytes) < OffsetTable._offsetTableHeaderSize:
            raise OTCodecError("Unable to read OffsetTable from file at {:#08x}".format(offsetInFile))
        tmp = struct.unpack(OffsetTable._offsetTableHeaderFormat, headerBytes)
        self.sfntVersion = Tag(tmp[0])
        self.numTables, self.searchRange, self.entrySelector, self.rangeShift = tmp[1:5]

        # get the table records -- we'll wrap BytesIO around fileBytes to provide sequential reading
        filebio = BytesIO(fileBytes)
        filebio.seek(offsetInFile + OffsetTable._offsetTableHeaderSize)
        for i in range(self.numTables):
            recData = filebio.read(TableRecord.size)
            if len(recData) < TableRecord.size:
                raise OTCodecError("Unable to read TableRecord from file")
            record = TableRecord(recData)
            self.tableRecords[record.tableTag] = record

    def TryGetTableRecord(self, tag:Tag):
        """Returns the table record matching the specified tag, if present. If not present, returns None."""
        if not tag in self.tableRecords:
            return None
        else:
            return self.tableRecords[tag]


# End of class OffsetTable


