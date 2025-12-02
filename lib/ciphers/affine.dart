import 'cipher_base.dart';

class AffineCipher implements CipherBase {
  @override
  String get name => "Affine (Doğrusal)";
  @override
  String get id => "affine";

  int gcd(int a, int b) => b == 0 ? a : gcd(b, a % b);

  @override
  String encrypt(String text, String key) {
    // Key format: "5,8"
    var parts = key.split(',');
    if (parts.length != 2) return "Anahtar 'a,b' formatında olmalı (Örn: 5,8)";

    int a = int.tryParse(parts[0]) ?? 0;
    int b = int.tryParse(parts[1]) ?? 0;

    if (gcd(a, 26) != 1) return "Hata: 'a' sayısı 26 ile aralarında asal olmalı.";

    StringBuffer result = StringBuffer();
    for (int i = 0; i < text.length; i++) {
      int charCode = text.codeUnitAt(i);
      if (charCode >= 65 && charCode <= 90) {
        result.write(String.fromCharCode(((a * (charCode - 65) + b) % 26) + 65));
      } else if (charCode >= 97 && charCode <= 122) {
        result.write(String.fromCharCode(((a * (charCode - 97) + b) % 26) + 97));
      } else {
        result.write(text[i]);
      }
    }
    return result.toString();
  }
}