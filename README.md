Bu proje, mobil bir istemci (**Flutter**) ile sunucu (**Python/Flask**) arasında güvenli veri iletişimini simüle eden hibrit bir kriptografi uygulamasıdır. Klasik şifreleme yöntemlerinin yanı sıra, modern standartlar (AES, DES) ve güvenli anahtar değişimi için **RSA Handshake** mekanizmasını içerir.

## Proje Hakkında

Uygulama, güvensiz bir ağ üzerinde güvenli iletişim kurmayı amaçlar. İstemci tarafında metinler şifrelenir ve sunucuya gönderilir. Sunucu, şifreli metni ve anahtarı alarak orijinal metni çözer.

## Temel Özellikler
* **Hibrit Kriptografi:** Simetrik (AES, DES) ve Asimetrik (RSA) şifrelemenin birlikte kullanımı.
* **Digital Handshake:** Simetrik oturum anahtarlarının (Session Key), RSA Public Key ile şifrelenerek güvenli transferi.
* **Eğitim Odaklı Kodlama:** AES ve DES gibi algoritmaların matematiksel temelleri (S-Box, Permütasyonlar) Python tarafında manuel olarak da uygulanmıştır.
* **Çoklu Algoritma Desteği:** Hem klasik hem modern 8 farklı algoritma.

## Mimari ve Çalışma Mantığı

Sistem şu adımları izler:

1.  **Public Key Dağıtımı:** İstemci, sunucudan RSA Public Key'i talep eder.
2.  **Oturum Anahtarı (Session Key):** Kullanıcı bir şifreleme anahtarı (örn: "sifre123") belirler.
3.  **Handshake:** İstemci, bu anahtarı sunucunun Public Key'i ile şifreler ve sunucuya gönderir. (Man-in-the-Middle koruması).
4.  **Veri Transferi:** Mesaj, simetrik algoritma (AES/DES) ile şifrelenir ve sunucuya iletilir. Sunucu, Handshake sırasında aldığı anahtarı kullanarak mesajı çözer.

## Desteklenen Algoritmalar

## Modern Algoritmalar
* **AES (Advanced Encryption Standard):** CBC modu ile 128/192/256-bit şifreleme.
* **DES (Data Encryption Standard):** 64-bit blok şifreleme (Feistel yapısı).
* **RSA:** Anahtar değişimi (Key Exchange) için kullanılır.

## Klasik (Tarihsel) Algoritmalar
* **Caesar Cipher:** Harf öteleme.
* **Vigenere Cipher:** Çoklu alfabe (Polyalphabetic) şifreleme.
* **Affine Cipher:** Doğrusal fonksiyon $E(x) = (ax + b) \mod 26$.
* **Rail Fence Cipher:** Zikzak (Transposition) şifreleme.
* **Substitution Cipher:** Basit yerine koyma.
* **Columnar Cipher:** Sütun bazlı yer değiştirme.
