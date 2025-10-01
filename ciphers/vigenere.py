import string
alfabe = string.ascii_lowercase

def encrypt(text, key):
    key=key.lower()
    sonuc=""
    k=0
    for ch in text.lower():
        if ch in alfabe:
            shift=alfabe.index(key[k%len(key)])
            sonuc+=alfabe[(alfabe.index(ch)+shift)%26]
            k+=1
        else:
            sonuc+=ch
    return sonuc

def decrypt(text,key):
    key=key.lower()
    sonuc=""
    k=0
    for ch in text.lower():
        if ch in alfabe:
            shift=alfabe.index(key[k%len(key)])
            sonuc+=alfabe[(alfabe.index(ch)-shift)%26]
            k+=1
        else:
            sonuc+=ch
    return sonuc
