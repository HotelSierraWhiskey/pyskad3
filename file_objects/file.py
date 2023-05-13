import itertools


PLAIN_COMMS = 0x00
PERMISSIVE_ACCESS = 0xEE


class BaseDataFile:
    '''
    An anemic container for blueprinting a File.
    Derived classes are valid arguments for `list()`
    '''

    def __init__(self, fileno,
                 comms_setting_byte,
                 access_rights,
                 file_size):

        self.fileno = fileno
        self.comms_setting_byte = comms_setting_byte
        self.access_rights = access_rights
        self.file_size = file_size

    def __iter__(self):
        return iter(itertools.chain(*[i for i in self.__dict__.values()]))


class PermissiveStandardDataFile(BaseDataFile):
    '''
    A preset for a permissive standard data file
    `file_size` = `[0x10, 0x00, 0x00]` (16 bytes) by default
    '''

    def __init__(self, fileno: list, file_size: list = [0x10, 0x00, 0x00]) -> None:
        self.fileno = fileno
        self.comms_setting_byte = [PLAIN_COMMS]
        self.access_rights = [PERMISSIVE_ACCESS,
                              PERMISSIVE_ACCESS]
        self.file_size = file_size
        super().__init__(
            self.fileno,
            self.comms_setting_byte,
            self.access_rights,
            self.file_size)


class PermissiveValueFile(BaseDataFile):
    def __init__(self,
                 fileno,
                 comms_setting_byte=[PLAIN_COMMS],
                 access_rights=[PERMISSIVE_ACCESS,
                                PERMISSIVE_ACCESS],
                 lower_limit=[0x00, 0x00, 0x00, 0x00],
                 upper_limit=[0x00, 0x00, 0x00, 0x7F],
                 #  upper_limit=[0x00, 0x00, 0x01, 0x00],
                 initial_value=[0x00] * 4,
                 limited_credit_available=[0x00]):

        self.fileno = fileno
        self.comms_setting_byte = comms_setting_byte
        self.access_rights = access_rights
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.initial_value = initial_value
        self.limited_credit_available = limited_credit_available

        super().__init__(
            self.fileno,
            self.comms_setting_byte,
            self.access_rights,
            [0x04, 0x00, 0x00])  # Value shouldn't matter, but added to prevent errors


class PermissiveCyclicRecordFile(BaseDataFile):
    def __init__(self,
                 fileno,
                 comms_setting_byte=[PLAIN_COMMS],
                 access_rights=[PERMISSIVE_ACCESS,
                                PERMISSIVE_ACCESS],
                 record_size=[0x10, 0x00, 0x00],
                 number_of_records=[0x03, 0x00, 0x00]):

        self.fileno = fileno
        self.comms_setting_byte = comms_setting_byte
        self.access_rights = access_rights
        self.record_size = record_size
        self.number_of_records = number_of_records

        super().__init__(
            self.fileno,
            self.comms_setting_byte,
            self.access_rights,
            [0x04, 0x00, 0x00])  # Value shouldn't matter, but added to prevent errors
