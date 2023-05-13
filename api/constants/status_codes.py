dispenser_status_codes = {
    0x30: "No Card Inside Card Dispenser",
    0x31: "One Card Inside Card Dispenser",
    0x32: "Card in RF/IC Position"
}

stacker_status_codes = {
    0x30: "No Card Inside Stacker",
    0x31: "A Few Cards Inside Stacker",
    0x32: "Sufficient Cards Inside Stacker"
}

capture_box_status_codes = {
    0x30: "Capture Box Capacity NOT Full",
    0x31: "Capture Box Capacity Full"
}


def _get_status(raw_response: list) -> dict:
    st0, st1, st2 = raw_response[7], raw_response[8], raw_response[9]
    status = {
        'dispenser_status':     {'code': st0, 'message': dispenser_status_codes[st0]},
        'stacker_status':       {'code': st1, 'message': stacker_status_codes[st1]},
        'capture_box_status':   {'code': st2, 'message': capture_box_status_codes[st2]}
    }
    return status
