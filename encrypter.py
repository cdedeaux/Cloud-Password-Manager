from Crypto.Cipher import AES
from argon2 import PasswordHasher
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
ph = PasswordHasher(hash_len=32)
def generate_salt():
    salt = os.urandom(16)
    return salt
def get_master_password():
    master_password = input("Enter your master password: ")
    return master_password
def get_verification_hash(master_password):
    return ph.hash(master_password)
def create_encrypted_data(master_password, web_pass, salt):
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=1_200_000,
    )
    encryption_key = kdf.derive(master_password.encode())
    cipher = AES.new(encryption_key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(web_pass.encode())
    return nonce, tag, ciphertext


