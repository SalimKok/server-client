# Polybius karesi oluştur
polybius_square = {
    'A': '11', 'B': '12', 'C': '13', 'D': '14', 'E': '15',
    'F': '21', 'G': '22', 'H': '23', 'I': '24', 'J': '24', 'K': '25',
    'L': '31', 'M': '32', 'N': '33', 'O': '34', 'P': '35',
    'Q': '41', 'R': '42', 'S': '43', 'T': '44', 'U': '45',
    'V': '51', 'W': '52', 'X': '53', 'Y': '54', 'Z': '55'
}

# Ters çevir — çözme işlemi için
reverse_polybius = {v: k for k, v in polybius_square.items()}

def encrypt(message):
    encrypted = ""
    for char in message.upper():
        if char == " ":
            encrypted += " "   # Boşluğu koru
        elif char in polybius_square:
            encrypted += polybius_square[char] + " "
    return encrypted.strip()

def decrypt(code):
    decrypted = ""
    parts = code.split(" ")
    for part in parts:
        if part == "":
            decrypted += " "
        elif part in reverse_polybius:
            decrypted += reverse_polybius[part]
    return decrypted

