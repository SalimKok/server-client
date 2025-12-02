from .cipher_interface import CipherInterface

class CaesarCipher(CipherInterface):
    def decrypt(self, text: str, key: str) -> str:
        try:
            shift = int(key)
            result = ""
            for char in text:
                if char.isalpha():
                    ascii_offset = 65 if char.isupper() else 97
                    # Şifrelemede +shift yapıldıysa, deşifrelemede -shift yapılır
                    result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
                else:
                    result += char
            return result
        except ValueError:
            return "Hata: Anahtar bir tam sayı olmalıdır."  