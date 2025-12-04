import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
from .cipher_interface import CipherInterface

class DESCipher(CipherInterface):
    def decrypt(self, text: str, key: str) -> str:
        try:

            key_bytes = key.encode('utf-8')
            while len(key_bytes) < 8:
                key_bytes += b' '
            key_bytes = key_bytes[:8] 

            raw_data = base64.b64decode(text)

            iv = raw_data[:8]
            ciphertext = raw_data[8:]

            cipher = DES.new(key_bytes, DES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)
            
            return plaintext.decode('utf-8')
        except Exception as e:
            return f"Hata: DES çözülemedi. ({str(e)})"