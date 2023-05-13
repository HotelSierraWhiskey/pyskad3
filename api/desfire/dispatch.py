from ..constants.command_codes import *
from ..utils.utils import bcc


def send_raw_apdu(self, apdu: list) -> list:
    '''
    This is a generic method for wrapping APDUs in complete Command Packages 
    and dispatching them to the SK-AD3 machine. `apdu` must be a list.
    '''
    # Since CMT, 0x60, and 0x34 are part of the TEXT field of the command package,
    # The length in bytes of the TEXT field = the length of the APDU + 3
    len_text = len(apdu) + 3
    lenh = len_text >> 8
    lenl = len_text & 0x00FF

    buffer = [STX, self.addr, lenh, lenl, CMT, 0x60, 0x34]
    buffer += apdu
    buffer += [ETX]
    buffer += [bcc(buffer)]

    self._write(buffer)
    raw_response = self._read()

    return raw_response
