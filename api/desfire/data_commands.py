from ..response.response import APDU_Response
from ..utils.utils import hexify
from .apdu_utils.data_commands import *


def read_data(self, fileno: list,
              offset: list = [0x00, 0x00, 0x00],
              length: list = [0x10, 0x00, 0x00]) -> APDU_Response:
    '''
    Reads `length` bytes of data in a file starting at `offset`. 
    `offset` is set to `[0x00, 0x00, 0x00]` (no offset) by default.
    `length` is set to `[0x00, 0x00, 0x00]` (16 bytes) by default.

    If successful, response.data is::

    {'file': {'fileno' int, 'file_data': list}}
    '''
    with self.serial_context:
        apdu = command_read_data(fileno, offset, length)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['file'] = {'fileno': fileno,
                                     'file_data': None}
            return response

        file_data = hexify(response.raw_response[10: -4])
        response.data['file'] = {'fileno': fileno,
                                 'file_data': file_data}
        return response


def write_data(self, fileno: list,
               data: list,
               offset: list = [0x00, 0x00, 0x00],
               length: list = [0x10, 0x00, 0x00]) -> APDU_Response:
    '''
    Writes data to a the file specified by `fileno` in the application currently selected.
    Offset is `[0x00, 0x00, 0x00]` (no offset) by default. 
    Length is `[0x10, 0x00, 0x00]` (16 bytes) by default.

    If successful, response.data is::

    {'file': {'fileno': int, 'written': True}}
    '''
    with self.serial_context:
        apdu = command_write_data(fileno, offset, length, data)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['file'] = {'fileno': fileno, 'written': False}
            return response
        response.data['file'] = {'fileno': fileno, 'written': True}
        return response


def write_record(self, fileno: list,
                 data: list,
                 offset: list = [0x00, 0x00, 0x00],
                 length: list = [0x10, 0x00, 0x00]) -> APDU_Response:
    '''
    Writes a record to a the record file specified by `fileno` in the application currently selected.
    Offset is `[0x00, 0x00, 0x00]` (no offset) by default. 
    Length is `[0x10, 0x00, 0x00]` (16 bytes) by default.

    If successful, response.data is::

    {'file': {'fileno': int, 'record_written': True}}
    '''
    with self.serial_context:
        apdu = command_write_record(fileno, offset, length, data)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['file'] = {'fileno': fileno, 'record_written': False}
            return response
        response.data['file'] = {'fileno': fileno, 'record_written': True}
        return response


def read_record(self, fileno: list, record_number: list, number_of_records: list) -> APDU_Response:
    with self.serial_context:
        apdu = command_read_record(fileno, record_number, number_of_records)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['record_data'] = None
            return response
        response.data['record_data'] = raw_response[10:-12]
        return response


def credit_value_file(self, fileno: list, amount: list) -> APDU_Response:
    amount = list(amount[0].to_bytes(4, byteorder='big'))
    with self.serial_context:
        apdu = command_credit(fileno, amount)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['credit'] = False
            return response

        response.data['credit'] = True
        return response


def debit_value_file(self, fileno: list, amount: list) -> APDU_Response:
    amount = list(amount[0].to_bytes(4, byteorder='big'))
    with self.serial_context:
        apdu = command_debit(fileno, amount)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['debit'] = False
            return response

        response.data['debit'] = True
        return response


def get_value_in_value_file(self, fileno: list) -> APDU_Response:
    with self.serial_context:
        apdu = command_get_value(fileno)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['value'] = False
            return response

        #   Converting from list of hex strings to single integer value
        temp = ''.join([i.replace('0x', '')
                       for i in hexify(raw_response[10:-4])])
        value = int(temp, 16)

        response.data['value'] = value
        return response


def commit_transaction(self) -> APDU_Response:
    with self.serial_context:
        apdu = command_commit_transaction()
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['commit'] = False
            return response
        response.data['commit'] = True
        return response
