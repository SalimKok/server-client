import 'cipher_base.dart';

class SubstitutionCipher implements CipherBase {
  @override
  String get name => "Substitution (Yerine Koyma)";
  @override
  String get id => "substitution";

  @override
  String encrypt(String text, String key) {
    if (key.length != 26) return "Anahtar 26 harfli bir alfabe olmalı.";

    String std = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    String upperKey = key.toUpperCase();
    StringBuffer result = StringBuffer();

    for (int i = 0; i < text.length; i++) {
      String char = text[i].toUpperCase();
      int index = std.indexOf(char);
      if (index != -1) {
        String enc = upperKey[index];
        result.write(text[i] == char ? enc : enc.toLowerCase());
      } else {
        result.write(text[i]);
      }
    }
    return result.toString();
  }
}