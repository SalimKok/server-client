from strategies.cipher_interface import CipherInterface


class VernamCipher(CipherInterface):
    def decrypt(self, text: str, key: str) -> str:
        try:
            if len(key) < len(text):
                return "Hata: Anahtar metinden kısa olamaz."
            
            text = text.upper()
            key = key.upper()
            result = ""
            
            for i in range(len(text)):
                p = (ord(text[i]) - ord(key[i])) % 26
                result += chr(p + 65)
            return result
        except:
            return "Hata: Vernam deşifre işlemi başarısız."