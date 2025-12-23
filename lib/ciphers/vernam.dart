import 'cipher_base.dart';

class VernamCipher implements CipherBase {
  @override
  String get name => "Vernam";
  @override
  String get id => "vernam";

  @override
  String encrypt(String text, String key) {
    if (key.length < text.length) return "Hata: Anahtar metinden kısa olamaz.";

    text = text.toUpperCase();
    key = key.toUpperCase();
    StringBuffer result = StringBuffer();

    for (int i = 0; i < text.length; i++) {
      int p = text.codeUnitAt(i) - 65;
      int k = key.codeUnitAt(i) - 65;
      result.write(String.fromCharCode(((p + k) % 26) + 65));
    }
    return result.toString();
  }
}