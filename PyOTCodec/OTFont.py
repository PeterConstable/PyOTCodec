import struct
from pathlib import Path
from io import BytesIO
from OTTypes import *
from OTFile import *

class OTFont:
    # represents a font resource: one font within a TTC, or the font of the entire file of not a TTC

    def __init__(self, otFile, offsetInFile: int = 0, ttcIndex: int = None):
        self.otFile = otFile
        self.offsetInFile = offsetInFile
        self.ttcIndex = ttcIndex
        self.isInTtc = False if ttcIndex is None else True
        self.offsetTable = OffsetTable(otFile.fileBytes, offsetInFile)
        self.tables: list = []
        self.defaultLabel = otFile.path.name if ttcIndex is None else otFile.path.name + ":" + str(ttcIndex)


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
        self.tableRecords: list = []

        # get the header
        headerBytes = fileBytes[offsetInFile : offsetInFile + OffsetTable._offsetTableHeaderSize]
        if len(headerBytes) < OffsetTable._offsetTableHeaderSize:
            raise OTCodecError("Unable to read OffsetTable from file at 0x{0:0=8x}".format(offsetInFile))
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
            self.tableRecords.append(record)

# End of class OffsetTable


