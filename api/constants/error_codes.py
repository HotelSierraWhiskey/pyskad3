sk_ad3_error_codes = {0x3030: "Undefined command",
                      0x3031: "Command parameter error",
                      0x3032: "Command execution sequence error",
                      0x3033: "Hardware does not support command",
                      0x3034: "Command data error in communication package",
                      0x3035: "IC card contact deactivates",
                      0x3130: "Card jam",
                      0x3132: "sensor error",
                      0x3133: "Too long card",
                      0x3134: "Too short card",
                      0x3430: "Card is withdrawn when retracting",
                      0x3431: "IC card solenoid error",
                      0x3433: "Disable to move to IC position",
                      0x3435: "Card is moved by outer force",
                      0x3530: "Counter overflow",
                      0x3531: "Motor error",
                      0x3630: "IC card power failure",
                      0x3631: "IC card activation failure",
                      0x3632: "IC card does not support current command",
                      0x3635: "IC card deactivates",
                      0x3636: "Current IC card does not support any command",
                      0x3637: "IC card data transmission error",
                      0x3638: "IC card data transmission timeout",
                      0x3639: "CPU/SAM card does not conform to EMV standard",
                      0x4130: "Stacker empty or no card inside stacker",
                      0x4131: "Capture box capacity full",
                      0x4230: "Card dispenser not reset"}


def _get_error(raw_response: list) -> dict:
    error_code = (raw_response[7] << 8) + raw_response[8]
    error = {
        'error': {'code': error_code, 'message': sk_ad3_error_codes[error_code]}
    }
    return error
