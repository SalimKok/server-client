import math
from .cipher_interface import CipherInterface

class ColumnarCipher(CipherInterface):
    def decrypt(self, text: str, key: str) -> str:
        key_indices = sorted(list(enumerate(key)), key=lambda x: x[1])
        msg_len = len(text)
        col_count = len(key)
        row_count = math.ceil(msg_len / col_count)
        
        empty_cells = (row_count * col_count) - msg_len
        grid = [''] * col_count
        
        current_idx = 0
        for k_idx, char in key_indices:
            col_len = row_count - 1 if k_idx >= col_count - empty_cells else row_count
            grid[k_idx] = text[current_idx : current_idx + col_len]
            current_idx += col_len
            
        result = ""
        for r in range(row_count):
            for c in range(col_count):
                if r < len(grid[c]):
                    result += grid[c][r]
        return result