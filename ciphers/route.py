import math

def _spiral_indices(rows, cols):
    top, left = 0, 0
    bottom, right = rows - 1, cols - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            yield top, c
        top += 1
       
        for r in range(top, bottom + 1):
            yield r, right
        right -= 1
        if top <= bottom:
            
            for c in range(right, left - 1, -1):
                yield bottom, c
            bottom -= 1

        if left <= right:
            
            for r in range(bottom, top - 1, -1):
                yield r, left
            left += 1

def encrypt(text, key):
    rows, cols = map(int, key.split(","))
    temiz = text.replace("\n", " ")
    size = rows * cols
    
    PAD = "_"
    if len(temiz) < size:
        temiz = temiz + PAD * (size - len(temiz))
    elif len(temiz) > size:
        raise ValueError("Metin, belirtilen matris boyutuna sığmıyor.")

    mat = [[''] * cols for _ in range(rows)]
    idx = 0
    for r in range(rows):
        for c in range(cols):
            mat[r][c] = temiz[idx]
            idx += 1

    sonuc = ""
    for r, c in _spiral_indices(rows, cols):
        sonuc += mat[r][c]
    return sonuc

def decrypt(text, key):
    rows, cols = map(int, key.split(","))
    if rows * cols != len(text):
        raise ValueError("Şifre metni uzunluğu rows*cols ile eşleşmiyor.")
    
    mat = [[''] * cols for _ in range(rows)]
    it = iter(text)

    for r, c in _spiral_indices(rows, cols):
        mat[r][c] = next(it)

    sonuc = ""
    for r in range(rows):
        for c in range(cols):
            sonuc += mat[r][c]

    return sonuc.rstrip("_")
