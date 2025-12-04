import 'dart:convert';
import 'dart:math';
import 'package:dart_des/dart_des.dart';
import 'cipher_base.dart';

class DesCipherAlgo implements CipherBase {
  @override
  String get name => "DES (Eski Standart)";
  @override
  String get id => "des";

  @override
  String encrypt(String text, String keyStr) {
    if (keyStr.isEmpty) return text;

    String paddedKey = keyStr.padRight(8, ' ');
    if (paddedKey.length > 8) {
      paddedKey = paddedKey.substring(0, 8);
    }
    List<int> keyBytes = utf8.encode(paddedKey);

    final random = Random.secure();
    List<int> ivBytes = List<int>.generate(8, (_) => random.nextInt(256));

    DES desCBC = DES(
      key: keyBytes,
      mode: DESMode.CBC,
      iv: ivBytes,
      paddingType: DESPaddingType.PKCS7,
    );

    List<int> messageBytes = utf8.encode(text);
    List<int> encryptedBytes = desCBC.encrypt(messageBytes);

    List<int> combined = ivBytes + encryptedBytes;

    return base64.encode(combined);
  }
}