from Crypto.Cipher import AES
import hashlib
from decouple import config

workingKey = config("WORKING_KEY")

def pad(data):
    length = 16 - (len(data)%16)
    data += chr(length) * length
    return data

def encrypt(plainText,workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    plainText = pad(plainText)
    encDigest = hashlib.md5(workingKey.encode()).digest()
    enc_cipher = AES.new(encDigest, AES.MODE_CBC, iv)
    encryptedText = enc_cipher.encrypt(plainText.encode()).hex()
    return encryptedText

def decrypt(cipherText,workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    decDigest = hashlib.md5(workingKey.encode()).digest()
    encryptedText = bytes.fromhex(cipherText)
    dec_cipher = AES.new(decDigest, AES.MODE_CBC, iv)
    decryptedText = dec_cipher.decrypt(encryptedText).decode().rstrip('\x06\x05\x04\x03\x02\x01')
    return decryptedText