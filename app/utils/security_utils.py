import os
from cryptography.fernet import Fernet
import base64

# --- Key Management ---
def generate_key():
    key = Fernet.generate_key()
    return key.decode()

def load_key(key_file='encryption.key'):
    try:
        with open(key_file, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        save_key(key, key_file)
        return key

def save_key(key, key_file='encryption.key'):
    with open(key_file, 'wb') as f:
        f.write(key)

# --- Encryption/Decryption ---
def encrypt_data(data: str, key: bytes) -> str:
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data.encode())
    return decrypted_data.decode()