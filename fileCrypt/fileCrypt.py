#!/usr/bin/python
# -*- coding: utf-8 -*-

# 
# fileCrypt - fileCrypt.py
# ------------------------
# en/decrypts files

import os
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
import tempfile


def _derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]


def _encrypt(inObject, password, key_length=32):
    """
    encrypts the inObject to a string and returns it
    """
    in_file = _mkFile(inObject)
    ret = ''
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = _derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ret = 'Salted__' + salt
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        ret += (cipher.encrypt(chunk))
    return ret


def _decrypt(inObject, password, key_length=32):
    """
    decrypts the inObject to a string and returns it
    """
    in_file = _mkFile(inObject)
    ret = ''
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = _derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        ret += chunk
    return ret


def _mkFile(inObject):
    """
    turns inObject into a file if available. currently str, files, fileURLs are available
    """
    if type(inObject) in [file]:
        ret = inObject
    elif type(inObject) in [str, unicode]:
        if len(inObject) <= 128:
            try:
                fExists = os.path.exists(inObject)
            except Exception:
                fExists = False
            if fExists:
                ret = open(inObject, 'rb')
            else:
                temp = tempfile.NamedTemporaryFile(delete=False)
                temp.write(inObject)
                temp.flush()
                temp.seek(0)
                ret = temp
        else:
            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.write(inObject)
            temp.flush()
            temp.seek(0)
            ret = temp
    return ret


def _writeFile(string, fileName):
    """
    writes a string to a file
    """
    try:
        with open(fileName, 'wb') as f:
            f.write(string)
    except Exception as e:
        raise e

def encryptToFile(inObject, outFilePath, password, key_length=32):
    """
    encrypts an object to a file
    """    
    string = _encrypt(inObject, password, key_length)
    _writeFile(string, outFilePath)


def decryptToFile(inObject, outFilePath, password, key_length=32):
    """
    decrypts an object to a file
    """
    string = _decrypt(inObject, password, key_length)
    _writeFile(string, outFilePath)    


def encrypt(inObject, password, key_length=32):
    """
    encrypts a file to a string
    """
    ret = _encrypt(inObject, password, key_length)
    return ret


def decrypt(inObject, password, key_length=32):
    """
    decrypts a file to a string
    """
    ret = _decrypt(inObject, password, key_length)
    return ret


if __name__ == '__main__':
    pass