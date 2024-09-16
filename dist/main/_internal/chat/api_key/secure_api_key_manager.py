from cryptography.fernet import Fernet
import os
from ..config import KEY_PATH


class APIKeyManager:
    def __init__(self,
                 cache_file_path,
                 key_file_path=KEY_PATH):
        self.cache_file_path = cache_file_path
        self.key_file_path = key_file_path
        self.key = self._get_key()

    def _get_key(self):
        if os.path.exists(self.key_file_path):
            with open(self.key_file_path, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file_path, 'wb') as f:
                f.write(key)
            return key

    def encrypt_api_key(self, api_key):
        cipher_suite = Fernet(self.key)
        encrypted_api_key = cipher_suite.encrypt(api_key.encode())
        return encrypted_api_key

    def decrypt_api_key(self, encrypted_api_key):
        cipher_suite = Fernet(self.key)
        api_key = cipher_suite.decrypt(encrypted_api_key).decode()
        return api_key

    def save_api_key(self, api_key):
        encrypted_api_key = self.encrypt_api_key(api_key)
        with open(self.cache_file_path, 'wb') as f:
            f.write(encrypted_api_key)

    def load_api_key(self):
        try:
            with open(self.cache_file_path, 'rb') as f:
                encrypted_api_key = f.read()
            api_key = self.decrypt_api_key(encrypted_api_key)
            return api_key
        except FileNotFoundError:
            return None
