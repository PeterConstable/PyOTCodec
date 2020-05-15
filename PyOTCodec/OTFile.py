import struct
from pathlib import Path
from io import BytesIO
from OTTypes import *
from OTFont import *



class OTFile(object):

    def __init__(self, fileName:str = None):
        self.path: Path = None
        self.fileBytes: bytearray = None
        self.sfntVersion: Tag = None
        self.ttcHeader = None
        self.numFonts = 0
        self.fonts = []

        # check for valid file path
        if not fileName: # catches None, empty string
            raise OTCodecError("Error: no file specified")
        self.path = Path(fileName) # Accepts empty string but not null
        if not self.path.is_file(): # catches items that don't exist
            raise OTCodecError("Error:", fileName, "is not a file")

        with open(fileName, "rb") as f: # file will be closed after with
            self.fileBytes = bytearray(f.read())

        # get sfntVersion
        rawbytes = self.fileBytes[:4]
        if len(rawbytes) < 4:
            raise OTCodecError("Unable to read sfntVersion")
        self.sfntVersion = Tag(rawbytes)
        if not OTFile.isSupportedSfntVersion(self.sfntVersion):
            raise OTCodecError("File is not a supported sfntVersion")

        if self.sfntVersion == "ttcf":
            #create TTCHeader from file
            self.ttcHeader = TTCHeader(self.fileBytes)
            self.numFonts = self.ttcHeader.numFonts
        else:
            self.numFonts = 1

        # Now know how many font resources; intialize font objects -- OTFont constructor will get the offset table
        if self.sfntVersion == "ttcf":
            #loop over ttcHeader.numFonts
            offsets = self.ttcHeader.offsetTableOffsets
            for i in range(self.numFonts):
                self.fonts.append(OTFont(self, offsets[i], i))
        else:
            self.fonts.append(OTFont(self))

    # end of __init__


    def isCollection(self):
        return self.sfntVersion == "ttcf"

    @staticmethod
    def isSupportedSfntVersion(tag:Tag):
        if tag not in (b'\x00\x01\x00\x00', "OTTO", "ttcf", "true"):
            return False
        else:
            return True


# end of Class OTFile



class TTCHeader:
    offsetInFile = 0

    # version 1 header for TTCHeader -- fields prior to offsetTable offsets array
    _ttcHeaderVersion1HeaderFormat = ">4sHHL"
    """ Structure:
        (big-endian)            >
        sfntVersion: Tag        4s
        majorVersion: uint16    H
        minorVersion: uint16    H
        numFonts: uint32        L
    """
    _ttcHeaderVersion1HeaderSize = struct.calcsize(_ttcHeaderVersion1HeaderFormat)

    _ttcHeaderVersion2FieldsFormat = ">4sLL"
    """ Structure:
        (big-endian)            >
        dsigTag: Tag            4s
        dsigLength: uint32      L
        dsigOffset: uint32      L
    """
    _ttcHeaderVersion2FieldsSize = struct.calcsize(_ttcHeaderVersion2FieldsFormat)


    def __init__(self, fileBytes:bytearray):
        self.ttcTag: Tag = None
        self.majorVersion, self.minorVersion, self.numFonts = 0, 0, 0
        self.offsetTableOffsets = []
        # v2 only: self.dsigTag, self.dsigLength, self.dsigOffset

        # get the version 1 header fields
        headerBytes = fileBytes[: TTCHeader._ttcHeaderVersion1HeaderSize]
        if len(headerBytes) < TTCHeader._ttcHeaderVersion1HeaderSize:
            raise OTCodecError("Unable to read TTC header from file")
        tmp = struct.unpack(TTCHeader._ttcHeaderVersion1HeaderFormat, headerBytes)
        self.ttcTag = Tag(tmp[0])
        self.majorVersion, self.minorVersion, self.numFonts = tmp[1:4]

        # confirm the version is recognized before continuing
        if self.majorVersion != 1 and self.majorVersion != 2:
            raise OTCodecError("TTCHeader version is not supported")

        # get the offsetTables offsets array -- wrapping BytesIO around fileBytes 
        # to provide sequential reading
        filebio = BytesIO(fileBytes)
        filebio.seek(TTCHeader.offsetInFile + OffsetTable._offsetTableHeaderSize)
        for i in range(self.numFonts):
            # unpack returns a tuple with one element; the comma after named var 
            # offset is syntax quirk needed to get that element, not the tuple
            offset = ReadUint32(filebio)
            self.offsetTableOffsets.append(offset)

        # if version 2, get additional fields
        if self.majorVersion == 2:
            v2fieldBytes = filebio.read(TTCHeader._ttcHeaderVersion2FieldsSize)
            if len(v2fieldBytes) < TTCHeader._ttcHeaderVersion2FieldsSize:
                raise OTCodecError("Unable to read version 2 TTC header from file")
            tmp = struct.unpack(TTCHeader._ttcHeaderVersion2FieldsFormat, v2fieldBytes)
            self.dsigTag = Tag(tmp[0])
            self.dsigLength, self.dsigOffset = tmp[1:3]

# End of class TTCHeader


def ReadRawBytes(fileBytesIO:BytesIO, length):
        rawbytes = fileBytesIO.read(length)
        if len(rawbytes) < length:
            raise OTCodecError("Unable to read expected number of bytes from file")
        return rawbytes

def ReadInt8(fileBytesIO:BytesIO):
    """ Reads an unsigned long (uint32) from the current position. """
    format = ">b"
    rawbytes = ReadRawBytes(fileBytesIO, struct.calcsize(format))
    val, = struct.unpack(format, rawbytes)
    return val

def ReadUint8(fileBytesIO:BytesIO):
    """ Reads an unsigned long (uint32) from the current position. """
    format = ">B"
    rawbytes = ReadRawBytes(fileBytesIO, struct.calcsize(format))
    val, = struct.unpack(format, rawbytes)
    return val

def ReadInt16(fileBytesIO:BytesIO):
    """ Reads an unsigned long (uint32) from the current position. """
    format = ">h"
    rawbytes = ReadRawBytes(fileBytesIO, struct.calcsize(format))
    val, = struct.unpack(format, rawbytes)
    return val

def ReadUint16(fileBytesIO:BytesIO):
    """ Reads an unsigned long (uint32) from the current position. """
    format = ">H"
    rawbytes = ReadRawBytes(fileBytesIO, struct.calcsize(format))
    val, = struct.unpack(format, rawbytes)
    return val

def ReadInt32(fileBytesIO:BytesIO):
    """ Reads an unsigned long (uint32) from the current position. """
    format = ">l"
    rawbytes = ReadRawBytes(fileBytesIO, struct.calcsize(format))
    val, = struct.unpack(format, rawbytes)
    return val

def ReadUint32(fileBytesIO:BytesIO):
    """ Reads an unsigned long (uint32) from the current position. """
    format = ">L"
    rawbytes = ReadRawBytes(fileBytesIO, struct.calcsize(format))
    val, = struct.unpack(format, rawbytes)
    return val

def ReadInt64(fileBytesIO:BytesIO):
    """ Reads an unsigned long (uint32) from the current position. """
    format = ">q"
    rawbytes = ReadRawBytes(fileBytesIO, struct.calcsize(format))
    val, = struct.unpack(format, rawbytes)
    return val

def ReadUint64(fileBytesIO:BytesIO):
    """ Reads an unsigned long (uint32) from the current position. """
    format = ">Q"
    rawbytes = ReadRawBytes(fileBytesIO, struct.calcsize(format))
    val, = struct.unpack(format, rawbytes)
    return val

