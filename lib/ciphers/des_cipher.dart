import 'dart:convert';
import 'dart:math';
import 'package:dart_des/dart_des.dart';
import 'cipher_base.dart';

class DesCipherAlgo implements CipherBase {
  @override
  String get name => "DES (Eski Standart)";
  @override
  String get id => "des";

  // Rastgele 8 karakterlik anahtar üretir
  static String generateRandomKey() {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    return String.fromCharCodes(Iterable.generate(8, (_) => chars.codeUnitAt(Random.secure().nextInt(chars.length))));
  }

  @override
  String encrypt(String text, String keyStr) {
    if (keyStr.isEmpty) return text;
    List<int> keyBytes = utf8.encode(keyStr.padRight(8, ' ').substring(0, 8));
    List<int> ivBytes = List<int>.generate(8, (_) => Random.secure().nextInt(256));

    DES des = DES(key: keyBytes, mode: DESMode.CBC, iv: ivBytes, paddingType: DESPaddingType.PKCS7);
    List<int> encrypted = des.encrypt(utf8.encode(text));
    return base64.encode(ivBytes + encrypted);
  }

  // Sunucu yanıtını çözmek için
  String decrypt(String base64Ciphertext, String keyStr) {
    List<int> combined = base64.decode(base64Ciphertext);
    List<int> keyBytes = utf8.encode(keyStr.padRight(8, ' ').substring(0, 8));
    List<int> iv = combined.sublist(0, 8);
    List<int> encryptedData = combined.sublist(8);

    DES des = DES(key: keyBytes, mode: DESMode.CBC, iv: iv, paddingType: DESPaddingType.PKCS7);
    return utf8.decode(des.decrypt(encryptedData));
  }
}