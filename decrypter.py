from Crypto.Cipher import AES
from argon2 import PasswordHasher
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
def derive_encryption_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000,
    )
    encryption_key = kdf.derive(master_password.encode())
    return encryption_key

def decrypt_password(encryption_key, ciphertext, nonce, tag):
    cipher_decrypt = AES.new(encryption_key, AES.MODE_EAX, nonce=nonce)
    try:
        plaintext = cipher_decrypt.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        print("The message was modified!")
        return None
    try:
        password = plaintext.decode('utf-8')
    except UnicodeDecodeError as e:
        print(f"Decoding error occurred: {e}")
        return None
    return password