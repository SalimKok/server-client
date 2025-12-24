import base64
import os
from .cipher_interface import CipherInterface

PI = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

PI_1 = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

S_BOX = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

PC_1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

PC_2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

class DESCipher(CipherInterface):
    def _bin_to_int(self, bits):
        res = 0
        for bit in bits:
            res = (res << 1) | bit
        return res

    def _int_to_bin(self, val, length):
        res = []
        for i in range(length):
            res.append((val >> (length - 1 - i)) & 1)
        return res

    def _permute(self, bits, table):
        return [bits[x - 1] for x in table]

    def _xor(self, b1, b2):
        return [x ^ y for x, y in zip(b1, b2)]

    def _generate_keys(self, key_str_bytes):
        key_bits = []
        for b in key_str_bytes:
            key_bits.extend(self._int_to_bin(b, 8))

        key_bits = self._permute(key_bits, PC_1)
        L, R = key_bits[:28], key_bits[28:]
        
        subkeys = []
        for shift in SHIFT_TABLE:
            L = L[shift:] + L[:shift]
            R = R[shift:] + R[:shift]
            subkeys.append(self._permute(L + R, PC_2))
        return subkeys

    def _f_function(self, R, k):
        expanded_R = self._permute(R, E)
        xored = self._xor(expanded_R, k)
        output = []
        for i in range(0, 48, 6):
            chunk = xored[i:i+6]
            row = (chunk[0] << 1) + chunk[5]
            col = (chunk[1] << 3) + (chunk[2] << 2) + (chunk[3] << 1) + chunk[4]
            output.extend(self._int_to_bin(S_BOX[i // 6][row][col], 4))
        return self._permute(output, P)

    def _pkcs7_pad(self, data):
        pad_len = 8 - (len(data) % 8)
        return data + bytes([pad_len] * pad_len)

    def _process_block(self, block_bits, subkeys):
        """Tek bir DES bloğunu (şifreleme/çözme için) işler."""
        current_bits = self._permute(block_bits, PI)
        L, R = current_bits[:32], current_bits[32:]
        for k in subkeys:
            L, R = R, self._xor(L, self._f_function(R, k))
        return self._permute(R + L, PI_1)

    def encrypt(self, text: str, key: str) -> str:
        """Kütüphanesiz Manuel DES-CBC Şifreleme"""
        try:
            key_bytes = key.encode('utf-8').ljust(8, b' ')[:8]
            subkeys = self._generate_keys(key_bytes)
            
            iv = os.urandom(8)
            plaintext = self._pkcs7_pad(text.encode('utf-8'))
            
            ciphertext = bytearray()
            prev_bits = []
            for b in iv: prev_bits.extend(self._int_to_bin(b, 8))

            for i in range(0, len(plaintext), 8):
                block_bytes = plaintext[i:i+8]
                block_bits = []
                for b in block_bytes: block_bits.extend(self._int_to_bin(b, 8))
                
                xor_bits = self._xor(block_bits, prev_bits)
                encrypted_bits = self._process_block(xor_bits, subkeys)
       
                for j in range(0, 64, 8):
                    ciphertext.append(self._bin_to_int(encrypted_bits[j:j+8]))
                prev_bits = encrypted_bits

            return base64.b64encode(iv + ciphertext).decode('utf-8')
        except Exception as e:
            return f"Manuel DES Encrypt Hatası: {str(e)}"

    def decrypt(self, text: str, key: str) -> str:
        """Kütüphanesiz Manuel DES-CBC Deşifreleme"""
        try:
            key_bytes = key.encode('utf-8').ljust(8, b' ')[:8]
            subkeys = self._generate_keys(key_bytes)[::-1]

            raw_data = base64.b64decode(text)
            iv_bytes, ct_bytes = raw_data[:8], raw_data[8:]
            
            iv_bits = []
            for b in iv_bytes: iv_bits.extend(self._int_to_bin(b, 8))

            decrypted_bytes = []
            prev_cipher_bits = iv_bits

            for i in range(0, len(ct_bytes), 8):
                block_bits = []
                for b in ct_bytes[i:i+8]: block_bits.extend(self._int_to_bin(b, 8))
                
                processed_bits = self._process_block(block_bits, subkeys)
                plain_bits = self._xor(processed_bits, prev_cipher_bits)
                
                for j in range(0, 64, 8):
                    decrypted_bytes.append(self._bin_to_int(plain_bits[j:j+8]))
                prev_cipher_bits = block_bits

            pad_len = decrypted_bytes[-1]
            return bytes(decrypted_bytes[:-pad_len]).decode('utf-8')
        except Exception as e:
            return f"Manuel DES Decrypt Hatası: {str(e)}"

# --- KÜTÜPHANE KULLANILAN VERSİYON  ---
'''
import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

class DESCipher(CipherInterface):
    def encrypt(self, text: str, key: str) -> str:
        key_bytes = key.encode('utf-8').ljust(8, b' ')[:8]
        cipher = DES.new(key_bytes, DES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), DES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')

    def decrypt(self, text: str, key: str) -> str:
        raw_data = base64.b64decode(text)
        iv, ct = raw_data[:8], raw_data[8:]
        key_bytes = key.encode('utf-8').ljust(8, b' ')[:8]
        cipher = DES.new(key_bytes, DES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), DES.block_size).decode('utf-8')
'''