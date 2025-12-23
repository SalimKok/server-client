from .cipher_interface import CipherInterface

class PlayfairCipher(CipherInterface):
    def _generate_matrix(self, key: str):
        key = key.upper().replace('J', 'I')
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        combined = ""
        for char in key + alphabet:
            if char not in combined and char.isalpha():
                combined += char
        
        return [list(combined[i:i+5]) for i in range(0, 25, 5)]

    def _find_position(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None

    def decrypt(self, text: str, key: str) -> str:
        try:
            matrix = self._generate_matrix(key)
            text = text.upper().replace('J', 'I').replace(" ", "")
            result = ""

            for i in range(0, len(text), 2):
                r1, c1 = self._find_position(matrix, text[i])
                r2, c2 = self._find_position(matrix, text[i+1])

                if r1 == r2: # Aynı satır
                    result += matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
                elif c1 == c2: # Aynı sütun
                    result += matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
                else: # Dikdörtgen
                    result += matrix[r1][c2] + matrix[r2][c1]
            return result
        except Exception as e:
            return f"Hata: Playfair deşifre edilemedi. {str(e)}"