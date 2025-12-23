import 'cipher_base.dart';

class HillCipher implements CipherBase {
  @override
  String get name => "Hill (2x2)";
  @override
  String get id => "hill";

  @override
  String encrypt(String text, String key) {
    // Key format: "3,3,2,5"
    var parts = key.split(',').map(int.parse).toList();
    if (parts.length != 4) return "Anahtar 4 sayıdan oluşmalı (2x2 matris).";

    String cleanText = text.toUpperCase().replaceAll(RegExp(r'[^A-Z]'), '');
    if (cleanText.length % 2 != 0) cleanText += 'X';

    StringBuffer result = StringBuffer();
    for (int i = 0; i < cleanText.length; i += 2) {
      int p1 = cleanText.codeUnitAt(i) - 65;
      int p2 = cleanText.codeUnitAt(i + 1) - 65;

      int c1 = (parts[0] * p1 + parts[1] * p2) % 26;
      int c2 = (parts[2] * p1 + parts[3] * p2) % 26;

      result.write(String.fromCharCode(c1 + 65));
      result.write(String.fromCharCode(c2 + 65));
    }
    return result.toString();
  }
}