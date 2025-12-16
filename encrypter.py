from Crypto.Cipher import AES
from argon2 import PasswordHasher
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
def get_master_password():
    return input("Enter master password: ")

def salt():
    salt = os.urandom(16)
    #dbinsert(salt)
    return


ph = PasswordHasher(hash_len=32)
verification_hash = ph.hash(master_password)

salt = os.urandom(16) #store this salt securely

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=1_200_000,
)
encryption_key = kdf.derive(master_password.encode())
web_pass = input("Input password ")
cipher = AES.new(encryption_key, AES.MODE_EAX)
nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(web_pass.encode())
print("Ciphertext:", ciphertext)
print("Nonce:", nonce)
print("Tag:", tag)

cipher_decrypt = AES.new(encryption_key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher_decrypt.decrypt_and_verify(ciphertext, tag)
password = plaintext.decode()
print("Decrypted password:", password)