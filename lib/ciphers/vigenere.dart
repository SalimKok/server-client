import 'cipher_base.dart';

class VigenereCipher implements CipherBase {
  @override
  String get name => "Vigenere Şifreleme";

  @override
  String get id => "vigenere";

  @override
  String encrypt(String text, String key) {
    if (key.isEmpty) return text;

    StringBuffer result = StringBuffer();
    String upperKey = key.toUpperCase();
    int keyIndex = 0;

    for (int i = 0; i < text.length; i++) {
      int charCode = text.codeUnitAt(i);
      if ((charCode >= 65 && charCode <= 90) || (charCode >= 97 && charCode <= 122)) {
        int shift = upperKey.codeUnitAt(keyIndex % upperKey.length) - 65;
        int base = (charCode >= 65 && charCode <= 90) ? 65 : 97;

        result.write(String.fromCharCode((charCode - base + shift) % 26 + base));
        keyIndex++;
      } else {
        result.write(text[i]);
      }
    }
    return result.toString();
  }
}