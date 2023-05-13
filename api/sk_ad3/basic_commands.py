from ..constants.command_codes import *
from ..constants.status_codes import _get_status
from ..utils.utils import bcc
from ..response.response import Response


#   NOTE: commands in this file are constructed according to the convention:
#
#           [STX, ADDR, LENH, LENL] + [CMT, CM, PM, (DATA), ETX] + [BCC]


def init(self, position: str = 'capture') -> Response:
    '''
    Initializes the dispenser. This must be done upon power-up
    to enable the use of other commands. `position` defaults to `'capture'`.
    Acceptable values for position are::

    'front', 'capture', 'no_move', 'front_with_counter', 'capture_with_counter', 'no_move_with_counter'

    If successful, response.data is::

    {'position': position}
    '''
    positions = {
        'front':                0x30,
        'capture':              0x31,
        'no_move':              0x33,
        'front_with_counter':   0x34,
        'capture_with_counter': 0x35,
        'no_move_with_counter': 0x37,
    }
    if position not in positions.keys():
        raise Exception(f'position must be one of {list(positions.keys())}')

    parameter = positions[position]

    buffer = [STX, self.addr, 0x00, 0x03]
    buffer += [CMT, COMMAND_INIT, parameter, ETX]
    buffer += [bcc(buffer)]

    with self.serial_context:
        raw_response = self.send_command(buffer)
        response = Response(raw_response)
        response.data['position'] = position
        return response


def move_card(self, position: str) -> Response:
    '''
    Moves a card to a given position. Acceptable values for position are::

    'front', 'IC', 'RF', 'capture', 'gate'

    If successful, response.data is::

    {'position': position}
    '''
    positions = {
        'front':    0x30,
        'IC':       0x31,
        'RF':       0x32,
        'capture':  0x33,
        'gate':     0x39,
    }
    if position not in positions.keys():
        raise Exception(f'position must be one of {list(positions.keys())}')

    parameter = positions[position]

    buffer = [STX, self.addr, 0x00, 0x03]
    buffer += [CMT, COMMAND_MOVE_CARD, parameter, ETX]
    buffer += [bcc(buffer)]

    with self.serial_context:
        raw_response = self.send_command(buffer)
        response = Response(raw_response)
        response.data['position'] = position
        return response


def get_status(self) -> Response:
    '''
    A dedicated status monitoring methed.
    Acquires the status of the device without having to issue a non-status-related command.

    If successful, response.data::

    {'status': dict}
    '''
    buffer = [STX, self.addr, 0x00, 0x03]
    buffer += [CMT, COMMAND_STATUS_SENSE, PARAM_PROVIDE_STATUS_INFO, ETX]
    buffer += [bcc(buffer)]

    with self.serial_context:
        raw_response = self.send_command(buffer)
        response = Response(raw_response)
        response.data['status'] = _get_status(raw_response)
        return response


def set_insertion(self, setting: bool) -> Response:
    '''
    Enables/ disables card insertion functionality on the SK AD3.
    `True` for `setting` enables insertion, `False` denies insertion.

    If successful, response.data::

    {'allow_insertion': setting}
    '''
    parameter = None
    if setting:
        parameter = PARAM_ALLOW_INSERTION
    else:
        parameter = PARAM_DENY_INSERTION

    assert (parameter is not None)

    buffer = [STX, self.addr, 0x00, 0x03]
    buffer += [CMT, COMMAND_SET_INSERTION, parameter, ETX]
    buffer += [bcc(buffer)]

    with self.serial_context:
        raw_response = self.send_command(buffer)
        response = Response(raw_response)
        response.data['allow_insertion'] = setting
        return response
