import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from .cipher_interface import CipherInterface

class AESCipher(CipherInterface):
    def decrypt(self, text: str, key: str) -> str:
        try:
            key_bytes = key.encode('utf-8')

            while len(key_bytes) < 32:
                key_bytes += b' '

            if len(key_bytes) > 32:
                key_bytes = key_bytes[:32]

            raw_data = base64.b64decode(text)

            iv = raw_data[:16]
            ciphertext = raw_data[16:]

            cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
            
            return plaintext.decode('utf-8')
        except Exception as e:
            return f"Hata: Şifre çözülemedi. ({str(e)})"