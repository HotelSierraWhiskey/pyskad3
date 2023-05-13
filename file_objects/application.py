from dataclasses import dataclass, field
import itertools


# NOTE: Refer to the table on page 7 of RevK's manual to get a (somewhat) clearer picture of what
#       all these values mean and how they're meant to be used in an actual APDU.

# Constants for KEY SETTINGS byte
#
# Card master key can be changed
ALLOW_CHANGE_MASTER_KEY = 0x01

# List applications is possible without master key, otherwise card master key is needed.
ALLOW_LIST_APPLICATIONS = 0x02

# Create applications is permitted without the master key. Delete needs card
# master key or app master key. If not set then both need card master key.
ALLOW_CREATE_APPLICATIONS = 0x04

# This setting can be changed. If unset, then that freezes this config.
ALLOW_CHANGE_CONFIG = 0x08

# Constants for APPLICATION settings byte
#
USE_DES = 0x00
USE_3K3DES = 0x20
USE_AES = 0x80


@dataclass
class BaseDesfireApplication:
    '''
    An anemic container for blueprinting a DESFire application.
    Derived application classes are valid arguments for `list()`
    '''

    aid: list = field(default_factory=list)
    key_settings: list = field(default_factory=list)
    app_settings: list = field(default_factory=list)

    def __iter__(self):
        return iter(itertools.chain(*[i for i in self.__dict__.values()]))

    # Since all applications are the same
    # we can provide an updating function in base class.
    def from_list(self, data: list) -> None:
        self.aid = [data[:3]]
        self.key_settings = [data[3]]
        self.app_settings = [data[4]]


class PermissiveDesfireApplication(BaseDesfireApplication):
    '''
    A preset for a permissive application that uses AES auth and a single key.
    '''

    def __init__(self, aid: list) -> None:
        super().__init__(self)
        self.aid = aid
        number_of_keys = 0x01
        self.key_settings = [
            ALLOW_CHANGE_MASTER_KEY |
            ALLOW_LIST_APPLICATIONS |
            ALLOW_CREATE_APPLICATIONS |
            ALLOW_CHANGE_CONFIG
        ]

        self.app_settings = [
            USE_AES | number_of_keys
        ]
