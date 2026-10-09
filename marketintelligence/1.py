from bcrypt import hashpw, gensalt, checkpw

from secrets import token_urlsafe

from cryptography.fernet import Fernet

SECRET_KEY = "sometextthatshouldbe32byteslong"  # This should be a secure key in production

class Security:
    def hash_password(self, password: str) -> str:
        hashed = hashpw(password.encode('utf-8'), gensalt())
        return hashed.decode('utf-8')

    def check_password(self, password: str, hashed: str) -> bool:
        return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def encrypt_data(self, data: str) -> str:
        fernet = Fernet(SECRET_KEY.encode('utf-8'))
        encrypted = fernet.encrypt(data.encode('utf-8'))
        return encrypted.decode('utf-8')

    def decrypt_data(self, encrypted_data: str) -> str:
        fernet = Fernet(SECRET_KEY.encode('utf-8'))
        decrypted = fernet.decrypt(encrypted_data.encode('utf-8'))
        return decrypted.decode('utf-8')


a = "password123"

print(Security().hash_password(a))

save_hash_password = Security().hash_password(a)
save_hash_password_encoded = save_hash_password.encode('utf-8')
save_hash_password_decoded = save_hash_password_encoded.decode('utf-8')

print(Security().check_password(a, save_hash_password))
print(Security().check_password(a, save_hash_password_decoded))
print(save_hash_password_encoded)
print(save_hash_password_decoded)