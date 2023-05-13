from ..desfire.apdu_utils.response_codes import apdu_response_codes
from ..constants.command_codes import *
from ..constants.status_codes import _get_status
from ..constants.error_codes import _get_error


class Response:
    '''
    The object returned from top-level API calls to the dispenser.
    Provides basic methods for determining the success of a basic command,
    reading the current status of the dispenser (see constants/status_codes.py),
    and obtaining error codes (see constants/error_codes.py). This class
    and its derived APDU_Response simplify the process of reading inbound Command Packages,
    they provide no actual error handling.
    '''

    def __init__(self, raw_response: list):
        self.raw_response = raw_response
        self.data = {}

    def status(self):
        return _get_status(self.raw_response)

    def error(self):
        return _get_error(self.raw_response)

    def is_successful(self):
        if self.raw_response[4] == PMT:
            return True
        return False


class APDU_Response(Response):
    '''
    APDU responses are encapsulated within a Command Package.
    Thus, APDU_Response inhereits the base Response class. As a result,
    users can read the state of the SK AD3 device during exchanges with
    RFID cards.
    '''

    def __init__(self, raw_response: list, *args, **kwargs) -> None:
        super().__init__(self, *args, **kwargs)
        self.raw_response = raw_response
        self.code = self.raw_response[-4:-2]
        # self.data = None

    def apdu_response_code(self) -> str:
        key = tuple(self.code)
        try:
            return apdu_response_codes[key]
        except KeyError as e:
            raise Exception(f"Undocumented response: {self.code}")

    #   Overrides Response.is_successful. In addition to checking for PMT
    #   this method also checks the APDU response code to determine success.
    def is_successful(self) -> bool:
        if self.raw_response[4] == PMT:
            key = tuple(self.code)
            if key not in [(0x91, 0x00), (0x90, 0x00), (0x91, 0xAF)]:
                return False
            return True
