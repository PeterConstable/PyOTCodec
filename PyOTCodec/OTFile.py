import struct
from pathlib import Path
from io import BytesIO
from OTTypes import *
from OTFont import *



class OTFile(object):
    def __init__(self, fileName: str =None):
        self.path: Path = None
        self.fileName = fileName #file pathname
        self.fileBytes: bytearray = None
        self.sfntVersion: Tag = Tag()
        self.ttcHeader = None
        self.numFonts = 0
        self.fonts = []

        # check for valid file path
        if not fileName: # catches None, empty string
            raise OTCodecError("Error: no file specified")
        self.path = Path(fileName) # Accepts empty string but not null
        if not self.path.is_file(): # catches items that don't exist
            raise OTCodecError("Error:", fileName, "is not a file")

        with open(fileName, "rb") as f:
            self.fileBytes = bytearray(f.read())
        self.sfntVersion = Tag(self.fileBytes[:4])

        if not OTFile.IsSupportedSfntVersion(self.sfntVersion):
            raise OTCodecError("File is not a supported sfntVersion")

        if self.sfntVersion.toString() == "ttcf":
            #create ttc header from file
            self.ttcHeader = TTCHeader(self.fileBytes)
            self.numFonts = self.ttcHeader.numFonts
        else:
            self.numFonts = 1

        # Now know how many font resources; intialize font objects -- OTFont constructor will get the offset table
        if self.sfntVersion.toString() == "ttcf":
            #loop over ttcHeader.numFonts
            offsets = self.ttcHeader.offsetTableOffsets
            for i in range(self.numFonts):
                self.fonts.append(OTFont(self, offsets[i], i))
        else:
            self.fonts.append(OTFont(self))

    # end of __init__


    def IsCollection(self):
        return self.sfntVersion.toString() == "ttcf"

    @staticmethod
    def IsSupportedSfntVersion(tag:Tag):
        if tag.toString() not in ('\x00\x01\x00\x00', "OTTO", "ttcf", "true"):
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
        self.offsetTableOffsets = []

        # get the version 1 header fields
        headerBytes = fileBytes[: TTCHeader._ttcHeaderVersion1HeaderSize]
        tmp = struct.unpack(TTCHeader._ttcHeaderVersion1HeaderFormat, headerBytes)
        self.ttcTag = Tag(tmp[0])
        self.majorVersion, self.minorVersion, self.numFonts = tmp[1:4]

        # confirm the version is recognized before continuing
        if self.majorVersion != 1 and self.majorVersion != 2:
            raise OTCodecError("TTCHeader version is not supported")

        # get the offsetTables offsets array -- we'll wrap BytesIO around fileBytes to provide sequential reading
        filebio = BytesIO(fileBytes)
        filebio.seek(TTCHeader.offsetInFile + OffsetTable._offsetTableHeaderSize)
        for i in range(self.numFonts):
            # unpack returns a tuple with one element; the comma after named var 
            # offset is syntax quirk needed to get that element, not the tuple
            offset, = struct.unpack(">L", filebio.read(4))
            self.offsetTableOffsets.append(offset)

        # if version 2, get additional fields
        v2fieldBytes = filebio.read(TTCHeader._ttcHeaderVersion2FieldsSize)
        tmp = struct.unpack(TTCHeader._ttcHeaderVersion2FieldsFormat, v2fieldBytes)
        self.dsigTag = Tag(tmp[0])
        self.dsigLength, self.dsigOffset = tmp[1:3]

# End of class TTCHeader



class OTCodecError(Exception): pass
