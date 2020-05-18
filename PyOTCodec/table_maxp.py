import struct
from io import BytesIO
from ot_types import *
#inline below: 
#  import ot_table
#  from ot_font import OTFont, TableRecord
#  from ot_file import calcCheckSum



class Table_maxp:

    _expectedTag = "maxp"

    _maxp_version = ">4s"
    _maxp_version_size = struct.calcsize(_maxp_version)

    # v0.5 fields
    _maxp_0_5_format = ">4sH"
    _maxp_0_5_size = struct.calcsize(_maxp_0_5_format)

    # additional fields in v1.0
    _maxp_1_0_addl_format = ">" + 13 * "H"
    """ Structure:
        (big endian)                    >
        maxPoints: uint16               H
        maxContours: uint16             H
        maxCompositePoints: uint16      H
        maxCompositeContours: uint16    H
        maxZones: uint16                H
        maxTwilightPoints: uint16       H
        maxStorage: uint16              H
        maxFunctionDefs: uint16         H
        maxInstructionDefs: uint16      H
        maxStackElements: uint16        H
        maxSizeOfInstructions: uint16   H
        maxComponentElements: uint16    H
        maxComponentDepth: uint16       H
    """
    _maxp_1_0_addl_size = struct.calcsize(_maxp_1_0_addl_format)

    _maxp_0_5_fields = ("version", "numGlyphs")

    _maxp_1_0_addl_fields = (
        "maxPoints",
        "maxContours",
        "maxCompositePoints",
        "maxCompositeContours",
        "maxZones",
        "maxTwilightPoints",
        "maxStorage",
        "maxFunctionDefs",
        "maxInstructionDefs",
        "maxStackElements",
        "maxSizeOfInstructions",
        "maxComponentElements",
        "maxComponentDepth"
        )

    _maxp_1_0_all_fields = _maxp_0_5_fields + _maxp_1_0_addl_fields

    _maxp_1_0_addl_defaults = (
        0, # maxPoints
        0, # maxContours
        0, # maxCompositePoints
        0, # maxCompositeContours
        0, # maxZones
        0, # maxTwilightPoints
        0, # maxStorage
        0, # maxFunctionDefs
        0, # maxInstructionDefs
        0, # maxStackElements
        0, # maxSizeOfInstructions
        0, # maxComponentElements
        0  # maxComponentDepth
        )


    def __init__(self):
        self.tableTag = Tag(self._expectedTag)


    @staticmethod
    def createNew_maxp(version:float):
        """Creates a new version 0.5 or version 1.0 maxp table with default values."""

        if float(version) != 0.5 and float(version) != 1.0:
            raise OTCodecError(f"Version {version} of the maxp table is not supported.")

        maxp = Table_maxp()
        
        if version == 0.5:
            maxp.version = Fixed.createNewFixedFromUint32(0x0000_5000)
            maxp.numGlyphs = 0
        else:
            maxp.version = Fixed.createNewFixedFromUint32(0x0001_0000)
            maxp.numGlyphs = 0
            for k, v in zip(maxp._maxp_1_0_addl_fields, maxp._maxp_1_0_addl_defaults):
                setattr(maxp, k, v)

        return maxp
    # End of createNew_maxp


    @staticmethod
    def tryReadFromFile(parentFont, tableRecord):
        """Returns a Table_maxp constructed from data in fileBytes. 
        
        Exceptions may be raised if tableRecord.tableTag doesn't match,
        or if tableRecord.offset or .length do not fit within the file."""

        maxp = Table_maxp()

        from ot_font import OTFont, TableRecord
        if not (isinstance(parentFont, OTFont) and isinstance(tableRecord, TableRecord)):
            raise Exception()

        import ot_table
        ot_table.ValidateTableTag(tableRecord, maxp._expectedTag)

        maxp.parentFont = parentFont
        maxp.tableRecord = tableRecord

        # get file bytes, then validate offset/length are in file bounds
        fileBytes = parentFont.fileBytes
        offsetInFile = tableRecord.offset
        ot_table.ValidateOffsetAndLength(
            len(fileBytes), offsetInFile, tableRecord.length
            )

        # get the table bytes: since offset length are in bounds, can get the expected length
        tableBytes = fileBytes[offsetInFile : offsetInFile + tableRecord.length]

        # check the version
        if len(tableBytes) < maxp._maxp_version_size:
            raise OTCodecError("The table lenght is wrong: can't even read the version.")
        vals = struct.unpack(maxp._maxp_version, tableBytes[:maxp._maxp_version_size])
        maxp.version = Fixed(vals[0])
        if maxp.version.fixedTableVersion != 0.5 and maxp.version.mantissa != 1:
            raise OTCodecError(f"Unsupported maxp version: {maxp.version}")

        if maxp.version.fixedTableVersion == 0.5 and tableRecord.length < maxp._maxp_0_5_size:
            raise OTCodecError("Can't read the verion 0.5 maxp table: the table length is too short.")
        elif maxp.version.mantissa == 1 and tableRecord.length < maxp._maxp_0_5_size + maxp._maxp_1_0_addl_size:
            raise OTCodecError(f"Can't read the verion {maxp.version.fixedTableVersion} maxp table: the table length is too short.")

        # unpack v0.5 fields
        vals = struct.unpack(maxp._maxp_0_5_format, tableBytes[:maxp._maxp_0_5_size])
        maxp.numGlyphs = vals[1]

        if maxp.version.mantissa == 1:
            # unpack additional v1.0 fields
            vals = struct.unpack(maxp._maxp_1_0_addl_format, tableBytes[maxp._maxp_0_5_size:])
            for k, v in zip(maxp._maxp_1_0_addl_fields, vals):
                setattr(maxp, k, v)

        # calculate checksum (should match what's in TableRecord)
        from ot_file import calcCheckSum
        maxp.calculatedCheckSum = calcCheckSum(tableBytes)

        return maxp
    # End of tryReadFromFile

# End of class Table_maxp
