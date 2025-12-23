from strategies.cipher_interface import CipherInterface

class PolybiusCipher(CipherInterface):
    def decrypt(self, text: str, key: str) -> str:
        # Standart Polybius Square (I/J aynı hücrede)
        square = {
            '11': 'A', '12': 'B', '13': 'C', '14': 'D', '15': 'E',
            '21': 'F', '22': 'G', '23': 'H', '24': 'I', '25': 'L',
            '31': 'M', '32': 'N', '33': 'O', '34': 'P', '35': 'Q',
            '41': 'R', '42': 'S', '43': 'T', '44': 'U', '45': 'V',
            '51': 'W', '52': 'X', '53': 'Y', '54': 'Z'
        }
        try:
            # Input format: "23 15 25 25 33" (HELLO)
            parts = text.split()
            return "".join([square.get(p, "?") for p in parts])
        except:
            return "Hata: Geçersiz Polybius formatı."