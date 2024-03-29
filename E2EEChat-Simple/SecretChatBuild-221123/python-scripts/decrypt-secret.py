from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def decode_base64(b64):
    return base64.b64decode(b64)

def encode_base64(p):
    return base64.b64encode(p).decode('ascii')

def read_from_base64():
    # a = input()
    # b = input()
    # return [ decode_base64(a+'='*(4-len(a)%4)), decode_base64(b+'='*(4-len(b)%4)) ]
    return [decode_base64(input()), decode_base64(input())]

def decrypt_secret(secret, priKey):
    # PKCS#1 OAEP를 이용한 RSA 복호화 구현
    key = RSA.import_key(priKey)
    pkcs = PKCS1_OAEP.new(key)
    decrypted_key = pkcs.decrypt(secret)
    return encode_base64(decrypted_key)

[secret, prikey] = read_from_base64()
result = decrypt_secret(secret, prikey)
print(result)