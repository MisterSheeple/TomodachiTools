from enum import IntEnum

from ctr.util.data_stream import DataStream
from ctr.util.serialize import JsonSerialize

"""
Texture Coordinate Generation Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x01  |   uint8  | Type (0 = 2x4 Matrix)
 0x01  |  0x01  |   uint8  | Source (0 = Tex0, 1 = Tex1, 2 = Tex2, 3 = Ortho, 4 = PaneBased, 5 = PerspectiveProj)
 0x02  |  0x02  |   bytes  | Padding (?)
===================
"""

# Generation Type Enum
class TexGenType(IntEnum):
    MATRIX_2x4 = 0

# Generation Source Enum
class TexGenSource(IntEnum):
    TEX0 = 0
    TEX1 = 1
    TEX2 = 2
    ORTHO = 3
    PANE_BASED = 4
    PERSPECTIVE_PROJ = 5


class TexCoordGen:

    genType: TexGenType = None
    genSource: TexGenSource = None
    padding: tuple[int, int] = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        """Reads the TexMap section from a material data stream"""

        # Read in the type and source as bytes
        self.genType = TexGenType(data.read_uint8())
        self.genSource = TexGenSource(data.read_uint8())
        self.padding = data.read_bytes(2)

        return data
    
    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("genType", self.genType, True)
        j.add("genSource", self.genSource, True)
        return j.serialize()