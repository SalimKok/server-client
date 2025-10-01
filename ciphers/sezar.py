def encrypt(text, key):
    key = int(key)
    sonuc = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            sonuc += chr((ord(ch)-base+key)%26 + base)
        else:
            sonuc += ch
    return sonuc

def decrypt(text, key):
    return encrypt(text, -int(key))
