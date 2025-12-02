from .cipher_interface import CipherInterface

class SubstitutionCipher(CipherInterface):
    def decrypt(self, text: str, key: str) -> str:
        if len(key) != 26: return "Hata: Anahtar 26 harfli bir alfabe olmalı."
        
        std_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key_map = {k.upper(): v for k, v in zip(key, std_alphabet)}
        
        result = ""
        for char in text:
            if char.isalpha():
                decoded = key_map.get(char.upper(), char)
                result += decoded if char.isupper() else decoded.lower()
            else:
                result += char
        return result