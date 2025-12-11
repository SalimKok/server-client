from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class RSACipher:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.private_key = self.key
        self.public_key = self.key.publickey()

    def get_public_key_pem(self) -> bytes:
        """İstemciye gönderilecek Public Key formatı"""
        return self.public_key.export_key()

    def decrypt_session_key(self, encrypted_key_b64: str) -> str:
        """
        İstemciden gelen Base64 formatındaki şifreli AES anahtarını çözer.
        """
        try:
            encrypted_bytes = base64.b64decode(encrypted_key_b64)

            cipher_rsa = PKCS1_OAEP.new(self.private_key)
            decrypted_session_key = cipher_rsa.decrypt(encrypted_bytes)

            return decrypted_session_key.decode('utf-8')

        except Exception as e:
            print(f"RSA Decrypt Hatası: {e}")
            return None