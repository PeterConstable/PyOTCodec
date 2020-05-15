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
#        self.offsetTable = OffsetTable(otFile.fileBytes, offsetInFile)
        self.offsetTable = OffsetTable.tryReadFromFile(otFile.fileBytes, offsetInFile)
        self.tables: dict = {}
        self.defaultLabel = otFile.path.name if ttcIndex is None \
                            else otFile.path.name + ":" + str(ttcIndex)

    def sfntVersionTag(self):
        return self.offsetTable.sfntVersion

    def containsTable(self, tag:Tag):
        return (tag in self.offsetTable.tableRecords)

    def tryGetTableOffset(self, tag:Tag):
        """If the specified table is present in the font, gets the offset from the start of the font. 
        
        If the specified table is not present, returns None.
        """
        tableRecord = self.offsetTable.tryGetTableRecord(tag)
        if tableRecord is None:
            return None
        else:
            return tableRecord.offset

    @staticmethod
    def isSupportedSfntVersion(tag:Tag):
        if tag not in (b'\x00\x01\x00\x00', "OTTO", "true"):
            return False
        else:
            return True

    @staticmethod
    def isKnownTableType(tag:Tag):
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
    def isSupportedTableType(tag:Tag):
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


    def __init__(self):
        """Initialize an empty TableRecord to allow for creating new instances from
        scratch. To read from a file, TryReadFromBuffer is used."""
        self.tableTag = None
        self.checkSum, self.offset, self.length = 0, 0, 0

    @staticmethod
    def createNewTableRecord(tableTag:Tag, checkSum = 0, offset = 0, length = 0):
        """Returns a new TableRecord using specified values.
        
        A tag is required. The checkSum, offset and length values are optional:
        these are only meaningful when a complete table has been created, and can
        be set later.
        """
        tr = TableRecord()
        tr.tableTag, tr.checkSum, tr.offset, tr.length = tableTag, checkSum, offset, length
        return tr

    @staticmethod
    def tryReadFromBuffer(buffer:bytearray):
        """Returns a TableRecord constructed from values in the buffer. Returns None 
        if the buffer is the wrong length."""

        if len(buffer) != TableRecord.size:
            return None
        tr = TableRecord()
        tmp = struct.unpack(TableRecord._tableRecordFormat, buffer)
        tr.tableTag = Tag(tmp[0])
        tr.checkSum, tr.offset, tr.length = tmp[1:4]
        return tr


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


    def __init__(self):
        self.sfntVersion: Tag = None
        self.numTables, self.searchRange, self.entrySelector, self.rangeShift = 0, 0, 0, 0
        self.tableRecords: dict = {}


    @staticmethod
    def createNewOffsetTable(sfntVersion:Tag, searchRange = 0, entrySelector = 0, rangeShift = 0):
        """Returns a new OffsetTable using the specified values.

        An sfntVersion tag is required. The searchRange, entrySelector and
        rangeShift arguments are optional: these are only meaningful when a
        complete font has been assembled, and can be set later.

        TableRecords can be added later using AddTableRecord."""
        ot = OffsetTable()
        ot.sfntVersion, ot.searchRange, ot.entrySelector, ot.rangeShift \
            = sfntVersion, searchRange, entrySelector, rangeShift
        return ot
    # End of createNewOffsetTable


    @staticmethod
    def tryReadFromFile(fileBytes:bytearray, offsetInFile: int):
        """Returns an OffsetTable constructed from data in fileBytes. 
        
        Exceptions may be raised if fileBytes is not long enough."""

        ot = OffsetTable()
        ot.offsetInFile = offsetInFile

        # get the header
        headerBytes = fileBytes[offsetInFile : offsetInFile + OffsetTable._offsetTableHeaderSize]
        if len(headerBytes) < OffsetTable._offsetTableHeaderSize:
            raise OTCodecError("Unable to read OffsetTable from file at {:#08x}".format(offsetInFile))
        tmp = struct.unpack(OffsetTable._offsetTableHeaderFormat, headerBytes)
        ot.sfntVersion = Tag(tmp[0])
        ot.numTables, ot.searchRange, ot.entrySelector, ot.rangeShift = tmp[1:5]

        # get the table records -- we'll wrap BytesIO around fileBytes to provide sequential reading
        filebio = BytesIO(fileBytes)
        filebio.seek(offsetInFile + OffsetTable._offsetTableHeaderSize)
        for i in range(ot.numTables):
            recData = filebio.read(TableRecord.size)
            if len(recData) < TableRecord.size:
                raise OTCodecError("Unable to read TableRecord from file")
            record = TableRecord.tryReadFromBuffer(recData)
            ot.tableRecords[record.tableTag] = record

        return ot
    # End of TryReadFromFile


    def tryGetTableRecord(self, tag:Tag):
        """Returns the table record matching the specified tag, if present. If not present, returns None."""
        if not tag in self.tableRecords:
            return None
        else:
            return self.tableRecords[tag]

    def addTableRecord(self, tableRecord:TableRecord):
        """Adds a TableRecord to the OffsetTable.

        The tableRecord.tableTag member must not be None.
        
        This can only be used with an OffsetTable instance created anew
        in memory. If called on an instance that was read from a file,
        an exception is raised.
        """
        if tableRecord is None:
            raise OTCodecError("The tableRecord argument must not be None.")
        if hasattr(self, "offsetInFile"):
            raise OTCodecError("Cannot add a TableRecord to an OffsetTable that was read from a file.")
        if tableRecord.tableTag is None:
            raise OTCodecError("Cannot add a TableRecord that doesn't have a tableTag.")
        self.tableRecords[tableRecord.tableTag] = tableRecord

# End of class OffsetTable


