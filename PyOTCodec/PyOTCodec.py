from OTTypes import *
from OTFile import *
from OTFont import *










#-------------------------------------------------------------
# END -- anything that follows is temporary stuff for testing
#-------------------------------------------------------------


x = OTFile(r"TestData\selawk.ttf")
print(x.sfntVersion)
print("file exists?", x.path.exists())
print("name:", x.path.name, x.path.is_file())
print("x.numFonts:", x.numFonts)
print("number of tables:", len(x.fonts[0].offsetTable.tableRecords))
print(x.fonts[0].defaultLabel)
print(x.fonts[0].ttcIndex)
x = OTFile(r"TestData\CAMBRIA.TTC")
print("x.numFonts:", x.numFonts)
print(x.fonts[0].defaultLabel)
print(x.fonts[0].ttcIndex)

print("tag 'abcd' validation", Tag.validateTagString("abcd"))
print("tag 'abc ' validation", Tag.validateTagString("abc "))
print("tag 'abc' validation", Tag.validateTagString("abc"))
print("tag 'ab c' validation", Tag.validateTagString("ab c"))
print("tag 'ab€c' validation", Tag.validateTagString("ab€c"))
print("tag b'\x00\x01\x00\x00' validation", Tag.validateTagString(b'\x00\x01\x00\x00'))
x = Tag("abc")



