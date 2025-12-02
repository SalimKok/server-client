import 'cipher_base.dart';

class CaesarCipher implements CipherBase {
  @override
  String get name => "Sezar Şifreleme";

  @override
  String get id => "caesar";

  @override
  String encrypt(String text, String key) {
    int shift = int.tryParse(key) ?? 0;
    StringBuffer result = StringBuffer();

    for (int i = 0; i < text.length; i++) {
      int charCode = text.codeUnitAt(i);
      if (charCode >= 65 && charCode <= 90) { // Büyük Harf
        result.write(String.fromCharCode((charCode - 65 + shift) % 26 + 65));
      } else if (charCode >= 97 && charCode <= 122) { // Küçük Harf
        result.write(String.fromCharCode((charCode - 97 + shift) % 26 + 97));
      } else {
        result.write(text[i]);
      }
    }
    return result.toString();
  }
}