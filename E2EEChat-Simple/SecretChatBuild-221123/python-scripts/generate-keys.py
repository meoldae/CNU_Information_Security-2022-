from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

def encode_base64(p):
    return base64.b64encode(p).decode('ascii')

# 32바이트 (256비트) 랜덤 비밀키 생성
secret = get_random_bytes(32)

# RSA 2048 키 생성 시작
rsa = RSA.generate(2048) 
# 공개키 export
pubkey = rsa.publickey().exportKey()
# 개인키 export
prikey = rsa.exportKey(pkcs=8)

print(encode_base64(secret) + '\n')

print(encode_base64(pubkey) + '\n')
print(encode_base64(prikey) + '\n')
