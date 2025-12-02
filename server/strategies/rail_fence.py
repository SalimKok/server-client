from .cipher_interface import CipherInterface

class RailFenceCipher(CipherInterface):
    def decrypt(self, text: str, key: str) -> str:
        try:
            num_rails = int(key)
            rail = [['\n' for i in range(len(text))] for j in range(num_rails)]
            
            dir_down = None
            row, col = 0, 0
            
            # Zikzak haritasını işaretle
            for i in range(len(text)):
                if row == 0: dir_down = True
                if row == num_rails - 1: dir_down = False
                rail[row][col] = '*'
                col += 1
                row += 1 if dir_down else -1
                
            # Harfleri yerine koy
            index = 0
            for i in range(num_rails):
                for j in range(len(text)):
                    if rail[i][j] == '*' and index < len(text):
                        rail[i][j] = text[index]
                        index += 1
            
            # Okuma yap
            result = []
            row, col = 0, 0
            for i in range(len(text)):
                if row == 0: dir_down = True
                if row == num_rails - 1: dir_down = False
                if rail[row][col] != '\n':
                    result.append(rail[row][col])
                    col += 1
                row += 1 if dir_down else -1
                
            return "".join(result)
        except:
            return "Hata: Anahtar bir tamsayı olmalı."