from socket import AddressFamily, SocketKind, socket
from threading import Thread

# for AES
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

ENCRYPTION_KEY:bytes = b''
BLOCK_SIZE = 16

class Receiver(Thread):
    def __init__(self, socket:socket):
        super().__init__()
        self.socket = socket

    def decrypt(self, ciphertext:bytes) -> bytes:
        # place your own implementation of
        # AES-128-ECB decryption with pycryptodome
        aes = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
        plain = aes.decrypt(ciphertext)
        plainText = unpad(plain, BLOCK_SIZE)
        return plainText
                
    def handle_recv(self, received:bytes):
        try:
            decrypt_result = self.decrypt(received)
            # Message 받을 때 개행 이상해짐.. 
            # print()
            # print("Received: " + bytes.decode(decrypt_result, "UTF-8"))
            # print('Message: ', end="")
            
            print("Received: " + bytes.decode(decrypt_result, "UTF-8"))
        except:
            pass

    def run(self):
        while True:
            received:bytes = self.socket.recv(1024)
            self.handle_recv(received)

def encrypt_message(msg: bytes) -> bytes:
    # place your own implementation of
    # AES-128-ECB encryption with pycryptodome
    paddedText = pad(msg, BLOCK_SIZE)
    aes = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    cipherText = aes.encrypt(paddedText)

    return cipherText

client_socket = socket(AddressFamily.AF_INET, SocketKind.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 24000))

print("[*] connected to 127.0.0.1:24000, Receiving an encryption key...")

# try to receive encryption key (128bits)
ENCRYPTION_KEY = client_socket.recv(16)
print("[*] Key received: " + str(ENCRYPTION_KEY))
print("[*] Now a chatting session is starting...")

# start receiving messages and chatting
Receiver(client_socket).start()

while True:
    msg = input("Message: ")
    msg_encoded = msg.encode("UTF-8")

    payload = encrypt_message(msg_encoded)
    client_socket.send(payload)
    
    print("Me: " + msg)
