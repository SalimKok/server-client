import 'cipher_base.dart';

class PlayfairCipher implements CipherBase {
  @override
  String get name => "Playfair";
  @override
  String get id => "playfair";

  @override
  String encrypt(String text, String key) {
    String preparedKey = _generateKey(key);
    String preparedText = _prepareText(text);

    List<List<String>> matrix = _createMatrix(preparedKey);
    StringBuffer result = StringBuffer();

    for (int i = 0; i < preparedText.length; i += 2) {
      String a = preparedText[i];
      String b = preparedText[i + 1];
      var posA = _findPosition(matrix, a);
      var posB = _findPosition(matrix, b);

      if (posA[0] == posB[0]) { // Aynı satır
        result.write(matrix[posA[0]][(posA[1] + 1) % 5]);
        result.write(matrix[posB[0]][(posB[1] + 1) % 5]);
      } else if (posA[1] == posB[1]) { // Aynı sütun
        result.write(matrix[(posA[0] + 1) % 5][posA[1]]);
        result.write(matrix[(posB[0] + 1) % 5][posB[1]]);
      } else { // Dikdörtgen
        result.write(matrix[posA[0]][posB[1]]);
        result.write(matrix[posB[0]][posA[1]]);
      }
    }
    return result.toString();
  }

  String _generateKey(String key) {
    String alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    String combined = (key.toUpperCase() + alphabet).replaceAll('J', 'I');
    return String.fromCharCodes(combined.runes.toSet().toList());
  }

  String _prepareText(String text) {
    String cleanText = text.toUpperCase().replaceAll(RegExp(r'[^A-Z]'), '').replaceAll('J', 'I');
    StringBuffer sb = StringBuffer();
    for (int i = 0; i < cleanText.length; i++) {
      sb.write(cleanText[i]);
      if (i + 1 < cleanText.length) {
        if (cleanText[i] == cleanText[i + 1]) sb.write('X');
      }
    }
    if (sb.length % 2 != 0) sb.write('X');
    return sb.toString();
  }

  List<int> _findPosition(List<List<String>> matrix, String char) {
    for (int r = 0; r < 5; r++) {
      for (int c = 0; c < 5; c++) {
        if (matrix[r][c] == char) return [r, c];
      }
    }
    return [0, 0];
  }

  List<List<String>> _createMatrix(String key) {
    List<List<String>> matrix = List.generate(5, (_) => List.filled(5, ""));
    for (int i = 0; i < 25; i++) {
      matrix[i ~/ 5][i % 5] = key[i];
    }
    return matrix;
  }
}