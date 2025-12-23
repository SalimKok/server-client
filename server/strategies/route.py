import math
from .cipher_interface import CipherInterface

class RouteCipher(CipherInterface):
    def decrypt(self, text: str, key: str) -> str:
        """
        Route Cipher deşifreleme: Sütun bazlı okunan metni satır bazlı hale getirir.
        """
        try:
            num_cols = int(key)
            if num_cols <= 0:
                return "Hata: Geçersiz sütun sayısı."

            # Satır sayısını hesapla
            num_rows = math.ceil(len(text) / num_cols)
            
            # Şifreli metin sütun bazlı okunduğu için, 
            # deşifre ederken metni sütun sütun ızgaraya yerleştirmeliyiz.
            grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
            
            idx = 0
            for c in range(num_cols):
                for r in range(num_rows):
                    if idx < len(text):
                        grid[r][c] = text[idx]
                        idx += 1
            
            # Orijinal metni elde etmek için satır satır oku
            result = ""
            for r in range(num_rows):
                for c in range(num_cols):
                    result += grid[r][c]
            
            # Padding (X karakterleri) temizlenebilir veya olduğu gibi bırakılabilir
            return result.rstrip('X')
            
        except ValueError:
            return "Hata: Anahtar tam sayı olmalıdır."
        except Exception as e:
            return f"Sistem Hatası: {str(e)}"