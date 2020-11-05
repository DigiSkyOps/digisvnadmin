#!/usr/bin/env python
# -*-coding:utf-8-*-
# Created by Eric.wu on 2019/3/29 

import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

def add_to_16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return (text)

class PasswdCrypt():
    def __init__(self, key):
        self.key = add_to_16(key)
        self.mode = AES.MODE_CBC
        self.iv = bytes(16)

    def pw_encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
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
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode().replace('\x00', '')


