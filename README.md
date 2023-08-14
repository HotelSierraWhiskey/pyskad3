# SK-AD3 Card Dispenser

## What is this?

This repository contains the SK-AD3 Card Dispenser python API. The API implements high level endpoints for most of what the SK-AD3 is capable of. It's important to note right off the bat that the SK-AD3 performs two distinct sets of operations. The first set of operations are native commands used to manipulate the mechanical components and sensors of the device (moving a card to the capture box, reading the state of the stacker, etc.). The second set of operations has to do with communication with RFID cards (this API currently only supports communication with DESFire EV1 cards). The first set of operations involves serial communication with the dispenser. The second set of operations involves communication with an RFID card *through* a serial connection to the dispenser. As such, this project exposes two APIs, one for basic SK-AD3 operations, and one for RFID operations. However, since RFID communication is proxied through the dispenser, the desfire API relies on resources that are properly part of basic dispenser code. 

## Examples

Importing the module, creating a dispenser object, and using it to initialize the SK AD3 is fairly intuitive. Every command returns a response that can be used to check the state of the the device.
```python
from SK_AD3_Card_Dispenser import SK_AD3


dispenser = SK_AD3('COM7')
response = dispenser.init()

if response.is_successful():
    print(response.status())
```

Basic mechanical commands such as moving a card to a given position - such as the "RF" position - can be issued like so:
```python
response = dispenser.move_card('RF')
```


Once a card is in the "RF" Position you can activate the card and begin communication. This is an example of how you can activate a Type A RFID card and obtain its UID:
```python
response = dispenser.activate_RF_card('type_a')

if response.is_successful():
    response = dispenser.get_card_uid()
    uid = response.data['uid']

    # Do something with uid
```

Certain RFID operations require authentication. The SK AD3 performs external authentication on the card level and application level. You will need to authenticate according to the settings on the card. The authentication response object will conveniently hold the generated session key, which can be used for encrypted communication and sensitive RFID commands.

```python
response = dispenser.aes_authenticate(SUPER_SECRET_AES_MASTER_KEY)

if response.is_successful():
    session_key = response.data['session_key']
```

Once properly authenticated, applications can be created on the card by using built-in presets:
```python
from SK_AD3_Card_Dispenser.file_objects.application import PermissiveDesfireApplication


my_app = PermissiveDesfireApplication([0xAB, 0xCD, 0xEF])

dispenser.create_application(my_app)
```

Same goes for files:
```python
from SK_AD3_Card_Dispenser.file_objects.file import PermissiveStandardDataFile

my_file = PermissiveStandardDataFile([0x00])

dispenser.select_application([0xAB, 0xCD, 0xEF])

dispenser.create_standard_data_file(my_file)    
```

Or, if you have specific needs, you can send generic APDUs to the card. The code below is equivalent to the above code, except `send_raw_apdu` will return a raw Command Package in the form of a list of integers instead of a ```Response``` object:

```python
dispenser.send_raw_apdu([0x90, 0x5A, 0x00, 0x00, 0x03, 0xAB, 0xCD, 0xEF, 0x00])
dispenser.send_raw_apdu([0x90, 0xCD, 0x00, 0x00, 0x07, 0x00, 0x00, 0xEE, 0xEE, 0x10, 0x00, 0x00, 0x00])
```

## Dependencies

Python 3 (v3.11 recommended).

This project uses [APDU Utils](https://github.com/HotelSierraWhiskey/apdu_utils) as a git submodule. Clone this project using the ```---recurse-submodules``` flag to ensure that APDU Utils comes included. The following modules also need to be installed in your environment:

- numpy
- pycryptodome

run 

```pip install -r requirements.txt```

to update your dependencies.

## Sources

The documentation for DESFire EV1 cards is subject to NDA. As such, this repository owes its existence to those individuals who have made their efforts reverse engineering these cards public. The following sources were used in the development of this project:

- [NXP MIFARE DESFire EV1 Protocol Manual](https://raw.githubusercontent.com/revk/DESFireAES/master/DESFire.pdf) - written by [RevK](https://github.com/revk)
- [Ridrix's Blog](https://ridrix.wordpress.com/tag/desfire-protocol/) and commenters
- ISO/IEC 14443
- [ISO/IEC 7816-4](https://github.com/dongri/emv-qrcode-doc/blob/master/ISO%20IEC%207816-4.pdf)
- [EFTlab's Complete APDU Reponses document](https://www.eftlab.com/knowledge-base/complete-list-of-apdu-responses)
