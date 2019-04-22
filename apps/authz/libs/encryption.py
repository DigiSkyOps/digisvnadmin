#!/usr/bin/env python
# -*-coding:utf-8-*-
# Created by Eric.wu on 2019/3/29 

import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class PasswdCrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def pw_encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16
        count = len(text)
        if (count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\x00' * add)

        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def pw_decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode().replace('\x00', '')


