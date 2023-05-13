from ..constants.command_codes import *
from ..utils.utils import bcc
from ..response.response import Response


def auto_test_RF_card_type(self) -> Response:
    '''
    Performs an automatic test on the card currently in the RF position.

    If successful, response.data is::

    {'card_type': str}
    '''
    card_types = {
        ('0', '0'): "Unknown RF card type",
        ('1', '0'): "Mifare one S50 card",
        ('1', '1'): "Mifare one S70 card",
        ('1', '2'): "Mifare one UL card",
        ('2', '0'): "Type A CPU card",
        ('3', '0'): "Type B CPU card",
    }

    buffer = [STX, self.addr, 0x00, 0x03]
    buffer += [CMT, COMMAND_AUTO_TEST_CARD_TYPE, PARAM_TEST_RF_CARD, ETX]
    buffer += [bcc(buffer)]

    with self.serial_context:
        response = self.send_command(buffer)
        response = Response(response)

        key = tuple([chr(i) for i in response.raw_response[-4:-2]])
        response.data['card_type'] = card_types[key]

        return response


def activate_RF_card(self, card_type: str = 'type_a') -> Response:
    '''
    Activates the RF card currently in the 'RF' position. 
    `card_type` defaults to `'type_a'`. Given the application, it may be best to run 
    `auto_test_RF_card_type()` before activating a card as responses vary depending on the
    type of card being activated.

    Acceptable values for `card_type` are::

    'type_a', 'type_b'

    If successful, response.data is::

    {'card_active': True}
    '''
    buffer = [STX, self.addr, 0x00, 0x05]
    buffer += [CMT, COMMAND_RF_CARD_OPERATION, PARAM_ACTIVATE_RF_CARD]

    sets = []
    if card_type == 'type_a':
        sets = [0x41, 0x30]
    elif card_type == 'type_b':
        sets = [0x30, 0x41]
    else:
        raise Exception(f"Unexpected value for card_type: {card_type}.\
                        Must be either 'type_a' or 'type_b'")

    buffer += sets
    buffer += [ETX]
    buffer += [bcc(buffer)]

    with self.serial_context:
        response = self.send_command(buffer)
        response = Response(response)

        if not response.is_successful():
            response.data['card_active'] = None
            return response

        response.data['card_active'] = True
        return response


def deactivate_RF_card(self) -> Response:
    '''
    Closes all antenna output signals.

    If successful, response.data is::

    {'card_active': False}
    '''
    buffer = [STX, self.addr, 0x00, 0x03]
    buffer += [CMT, COMMAND_RF_CARD_OPERATION, PARAM_DEACTIVATE_RF_CARD, ETX]
    buffer += [bcc(buffer)]

    with self.serial_context:
        response = self.send_command(buffer)
        response = Response(response)

        if not response.is_successful():
            response.data['card_active'] = None
            return response

        response.data['card_active'] = False
        return response
