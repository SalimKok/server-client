import 'cipher_base.dart';

class RouteCipher implements CipherBase {
  @override
  String get name => "Route (Sütun Bazlı)";
  @override
  String get id => "route";

  @override
  String encrypt(String text, String key) {
    int? numCols = int.tryParse(key);
    if (numCols == null || numCols <= 0) {
      return "Hata: Anahtar pozitif bir tam sayı (sütun sayısı) olmalıdır.";
    }

    String cleanText = text.replaceAll(' ', '');
    int numRows = (cleanText.length / numCols).ceil();

    List<List<String>> grid = List.generate(
      numRows,
          (_) => List.filled(numCols, 'X'),
    );

    int charIdx = 0;
    for (int r = 0; r < numRows; r++) {
      for (int c = 0; c < numCols; c++) {
        if (charIdx < cleanText.length) {
          grid[r][c] = cleanText[charIdx++];
        }
      }
    }

    StringBuffer result = StringBuffer();
    for (int c = 0; c < numCols; c++) {
      for (int r = 0; r < numRows; r++) {
        result.write(grid[r][c]);
      }
    }

    return result.toString();
  }
}