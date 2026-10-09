from bcrypt import hashpw, gensalt, checkpw

from secrets import token_urlsafe

from cryptography.fernet import Fernet

from base64 import urlsafe_b64encode, urlsafe_b64decode

from hashlib import sha256

SECRET_KEY = "sometextthatshouldbe32byteslong"  # This should be a secure key in production

class Security:
    def __init__(self):
        key_bytes = SECRET_KEY.encode('utf-8')
        key_digest = sha256(key_bytes).digest()
        fernet_key = urlsafe_b64encode(key_digest)
        self._fernet = Fernet(fernet_key)
    def hash_password(self, password: str) -> str:
        hashed = hashpw(password.encode('utf-8'), gensalt())
        return hashed.decode('utf-8')

    def check_password(self, password: str, hashed: str) -> bool:
        return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def encrypt_data(self, secret_data: str) -> str:
        return self._fernet.encrypt(secret_data.encode('utf-8')).decode('utf-8')

    def decrypt_data(self, encrypted_data: str) -> str:
        return self._fernet.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')

    def create_secret_key(self) -> str:
        return token_urlsafe(32)
    

security_instance = Security()