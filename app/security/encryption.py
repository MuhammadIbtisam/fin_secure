from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

def encrypt(data: str) -> bytes:
    encoded_data = data.encode()
    return cipher_suite.encrypt(encoded_data)

def decrypt(encrypted_data: bytes) -> str:
    decoded_data = cipher_suite.decrypt(encrypted_data)
    return decoded_data.decode()
