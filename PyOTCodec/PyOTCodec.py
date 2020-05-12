from OTFile import *
from OTTypes import *
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
