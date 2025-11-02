import serial
from abc import ABC, abstractmethod

def hex_dump(prefix: str, data: bytes):
    """
    Prints a hexadecimal representation of bytes for debugging.
    """
    hex_str = data.hex()
    pairs = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
    print(f"{prefix}\nlen={len(data)} bytes: {' '.join(pairs)}\n")

class BaseTransport(ABC):
    """
    Abstract Base Class for MAVLink transport layers.
    Defines the interface for sending MAVLink packets over a physical link.
    """
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.dev: serial.Serial | None = None

    def open(self):
        """Opens the serial device with pyserial."""
        self.dev = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=self.timeout,
            write_timeout=0  # non-blocking writes
        )
        print(f"Opened serial device: {self.port} @ {self.baudrate} baud")

    def close(self):
        """Closes the serial device."""
        if self.dev and self.dev.is_open:
            self.dev.close()
            print(f"Closed serial device: {self.port}")
            self.dev = None

    @abstractmethod
    def write_packet(self, raw_mavlink_packet: bytes, message_name: str = "MAVLink Message"):
        """
        Abstract method to write a MAVLink packet.
        Concrete implementations will handle specific framing (e.g., SLIP).
        """
        pass
