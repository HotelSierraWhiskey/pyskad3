from .serial_context import SerialContext


class SK_AD3:
    '''
    The SK_AD3 class owns all of the methods located in api/desfire and api/sk_ad3. 
    They are imported and bound to this namespace at instatiation time, and therefore
    must be accessed through an instance of this class. This mechanism allows for a 
    (relatively) clean logical separation between the two APIs.
    '''

    #   Top-level SK_AD3 methods
    from .api.sk_ad3.dispatch import send_command
    from .api.sk_ad3.basic_commands import \
        init, \
        get_status, \
        move_card, \
        set_insertion
    from .api.sk_ad3.card_commands import \
        auto_test_RF_card_type, \
        activate_RF_card, \
        deactivate_RF_card

    #   Top-level Desfire API methods
    from .api.desfire.dispatch import send_raw_apdu
    from .api.desfire.security_commands import \
        aes_authenticate, \
        des_authenticate, \
        change_picc_master_key, \
        change_application_key, \
        get_key_version
    from .api.desfire.application_commands import \
        get_card_uid, \
        get_application_ids, \
        select_application, \
        create_application, \
        delete_application, \
        format_picc
    from .api.desfire.file_commands import \
        get_file_ids, \
        create_standard_data_file, \
        create_cyclic_record_file, \
        create_value_file, \
        delete_file, \
        get_file_settings
    from .api.desfire.data_commands import \
        read_data, \
        write_data, \
        write_record, \
        read_record, \
        credit_value_file, \
        debit_value_file, \
        get_value_in_value_file, \
        commit_transaction

    def __init__(self, port: str, addr: int = 0x00):
        self.addr = addr
        self.port = port
        self.serial_context = SerialContext(
            port=self.port, baudrate=9600)
        self.serial_context.close()

    def _read(self) -> list:
        '''
        Internal use only.
        Reads data from the serial port.
        '''
        while self.serial_context.in_waiting:
            pass

        temp = self.serial_context.read(5)
        response = list(temp)
        try:
            #   NOTE:
            #   99% of the time (for some unknown reason) the device
            #   adds a 0x06 to the beginning of a response frame.
            #   During a read error, The 0x06 is missed, triggering an
            #   exception on remove().
            response.remove(6)
            length = (response[2] << 8) + response[3]
            response += list(self.serial_context.read(length + 2))
        except Exception:
            print('Read Error Occurred')
        finally:
            return response

    def _write(self, data: list) -> None:
        '''
        Internal use only.
        Writes data to the serial port. Must be provided with a valid SK-AD3 frame in the form of a list.
        '''
        self.serial_context.write(bytearray(data))
        while self.serial_context.out_waiting:
            pass
