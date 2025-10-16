def _get_key_order(key):
    return sorted(range(len(key)), key=lambda x: key[x])

def encrypt(text, key):
    cols = len(key)                 
    rows = (len(text) + cols - 1) // cols  

    mat = [['*'] * cols for _ in range(rows)]

    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(text):
                mat[r][c] = text[idx]
                idx += 1

    order = _get_key_order(key)

    sonuc = ""
    for col in order:
        for r in range(rows):
            sonuc += mat[r][col]

    return sonuc

def decrypt(text, key):
    cols = len(key)             
    rows = (len(text) + cols - 1) // cols

    mat = [[' '] * cols for _ in range(rows)]

    order = _get_key_order(key)

    idx = 0
    for col in order:
        for r in range(rows):
            if idx < len(text):
                mat[r][col] = text[idx]
                idx += 1

    sonuc = ""
    for r in range(rows):
        for c in range(cols):
            sonuc += mat[r][c]

    return sonuc
