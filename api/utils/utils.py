def bcc(array):
    temp = 0
    for item in array:
        temp ^= item
    return temp


def bcc_eval(array, against):
    temp = 0
    for item in array:
        temp ^= item
    if temp == against:
        return True
    else:
        return False


def crc(data: list) -> int:
    poly = 0xEDB88320
    crc = 0xFFFFFFFF
    for n in range(len(data)):
        crc ^= data[n]
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
    return crc


def flip(crc: int) -> list:
    crc = hex(crc).replace('0x', '')
    crc = [crc[i:i+2] for i in range(0, len(crc), 2)][::-1]
    crc = [int(i, 16) for i in crc]
    return crc


def hexify(response: list) -> list:
    return [f'{i:#04x}' for i in response]
