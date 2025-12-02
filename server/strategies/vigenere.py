from .cipher_interface import CipherInterface

class VigenereCipher(CipherInterface):
    def decrypt(self, text: str, key: str) -> str:
        if not key: return text
        
        decrypted_text = []
        key_index = 0
        key = key.upper()
        
        for char in text:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - 65
                if char.isupper():
                    decrypted_char = chr((ord(char) - 65 - shift) % 26 + 65)
                else:
                    decrypted_char = chr((ord(char) - 97 - shift) % 26 + 97)
                
                decrypted_text.append(decrypted_char)
                key_index += 1
            else:
                decrypted_text.append(char)
                
        return "".join(decrypted_text)