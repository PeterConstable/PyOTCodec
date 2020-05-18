import struct
from io import BytesIO
from ot_types import *
#inline below: 
#  import ot_table
#  from ot_font import OTFont, TableRecord
#  from ot_file import calcCheckSum


class Table_fmtx:

    _expectedTag = "fmtx"

    _fmtx_version = ">4s"
    _fmtx_version_size = struct.calcsize(_fmtx_version)

    _fmtx_2_0_format = ">4sL" + 8 * "B"
    """ Structure:
        (big endian)                 >
        version               fixed  4s
        glyphIndex            uint32 L
        horizontalBefore      uint8  B
        horizontalAfter       uint8  B
        horizontalCaretHead   uint8  B
        horizontalCaretBase   uint8  B
        verticalBefore        uint8  B
        verticalAfter         uint8  B
        verticalCaretHead     uint8  B
        verticalCaretBase     uint8  B
    """

    _fmtx_2_0_size  = struct.calcsize(_fmtx_2_0_format)

    _fmtx_2_0_fields = (
        "version",
        "glyphIndex",
        "horizontalBefore",
        "horizontalAfter",
        "horizontalCaretHead",
        "horizontalCaretBase",
        "verticalBefore",
        "verticalAfter",
        "verticalCaretHead",
        "verticalCaretBase"
         )

    _fmtx_2_0_defaults = (
        b'\x00\x02\x00\x00', #  version
        #0x0002_0000, #  version
        #2.0, #  version
        0, #  glyphIndex
        0, #  horizontalBefore
        0, #  horizontalAfter
        0, #  horizontalCaretHead
        0, #  horizontalCaretBase
        0, #  verticalBefore
        0, #  verticalAfter
        0, #  verticalCaretHead
        0, #  verticalCaretBase
        )


    def __init__(self):
        self.tableTag = Tag(self._expectedTag)


    @staticmethod
    def createNew_fmtx():
        """Creates a new version 2.0 fmtx table with default values."""

        fmtx = Table_fmtx()

        fmtx.version = Fixed(fmtx._fmtx_2_0_defaults[0])
        #fmtx.version = Fixed.createNewFixedFromUint32(fmtx._fmtx_2_0_defaults[0])
        #fmtx.version = Fixed.createNewFixedFromFloat(fmtx._fmtx_2_0_defaults[0])
        for k, v in zip(fmtx._fmtx_2_0_fields[1:], fmtx._fmtx_2_0_defaults[1:]):
            setattr(fmtx, k, v)

        return fmtx
    # End of createNew_fmtx


    @staticmethod
    def tryReadFromFile(parentFont, tableRecord):
        """Returns a Table_fmtx constructed from data in fileBytes. 
        
        Exceptions may be raised if tableRecord.tableTag doesn't match,
        or if tableRecord.offset or .length do not fit within the file.
        """

        fmtx = Table_fmtx()

        from ot_font import OTFont, TableRecord
        if not (isinstance(parentFont, OTFont) and isinstance(tableRecord, TableRecord)):
            raise Exception()

        import ot_table
        ot_table.ValidateTableTag(tableRecord, fmtx._expectedTag)

        fmtx.parentFont = parentFont
        fmtx.tableRecord = tableRecord

        # get file bytes, then validate offset/length are in file bounds
        fileBytes = parentFont.fileBytes
        offsetInFile = tableRecord.offset
        ot_table.ValidateOffsetAndLength(
            len(fileBytes), offsetInFile, tableRecord.length
            )

        # get the table bytes: since offset length are in bounds, can get the expected length
        tableBytes = fileBytes[offsetInFile : offsetInFile + tableRecord.length]

        # check the version
        if len(tableBytes) < fmtx._fmtx_version_size:
            raise OTCodecError("The table lenght is wrong: can't even read the version.")
        vals = struct.unpack(fmtx._fmtx_version, tableBytes[:fmtx._fmtx_version_size])
        fmtx.version = Fixed(vals[0])
        if fmtx.version.mantissa != 2:
            raise OTCodecError(f"Unsupported fmtx version: {fmtx.version.fixedTableVersion}")

        if fmtx.version.mantissa == 2 and tableRecord.length < fmtx._fmtx_2_0_size:
            raise OTCodecError(f"Can't read the version {fmtx.version.fixedTableVersion} fmtx table: the table is too short.")
            
        # unpack
        vals = struct.unpack(fmtx._fmtx_2_0_format, tableBytes)
        for k, v in zip(fmtx._fmtx_2_0_fields[1:], vals[1:]):
            setattr(fmtx, k, v)

        # calculate checksum (should match what's in TableRecord)
        from ot_file import calcCheckSum
        fmtx.calculatedCheckSum = calcCheckSum(tableBytes)

        return fmtx
    # End of tryReadFromFile

# End of class Table_fmtx
