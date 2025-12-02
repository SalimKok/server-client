from .cipher_interface import CipherInterface

class AffineCipher(CipherInterface):
    def mod_inverse(self, a, m):
        for x in range(1, m):
            if (a * x) % m == 1: return x
        return None

    def decrypt(self, text: str, key: str) -> str:
        try:
            # Anahtar formatı: "5,8" (a=5, b=8)
            parts = key.split(',')
            a, b = int(parts[0]), int(parts[1])
            
            a_inv = self.mod_inverse(a, 26)
            if a_inv is None: return "Hata: 'a' sayısı 26 ile aralarında asal olmalı."

            result = ""
            for char in text:
                if char.isalpha():
                    y = ord(char.upper()) - 65
                    # D(x) = a^-1 * (y - b) % 26
                    decrypted_char = chr(((a_inv * (y - b)) % 26) + 65)
                    result += decrypted_char if char.isupper() else decrypted_char.lower()
                else:
                    result += char
            return result
        except:
            return "Hata: Anahtar formatı 'a,b' olmalı (Örn: 5,8)"