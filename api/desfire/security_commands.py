from Crypto.Cipher import DES, AES
from .auth import Auth
from ..response.response import APDU_Response
from ..utils.utils import crc, flip
from .apdu_utils.security_commands import *
from .apdu_utils.application_commands import command_additional_frame


def aes_authenticate(self, key: list, key_id: list = [0x00]) -> APDU_Response:
    '''
    DESFire EV1 cards implement a three-pass external authentication protocol 
    whereby neither device exposes their encryption key. Depending on your application 
    you may need to perform an external authentication procedure with the
    DESFire card you're working on.
    The `key_id` is `0` by default.

    If successful, response.data is::

    {'authentication': True, 'session_key': list}
    '''
    with self.serial_context:

        key = bytearray(key)

        authenticator = Auth(key, 'AES')

        #   Request AES Challenge
        apdu = command_aes_auth(key_id)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)
        #   Verify that the authentication procedure has begun
        if not response.is_successful():
            response.data = {'authentication': False}
            return response

        #   Solve AES Challenge
        challenge = raw_response[10:-4]
        submission = authenticator._first_pass(challenge)

        #   Submit, and receive response
        apdu = command_additional_frame(submission)
        raw_response = self.send_raw_apdu(apdu)

        authenticator._second_pass(raw_response[10:-4])

        response = APDU_Response(raw_response)

        #   If we received anything other than success, return failure response
        if not response.is_successful():
            response.data = {'authentication': False}
            return response

        #   Else, return a successful response
        response.data = {'authentication': True,
                         'session_key': authenticator.session_key}

        return response


def des_authenticate(self, key: list, key_id: list = [0x00]) -> APDU_Response:
    '''
    DESFire EV1 cards implement a three-pass external authentication protocol 
    whereby neither device exposes their encryption key. Depending on your application 
    you may need to perform an external authentication procedure with the
    DESFire card you're working on.
    The `key_id` is `0` by default.

    If successful, response.data is::

    {'authentication': True, 'session_key': list}
    '''

    key = bytearray(key)

    authenticator = Auth(key, 'DES')

    with self.serial_context:
        apdu = command_des_auth(key_id)
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)

        #   Verify that the authentication procedure has begun
        if not response.is_successful():
            response.data = {'authentication': False}
            return response

        #   Solve DES Challenge
        challenge = raw_response[10:-4]
        submission = authenticator._first_pass(challenge)

        #   Submit, and receive response
        apdu = command_additional_frame(submission)
        raw_response = self.send_raw_apdu(apdu)

        authenticator._second_pass(raw_response[10:-4])

        response = APDU_Response(raw_response)

        if not response.is_successful():
            response.data = {'authentication': False}
            return response

        response.data = {'authentication': True,
                         'session_key': authenticator.session_key}

        return response


def _change_key(new_key: list, session_key: list, key_number: list, key_version: list):
    '''
    Internal use only.
    Encrypts the C4/ Change Key command data, builds and returns the encrypted APDU.

    NOTE: Currently this method cannot revert an AES authenticated card back into its factory DES state.
    '''
    engine = None
    padding = [0x00]

    #   From DES to AES
    if len(session_key) == 8:
        engine = DES
        padding *= 3
    #   From AES to AES
    if len(session_key) == 16:
        engine = AES
        padding *= 11

    assert engine

    command = [0xC4]

    formatted_crc = flip(crc(command + key_number + new_key + key_version))

    to_encipher = bytearray(new_key + key_version + formatted_crc + padding)

    cipher = engine.new(bytearray(session_key),
                        engine.MODE_CBC,
                        bytearray([0] * len(session_key)))

    ciphertext = list(cipher.encrypt(to_encipher))

    apdu = command_change_key(key_number, ciphertext)

    return apdu


def change_picc_master_key(self, new_key: list, session_key: list, key_version: list = [0x00]) -> APDU_Response:

    key_number = [0x80]

    apdu = _change_key(new_key, session_key, key_number, key_version)

    with self.serial_context:
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)

        if not response.is_successful():
            response.data['key_changed'] = False
            return response

        response.data['key_changed'] = True

        return response


def change_application_key(self, new_key: list, session_key: list, key_number: list = [0x00], key_version: list = [0x00]) -> APDU_Response:

    apdu = _change_key(new_key, session_key, key_number, key_version)

    with self.serial_context:
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)

        if not response.is_successful():
            response.data['key_changed'] = False
            return response

        response.data['key_changed'] = True

        return response


def get_key_version(self, key_id: list):
    '''
    Gets the key version for a given key.
    You should be able to obtain the key version without authentication.

    If successful, response.data is::

    {'key_version': str}
    '''
    apdu = command_get_key_version(key_id)

    with self.serial_context:
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)

        if not response.is_successful():
            response.data['key_version'] = None
            return response

        #   The key version is just one byte with a consistent location in the response
        response.data['key_version'] = raw_response[10]

        return response
