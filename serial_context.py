import serial
from serial import EIGHTBITS, STOPBITS_ONE, PARITY_NONE


class SerialContext(serial.Serial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bytesize = EIGHTBITS
        self.stopbits = STOPBITS_ONE
        self.parity = PARITY_NONE

    def __enter__(self, *args, **kwargs):
        self.open()

    def __exit__(self, *args, **kwargs):
        self.close()
