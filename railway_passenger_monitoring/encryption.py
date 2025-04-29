import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

class EncryptionHandler:
    def __init__(self):
        """Initialize encryption with key from environment."""
        load_dotenv()
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            raise ValueError("ENCRYPTION_KEY not found in .env file.")
        self.fernet = Fernet(key)

    def encrypt(self, data):
        """Encrypt data."""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        """Decrypt data."""
        return self.fernet.decrypt(encrypted_data.encode()).decode()