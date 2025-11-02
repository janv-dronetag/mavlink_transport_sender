from .base_transport import BaseTransport, hex_dump

class Slip:
    """
    SLIP (Serial Line Internet Protocol) encoder/decoder.
    This class handles the framing of data packets.
    """
    END = 0x0A
    ESC = 0xDB
    ESC_END = 0xDC
    ESC_ESC = 0xDD

    END_b = b"\x0a"
    ESC_b = b"\xdb"
    ESC_END_b = b"\xdc"
    ESC_ESC_b = b"\xdd"

    @staticmethod
    def encode(data: bytes) -> bytes:
        """Encodes raw bytes into a SLIP frame."""
        return (
            data
            .replace(Slip.ESC_b, Slip.ESC_b + Slip.ESC_ESC_b)
            .replace(Slip.END_b, Slip.ESC_b + Slip.ESC_END_b)
            + Slip.END_b
        )
class SlipTransport(BaseTransport):
    """Implements sending of MAVLink bytes framed with SLIP over serial."""
    def __init__(self, port: str, mux_address: int, baudrate: int = 115200, timeout: float = 0):
        super().__init__(port, baudrate, timeout)
        self.mux_address = mux_address

    def write_packet(self, raw_mavlink_packet: bytes, message_name: str = "MAVLink Message"):
        if not self.dev or not self.dev.is_open:
            raise IOError("Serial device is not open.")
        
        slip_encoded_packet = Slip.encode(raw_mavlink_packet)
        final_packet = bytes([self.mux_address]) + slip_encoded_packet
        
        hex_dump(message_name, final_packet)
        self.dev.write(final_packet)
        self.dev.flush()