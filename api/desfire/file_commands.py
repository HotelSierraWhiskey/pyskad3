from ...file_objects.file import BaseDataFile
from ..response.response import APDU_Response
from ..utils.utils import hexify
from .apdu_utils.file_commands import *

#   NOTE: By default, methods that take arguments such as 'length' and 'offset' expect three bytes of data.
#   DESFire cards want the byte order in reverse.
#   Ex: you might expect that `0x10` -> `0x000010` -> `b'\\x00\\x00\\x10'` (in three bytes),
#   but the DESFire cards actually want that reversed, i.e. `b'\\x10\\x00\\x00'`.


def create_standard_data_file(self, file: BaseDataFile) -> APDU_Response:
    '''
    Creates a standard data file in the currently selected application.
    file must be an instance of `BaseDataFile`. 

    If successful, response.data is::

    {'file': {'fileno' int, 'created': True}}
    '''
    with self.serial_context:
        apdu = command_create_std_data_file(
            file.fileno, file.comms_setting_byte, file.access_rights, file.file_size)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['file'] = {'fileno': file.fileno,
                                     'created': False}
            return response
        response.data['file'] = {'fileno': file.fileno,
                                 'created': True}
        return response


def create_cyclic_record_file(self, file: BaseDataFile) -> APDU_Response:
    with self.serial_context:
        apdu = command_create_cyclic_record_file(
            file.fileno, file.comms_setting_byte, file.access_rights, file.record_size, file.number_of_records)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['file'] = {'fileno': file.fileno,
                                     'created': False}
            return response
        response.data['file'] = {'fileno': file.fileno,
                                 'created': True}
        return response


def get_file_settings(self, fileno: list) -> APDU_Response:
    with self.serial_context:
        apdu = command_get_file_settings(fileno)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['file_settings'] = None
            return response
        response.data['file_settings'] = raw_response
        return response


def create_value_file(self, file: BaseDataFile) -> APDU_Response:
    '''
    Creates a value file in the currently selected application.
    file must be an instance of `BaseDataFile`. 

    If successful, response.data is::

    {'file': {'fileno' int, 'created': True}}
    '''
    with self.serial_context:
        apdu = command_create_value_file(file.fileno, file.comms_setting_byte, file.access_rights,
                                         file.lower_limit, file.upper_limit, file.initial_value, file.limited_credit_available)

        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['file'] = {'fileno': file.fileno,
                                     'created': False}
            return response
        response.data['file'] = {'fileno': file.fileno,
                                 'created': True}
        return response


def delete_file(self, fileno: list) -> APDU_Response:
    '''
    Deletes the file with FID `fileno`.

    If successful, response.data is::

    {'file': {'fileno' int, 'deleted': True}}
    '''
    with self.serial_context:
        apdu = command_delete_file(fileno)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['file'] = {'fileno': fileno,
                                     'deleted': False}
            return response
        response.data['file'] = {'fileno': fileno,
                                 'deleted': True}
        return response


# More attention here
def get_file_ids(self) -> APDU_Response:
    '''
    Gets a list of file IDs in the selected application.
    Will return 91 F0 (Specified file number does not exist) if the application does not
    allow for the viewing of file ids without the proper authentication.
    '''
    with self.serial_context:
        apdu = command_get_file_ids()
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        if not response.is_successful():
            response.data['file'] = {'ids': None}
            return response
        response.data['file'] = {'ids': raw_response}
        return response
