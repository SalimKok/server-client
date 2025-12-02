import 'cipher_base.dart';

class ColumnarCipher implements CipherBase {
  @override
  String get name => "Columnar (Sütunlu)";
  @override
  String get id => "columnar";

  @override
  String encrypt(String text, String key) {
    if (key.isEmpty) return text;

    // 1. Anahtar sıralamasını belirle
    // Örneğin Key: "ZEBRA" -> Harf sırası: 5, 2, 3, 4, 1 (Alfabetik)
    List<int> keyIndices = List.generate(key.length, (index) => index);
    keyIndices.sort((a, b) {
      return key[a].toLowerCase().compareTo(key[b].toLowerCase());
    });

    int colCount = key.length;
    int rowCount = (text.length / colCount).ceil();
    StringBuffer result = StringBuffer();

    // 2. Sütunları, anahtarın alfabetik sırasına göre oku
    for (int i = 0; i < colCount; i++) {
      int currentColumn = keyIndices[i];

      for (int row = 0; row < rowCount; row++) {
        // Matris mantığı: satır * genişlik + sütun
        int charIndex = (row * colCount) + currentColumn;

        if (charIndex < text.length) {
          result.write(text[charIndex]);
        }
      }
    }

    return result.toString();
  }
}