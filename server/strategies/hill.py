from strategies.cipher_interface import CipherInterface


class HillCipher(CipherInterface):
    def mod_inverse(self, a, m):
        for x in range(1, m):
            if (a * x) % m == 1: return x
        return None

    def decrypt(self, text: str, key: str) -> str:
        try:
            # Key format: "3,3,2,5" -> [[3, 3], [2, 5]]
            k = list(map(int, key.split(',')))
            det = (k[0] * k[3] - k[1] * k[2]) % 26
            det_inv = self.mod_inverse(det, 26)
            
            if det_inv is None:
                return "Hata: Matrisin tersi yok (Determinant 26 ile aralarında asal değil)."

            # Adjoint matris hesaplama ve tersini bulma
            # [[d, -b], [-c, a]] * det_inv
            inv_matrix = [
                (k[3] * det_inv) % 26,
                (-k[1] * det_inv) % 26,
                (-k[2] * det_inv) % 26,
                (k[0] * det_inv) % 26
            ]

            result = ""
            text = text.upper().replace(" ", "")
            for i in range(0, len(text), 2):
                p1, p2 = ord(text[i]) - 65, ord(text[i+1]) - 65
                c1 = (inv_matrix[0] * p1 + inv_matrix[1] * p2) % 26
                c2 = (inv_matrix[2] * p1 + inv_matrix[3] * p2) % 26
                result += chr(c1 + 65) + chr(c2 + 65)
            return result
        except:
            return "Hata: Hill anahtarı 'a,b,c,d' formatında 4 sayı olmalıdır."