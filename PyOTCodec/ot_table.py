import struct
from io import BytesIO
from ot_types import *
from ot_file import *
from ot_font import *


class OTTable:
    def __init__(self):
        pass




def ValidateTableTag(tableRecord:TableRecord, expectedTag:Tag):
    if tableRecord.tableTag != expectedTag:
        raise OTCodecError("The tableRecord.tableTag value doesn't match the Table_{expectedTag} class.")

def ValidateOffsetAndLength(fileLength, offsetInFile, length, expectedLength = 0, tag = ""):
    if offsetInFile >= fileLength:
        raise OTCodecError("The offset value is beyond the end of the file.")
    if offsetInFile + length > fileLength:
        raise OTCodecError("The offset and length values extend beyond the end of the file.")

    if expectedLength > 0 and length != expectedLength:
        raise OTCodecError(f"The length is the wrong length for any supported version of the {tag} table.")
