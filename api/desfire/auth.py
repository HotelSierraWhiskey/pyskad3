from Crypto.Cipher import AES, DES
import numpy as np
from collections import deque


class Auth:
    def __init__(self, key, auth_type: str):
        self.engine = None
        self.index = None
        if auth_type == 'AES':
            self.engine = AES
            self.index = 16
        if auth_type == 'DES':
            self.engine = DES
            self.index = 8

        assert (self.engine and self.index)

        self.key = key
        self.iv = None
        self.cipher = None
        self.random_a = None
        self.random_b = None
        self.session_key = None
        self.authenticated = False

    def _first_pass(self, ciphertext: list) -> list:
        '''
        Internal use only.
        Performs an external authentication procedure.
        '''
        ciphertext = bytearray(ciphertext)
        self.iv = bytearray([0x00] * self.index)
        self.cipher = self.engine.new(
            self.key, self.engine.MODE_CBC, iv=self.iv)
        self.random_b = self.cipher.decrypt(ciphertext)
        self.random_a = list(np.random.randint(0, 255, self.index))
        random_b_prime = deque(list(self.random_b))
        random_b_prime.rotate(-1)
        random_b_prime = list(random_b_prime)
        concatenated = bytearray(self.random_a + random_b_prime)
        self.iv = ciphertext
        cipher = self.engine.new(self.key, self.engine.MODE_CBC, iv=self.iv)
        encrypted_concatenated = cipher.encrypt(concatenated)
        self.iv = encrypted_concatenated[-self.index:]
        result = list(encrypted_concatenated)
        return result

    def _second_pass(self, ciphertext: list) -> None:
        '''
        Internal use only.
        Decrypt last response. If it matches the original `random_a` (rotated one byte left),
        the reader knows the card has the same self.engine key.
        It assumes that external_authentication has already been called. 
        '''
        cipher = self.engine.new(self.key, self.engine.MODE_CBC, iv=self.iv)
        ciphertext = bytearray(ciphertext)
        result = cipher.decrypt(ciphertext)
        check = deque(self.random_a)
        check.rotate(-1)
        self.authenticated = list(check) == list(result)
        if self.authenticated:
            if self.engine == AES:
                part_1 = list(self.random_a[:4]) + list(self.random_b[:4])
                part_2 = list(self.random_a[-4:]) + list(self.random_b[-4:])
                self.session_key = part_1 + part_2
            if self.engine == DES:
                self.session_key = list(self.random_a[:4]) + list(self.random_b[:4])
