from ctr.util.data_stream import DataStream

from ctr.lib.lms.msbp.colors.clb1 import CLB1
from ctr.lib.lms.msbp.colors.clr1 import CLR1

from ctr.lib.lms.msbp.attributes.ati2 import ATI2
from ctr.lib.lms.msbp.attributes.alb1 import ALB1
from ctr.lib.lms.msbp.attributes.ali2 import ALI2


class Msbp:
    "A class to repersent a Message Studio Binary Project file"

    def __init__(self, filepath: str = None):
        self.filepath = filepath

    def parse(self) -> None:
        with open(self.filepath, "rb") as d:
            # Parsing the header
            data = DataStream(d)

            # Magic
            self.magic = data.read_string(8)

            if self.magic != "MsgPrjBn":
                raise ValueError(
                    f'Input file specified has an invalid signature! (Expected "MsgPrjBn", got "{str(self.magic)})'
                )

            # BOM
            self.byteOrderMark = "little" if data.read_bytes(
                2) == b"\xFF\xFE" else "big"

            # Skip some zeros
            data.read_bytes(2)

            # Possible mesasge encoding types
            encodings = {0: "UTF-8", 1: "UTF-16", 2: "UTF-32"}

            # Get the message encoding
            self.messageEncoding = encodings[data.read_int8()]

            if self.messageEncoding != "UTF-8":
                raise ValueError(
                    f"Message Encoding is invalid, expected UTF-8, got {self.messageEncoding}")

            # Version
            self.version = data.read_uint8()

            if self.version != 3:
                raise ValueError(
                    f"Version number is unsupported! Expected 3, got {self.version}")

            self.numberOfChunks = data.read_uint16()

            # Skip zeros
            data.read_bytes(2)

            # Filesize
            self.fileSize = data.read_uint32()

            # Skip to the start of the MSBP data
            data.read_bytes(10)

            for _ in range(4):
                magic = data.read_string(4)
                match magic:
                    case "CLR1":
                        self.clr1 = CLR1(data)
                        data = self.clr1.read()
                    case "CLB1":
                        self.clb1 = CLB1(data)
                        data = self.clb1.read()
                    case "ATI2":
                        self.ati2 = ATI2(data)
                        data = self.ati2.read()
                    case "ALB1":
                        self.alb1 = ALB1(data)
                        data = self.alb1.read()
                    case "ALI2":
                        self.ali2 = ALI2(data)
                        data = self.ali2.read()
                    case "TGG2":
                        pass
                    case "TAG2":
                        pass
                    case "TGL2":
                        pass
                    case "SLB1":
                        pass
                    case "SYL3":
                        pass
