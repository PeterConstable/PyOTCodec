# PyOTCodec

Python library for parsing font files

This was started as a project for learning Python: I was already quite familiar with the binary layout of font files and the OpenType spec and had earlier personal projects writing parsing code in Visual Basic and in C#. It was a meaty project sure to provide opportunity to learn many aspects of Python (though certainly not many others).

My thought was eventually to be able to parse or write data, but initially the focus is almost entirely on parsing.

Parts of the OpenType spec that have been implemented include:

* sfnt / TTC headers and table directory
  * The class hierarchy has OTFile as the root, with optional TTCHeader; and one or more OTFont objects as children of OTFile, each with a TableDirectory.
* head, hhea, maxp, fmtx tables
  * These are simple/flat tables so easy to start with.
* COLR table
  * This is the first table with internal hierarchy to be supported, chosen because of current interest in possible extensions for gradients.
  * Version 0 is supported, as well as a preliminary draft for a version 1 with gradient support.
* While adding support for COLR v1, generic functions were created and patterns established to support hierarchical structure elsewhere in the spec:
  * A generic function to read arrays of records comprised only basic data types supported directly by the `struct` module.
  * A generic function to read arrays of records comprised with complex structs as members.
  * A generic function to read subtables of a single type referenced via offsets within a parent table.
  * A generic function to read subtables with different formats (with `format` as the first field in the subtable).
