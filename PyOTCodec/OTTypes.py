class Tag:
    def __init__(self, tagArray:bytearray = bytearray([0,0,0,0])):
        # Take first four bytes; pad with 0 if less than four bytes passed.
        tmp = tagArray + bytearray([0,0,0,0])
        tmp = tmp[:4]
        self.tagBytes = bytes(tmp)

    @classmethod
    def fromString(cls, tagString: str):
        # Take first four Latin-1 characters; pad with space
        # error if any characters > U+00FF
        tmp = tagString + 4 * "\u0020"
        tmp = tmp[:4]
        tagArray = tmp.encode("Latin-1")
        return cls(tagArray)
    
    def toString(self):
        return self.tagBytes.decode("Latin-1")
    
    def __str__(self):
        return self.toString()