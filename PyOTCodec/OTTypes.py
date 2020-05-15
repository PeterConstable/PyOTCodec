import re



class Tag(str):
    
    # Use __new__, not __init__, so we can modify the value being constructed
    def __new__(cls, tagContent):
        """ Accept bytes, bytearray or string."""

        if isinstance(tagContent, bytes) or isinstance(tagContent, bytearray):
            # take 4 bytes; if less than 4 pad with 0x00
            tmp = tagContent + bytearray([0,0,0,0])
            tmp = tmp[:4]
        elif isinstance(tagContent, str):
            # take 4 characters; if less than 4 pad with spaces
            tmp = tagContent + 4 * "\u0020"
            tmp = tmp[:4]
            # verify only 0x00 to 0xFF by trying to encode as Latin-1
            # this will raise a UnicodeError if any out of range characters
            enc = tmp.encode("Latin-1")
        else:
            raise OTCodecError("Tag can only be constructed from str, bytearray or bytes")

        return super().__new__(cls, cls._decodeIfBytes(tmp))

    @staticmethod
    def _decodeIfBytes(content):
        if isinstance(content, bytearray) or isinstance(content, bytes):
            content = content.decode("Latin-1")
        return content

    def toBytes(self):
        return self.encode("Latin-1")


    # Override __eq__, __ne__ to facilitate correct comparison of str with bytes
    def __ne__(self, other):
        """Compare to tag bytearray, bytes or string"""
        return not self.__eq__(other)

    def __eq__(self, other):
        """Compare to tag bytearray, bytes or string"""
        tmp = self._decodeIfBytes(other)
        return str.__eq__(self, self._decodeIfBytes(other))

    # Implementation of __hash__ is needed so that a Tag can be used as a dict key
    def __hash__(self):
        return str.__hash__(self)

    @staticmethod
    def validateTag(tag):
        """Check if a tag string is a valid OpenType tag. Returns an error code.

        OpenType tags must be 4 characters long. They can only include 
        ASCII 0x20 to 0x7E, and spaces can only be trailing. The sfnt
        version tag 0x0100 is the one exception to these rules, and
        b'\x00\x01\x00\x00' will be accepted. 

        The method returns an error code with flags:
            0x00: valid tag string
            0x01: wrong length
            0x02: out of range characters
            0x04: non-trailing spaces
        """

        if tag == None:
            raise OTCodecError("Invalid argument: None")

        # Recognize exceptional sfntVersion tag:
        if tag == b'\x00\x01\x00\x00':
            return 0

        errors = 0

        # Test against normal rules

        if len(tag) != 4:
            errors += 0x01
        for c in tag:
            if ord(c) < 0x20 or ord(c) > 0x7E:
                errors += 0x02

        # check for non-trailing spaces: remove all spaces and compare with rstrip
        if re.sub(" ", "", tag) != tag.rstrip():
            errors += 0x04
        
        return errors

# End of class Tag



class OTCodecError(Exception): pass
