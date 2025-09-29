def sezar_sifrele(metin, kaydirma):
    sonuc = ""
    for ch in metin:
        if ch.isalpha():
            alfabe_baslangic = ord('A') if ch.isupper() else ord('a')
            yeni = (ord(ch) - alfabe_baslangic + kaydirma) % 26 + alfabe_baslangic
            sonuc += chr(yeni)
        else:
            sonuc += ch  
    return sonuc

def sezar_coz(metin, kaydirma):
    return sezar_sifrele(metin, -kaydirma)

orijinal = "selamin aleykum"
kaydirma = 3

sifreli = sezar_sifrele(orijinal, kaydirma)
print("Şifreli:", sifreli)

cozulmus = sezar_coz(sifreli, kaydirma)
print("Çözülmüş:", cozulmus)
