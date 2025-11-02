from .base_transport import BaseTransport, hex_dump

class RawTransport(BaseTransport):
    """Implements sending of MAVLink bytes directly over serial."""
    def write_packet(self, raw_mavlink_packet: bytes, message_name: str = "MAVLink Message"):
        if not self.dev or not self.dev.is_open:
            raise IOError("Serial device is not open.")
        
        hex_dump(message_name, raw_mavlink_packet)
        self.dev.write(raw_mavlink_packet)
        self.dev.flush()