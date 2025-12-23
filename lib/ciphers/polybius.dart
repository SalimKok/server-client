import 'cipher_base.dart';

class PolybiusCipher implements CipherBase {
  @override
  String get name => "Polybius";
  @override
  String get id => "polybius";

  final Map<String, String> _square = {
    'A': '11', 'B': '12', 'C': '13', 'D': '14', 'E': '15',
    'F': '21', 'G': '22', 'H': '23', 'I': '24', 'K': '24',
    'L': '25', 'M': '31', 'N': '32', 'O': '33', 'P': '34',
    'Q': '35', 'R': '41', 'S': '42', 'T': '43', 'U': '44',
    'V': '45', 'W': '51', 'X': '52', 'Y': '53', 'Z': '54', 'J': '24'
  };

  @override
  String encrypt(String text, String key) {
    return text.toUpperCase().split('').map((char) => _square[char] ?? char).join(' ');
  }
}