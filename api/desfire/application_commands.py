from ...file_objects.application import BaseDesfireApplication
from ..response.response import APDU_Response
from ..utils.utils import hexify
from .apdu_utils.application_commands import *


def get_card_uid(self) -> APDU_Response:
    '''
    Gets the UID of a card. You should always be able to obtain this information
    without authentication. the Get Version command-response procedure takes place
    over multiple frames because the response includes other information such as
    card manufacturing year, week, and hardware/software versions. Everything other than
    the card's uid gets stripped away in this method. The UID of the card should be
    seven bytes encoded in exactly 14 characters. 

    If successful, response.data is::

    {'uid': str}
    '''
    with self.serial_context:

        #   Get the card version info
        apdu = command_get_version()
        response = self.send_raw_apdu(apdu)
        response = APDU_Response(response)

        if not response.is_successful():
            return response

        #   Get the next frame
        apdu = command_additional_frame()
        response = self.send_raw_apdu(apdu)
        response = APDU_Response(response)

        if not response.is_successful():
            return response

        #   And the next frame
        apdu = command_additional_frame()
        response = self.send_raw_apdu(apdu)

        #   Strip away non-uid-related information
        uid = response[10:17]
        uid = ''.join([i.replace('0x', '').upper() for i in hexify(uid)])

        #   Return successful response
        response = APDU_Response(response)
        response.data = {'uid': uid}

        return response


def create_application(self, app: BaseDesfireApplication) -> APDU_Response:
    '''
    Creates a new application. Depending on settings this may be possible without authenticating
    as the card master key. `app` must be an instance of a `BaseDesfireApplication`. 

    NOTE:   In the future this method should be able to ignore `BaseDesfireApplication`s altogether
            and create applications from raw lists.

    If successful, response.data is::

    {'application_created':{'status': True, 'aid': str}}
    '''
    with self.serial_context:
        apdu = command_create_application(
            app.aid, app.key_settings, app.app_settings)
        response = self.send_raw_apdu(apdu)
        response = APDU_Response(response)

        if not response.is_successful():
            response.data['application_created'] = {
                'status': False, 'aid': app.aid}
            return response
        response.data['application_created'] = {
            'status': True, 'aid': app.aid
        }
        return response


def select_application(self, aid: list):
    '''
    Selects an application based on the AID provided. Depending on settings this may be possible without authenticating
    as the card master key.

    If successful, response.data is::

    {'selected': aid, 'status' True}
    '''
    with self.serial_context:
        apdu = command_select_application(aid)
        response = self.send_raw_apdu(apdu)
        response = APDU_Response(response)
        if not response.is_successful():
            response.data['selected'] = {'aid': aid, 'status': False}
            return response
        response.data['selected'] = {'aid': aid, 'status': True}
        return response


def delete_application(self, aid: list) -> APDU_Response:
    '''
    Deletes an application based on the AID provided. Depending on settings this may be possible without authenticating
    as the card master key.

    If successful, response.data is::

    {'deleted': aid, 'status' True}
    '''
    with self.serial_context:
        apdu = command_delete_application(aid)
        response = self.send_raw_apdu(apdu)
        response = APDU_Response(response)
        if not response.is_successful():
            response.data['deleted'] = {'aid': aid, 'status': False}
            return response
        response.data['deleted'] = {'aid': aid, 'status': True}
        return response


def get_application_ids(self) -> APDU_Response:
    '''
    Gets a list of application ids. Depending on settings this may be possible without authenticating
    as the card master key.

    If successful, response.data is::

    {'ids': list}

    NOTE: ^^ list of lists\n
    or, if no applications exist::

    {'ids': None}
    '''
    with self.serial_context:
        apdu = command_get_application_ids()
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)

        if not response.is_successful():
            response.data['ids'] = None
            return response

        ids = raw_response[10:-4]

        #   If no applications exist on the card
        if not ids:
            #   provide None as opposed to an empty list
            response.data['ids'] = None

        #   ids is a list of application ids. Each application id is a list of exactly 3 ints
        ids = [ids[x:x+3] for x in range(0, len(ids), 3)]

        #   If currently authenticated, the card will return ids along with an 8-byte
        #   CMAC added to the response. If the length of the last chunk of ids is 2,
        #   then the last chunk is actually the last two bytes of the CMAC. In this case
        #   we just simply strip off the last 8 bytes from ids, and provide what remains.
        if ids:
            if len(ids[-1]) == 2:
                ids = ids[:-3]

        response.data['ids'] = ids

        return response


def format_picc(self):
    '''
    Reformats the card. This always requires authentication.

    If successful, response.data is::

    {'reformat': True}
    '''
    with self.serial_context:
        apdu = command_format_picc()
        raw_response = self.send_raw_apdu(apdu)
        response = APDU_Response(raw_response)

        if not response.is_successful():
            response.data['reformat'] = False
            return response

        response.data['reformat'] = True
        return response
