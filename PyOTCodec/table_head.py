import struct
from io import BytesIO
from ot_types import *
#inline below: 
#  import ot_table
#  from ot_font import OTFont, TableRecord
#  from ot_file import calcCheckSum


class Table_head:

    _expectedTag = "head"

    # head v1.0 format

    _head_version = ">2H"
    _head_version_size = struct.calcsize(_head_version)

    _head_1_0_format = ">2H4s2L2H2q" + "4h" + "2H" + "3h"
    """ Structure:
        (big endian)                      >
        majorVersion        uint16        H
        minorVersion        uint16        H
        fontRevision        Fixed         4s
        checkSumAdjustment  uint32        L
        magicNumber         uint32        L
        flags               uint16        H
        unitsPerEm          uint16        H
        created             LONGDATETIME  q
        modified            LONGDATETIME  q
        xMin                int16         h
        yMin                int16         h
        xMax                int16         h
        yMax                int16         h
        macStyle            uint16        H
        lowestRecPPEM       uint16        H
        fontDirectionHint   int16         h
        indexToLocFormat    int16         h
        glyphDataFormat     int16         h
    """
    _head_1_0_size = struct.calcsize(_head_1_0_format)

    _head_1_x_checkSumAdjustment_offset = struct.calcsize(">2H4s")

    _head_1_0_fields = (
        "majorVersion",
        "minorVersion",
        "fontRevision",
        "checkSumAdjustment",
        "magicNumber",
        "flags",
        "unitsPerEm",
        "created",
        "modified",
        "xMin",
        "yMin",
        "xMax",
        "yMax",
        "macStyle",
        "lowestRecPPEM",
        "fontDirectionHint",
        "indexToLocFormat",
        "glyphDataFormat"
        )

    _head_1_0_defaults = (
        1, # majorVersion
        0, # minorVersion
        b'\x00\x00\x00\x00', # fontRevision
        0, # checkSumAdjustment
        0x5F0F3CF5, # magicNumber
        0, # flags
        2048, # unitsPerEm
        0, # created
        0, # modified
        0, # xMin
        0, # yMin
        0, # xMax
        0, # yMax
        0, # macStyle
        0, # lowestRecPPEM
        0, # fontDirectionHint
        0, # indexToLocFormat
        0  # glyphDataFormat
        )

    def __init__(self):
        self.tableTag = Tag(self._expectedTag)


    @staticmethod
    def createNew_head():
        """Creates a new version 1.0 hhea table with default values."""

        head = Table_head()
        for k, v in zip(head._head_1_0_fields, head._head_1_0_defaults):
            if k != "fontRevision":
                setattr(head, k, v)
        head.fontRevision = Fixed(head._head_1_0_defaults[2])

        return head


    @staticmethod
    def tryReadFromFile(parentFont, tableRecord):
        """Returns a Table_head constructed from data in fileBytes. 
        
        Exceptions may be raised if tableRecord.tableTag doesn't match,
        or if tableRecord.offset or .length do not fit within the file.
        """

        head = Table_head()

        from ot_font import OTFont, TableRecord
        if not (isinstance(parentFont, OTFont) and isinstance(tableRecord, TableRecord)):
            raise Exception()

        import ot_table
        ot_table.ValidateTableTag(tableRecord, head._expectedTag)

        head.parentFont = parentFont
        head.tableRecord = tableRecord

        # get file bytes, then validate offset/length are in file bounds
        fileBytes = parentFont.fileBytes
        offsetInFile = tableRecord.offset
        ot_table.ValidateOffsetAndLength(
            len(fileBytes), offsetInFile, tableRecord.length
            )

        # get the table bytes: since offset length are in bounds, can get the expected length
        tableBytes = fileBytes[offsetInFile : offsetInFile + tableRecord.length]

        # check the version
        if len(tableBytes) < head._head_version_size:
            raise OTCodecError("The table lenght is wrong: can't even read the version.")
        vals = struct.unpack(head._head_version, tableBytes[:head._head_version_size])
        head.majorVersion, head.minorVersion = vals
        if head.majorVersion != 1:
            raise OTCodecError(f"Unsupported table version: {hhea.majorVersion}.{hhea.minorVersion}")
        if len(tableBytes) < head._head_1_0_size:
            raise OTCodecError(f"Can't read the version {hhea.majorVersion}.{hhea.minorVersion} hhea table: the table is too short.")

        # unpack
        vals = struct.unpack(head._head_1_0_format, tableBytes)
        head.fontRevision = Fixed(vals[2])
        for k, v in zip(head._head_1_0_fields[3:], vals[3:]):
            setattr(head, k, v)

        # calculate checksum
        # Note: a special calculation is required for the head table. We need
        # to make sure to include pad bytes from the file.
        padded_length = (tableRecord.length + 3) - (tableRecord.length + 3) % 4
        tableBytes = fileBytes[offsetInFile : offsetInFile + padded_length]
        head.calculatedCheckSum = head._calcHeadCheckSum(tableBytes)

        # Calculating the checkSumAdjustment for the font is somewhat costly,
        # so don't do it up front; leave it until it's needed.
        # head.calculatedCheckSumAdjustment = head._calcCheckSumAdjustment(parentFont)

        return head
    # End of tryReadFromFile


    @staticmethod
    def _calcHeadCheckSum(headBytes:bytes):
        """Calculates a checksum for the head table based on the provided data.

        Can be called for a head table read from a file or a new head table
        created in memory. A version 1.x table is assumed. The length of the
        data should be a multiple of four. If not, the checksum will be
        calculated after padding with null bytes. If the data is read from a
        file, you should include padding bytes from the file.
        """

        assert isinstance(headBytes, (bytearray, bytes, memoryview))
        assert len(headBytes) >= Table_head._head_1_0_size

        """
        The 'head' table requires special handling for calculating a checksum. The
        process also involves the head.checksumAdjustment field.
            
        From OT spec (v1.8.3) font file regarding TableRecord.checkSum for 'head':
            To calculate the checkSum for the 'head' table which itself includes the 
            checkSumAdjustment entry for the entire font, do the following:
                1. Set the checkSumAdjustment to 0.
                2. Calculate the checksum for all the tables including the 'head' table
                    and enter that value into the table directory.
        
        NOTE: This wording is unclear and can be misleading. The TableRecord.checkSum
        for 'head' is calculated using the modified 'head' data only, not the rest of
        the file.
            
        From OT spec 'head' table regarding checkSumAdjustment:
            To compute it: set it to 0, sum the entire font as uint32, 
            then store 0xB1B0AFBA - sum.
            
            If the font is used as a component in a font collection file, the value
            of this field will be invalidated by changes to the file structure and
            font table directory, and must be ignored. 
            
        If in a TTC, ignore all that and just set both calculated values to 0.
        """

        headCopy = bytearray(headBytes)
        headCopy[Table_head._head_1_x_checkSumAdjustment_offset
                 : Table_head._head_1_x_checkSumAdjustment_offset + 4] = [0,0,0,0]

        from ot_file import calcCheckSum
        return calcCheckSum(headCopy)
    # End _calcHeadCheckSum


    def calcCheckSumAdjustment(self):
        """Calculates the checkSumAdjustment for the font containing the head
        table. If the font is within a TTC, returns 0.

        The checkSumAdjustment value is returned. No font data is changed.
        
        The head table must have a parentFont attribute set to an OTFont
        object, and that OT font must have the fileBytes attribute set to a
        byte sequence containing the font data. This should only be called for 
        font data read from a file or for a complete font created in memory.
        """

        from ot_font import OTFont, TableRecord
        assert hasattr(self, "parentFont")
        font = self.parentFont
        assert isinstance(font, OTFont)
        assert hasattr(font, "fileBytes")

        # If within TTC, just return 0
        if font.isWithinTtc:
            return 0

        # get the head TableRecord
        head_rec = font.offsetTable.tryGetTableRecord("head")
        if head_rec is None:
            return None

        # To calculate checkSumAdjustment, the font file must be modified by
        # setting head.checkSumAdjustment to 0. A checksum is calculated for
        # the entire font file with that modification. After computing the 
        # file checksum, the differnce from 0xB1B0AFBA is taken.
        # https://docs.microsoft.com/en-us/typography/opentype/spec/otff#calculating-checksums
        #
        # To avoid copying the entire font data to make a small change, the 
        # file checksum can be computed sequentially on three segments:
        #
        #   1) data before the modified head table (not copied)
        #   2) continue with a modified copy of the head table
        #   3) continue with the remainder (not copied)
        #
        # A memoryview will be used to avoid copying.

        fontBytesView = memoryview(font.fileBytes)


        # All tables offsets (from start of file) are expected to be multiples 
        # of 4, though that might not be true in some fonts. Checksums must be
        # calculated on 4-byte increments. Determine if we need to work around
        # any such quirk.

        phase = 4 - (head_rec.offset % 4) if (head_rec.offset % 4) != 0 \
                else (head_rec.offset % 4)
        # phase is the number of extra bytes from the start of the head table
        # to include in the first segment

        from ot_file import calcCheckSum

        # get checksum for the first segment
        first_segment_length = head_rec.offset + phase
        assert first_segment_length % 4 == 0
        first_segment = fontBytesView[:first_segment_length]
        checksum = calcCheckSum(first_segment)

        # For the second segment, use 12 bytes after the end of the first
        # segment, which will include the head.checkSumAdjustment member.
        # Get a copy and clear the checkSumAdjustment.

        second_segment = bytearray(fontBytesView[first_segment_length : first_segment_length + 12])
        csa_offset = Table_head._head_1_x_checkSumAdjustment_offset - phase
        second_segment[csa_offset : csa_offset + 4] = [0,0,0,0]

        # continue the checksum with the modified second segment
        checksum = calcCheckSum(second_segment, leftPrior= checksum)

        # finish the checksum with the third segment
        third_segment = fontBytesView[first_segment_length + 12:]
        checksum = calcCheckSum(third_segment, leftPrior= checksum)

        return 0xB1B0AFBA - checksum
    # End of _calcCheckSumAdjustment


# End of class Table_head
