import 'package:encrypt/encrypt.dart' as enc;
import 'dart:convert';
import 'dart:math';
import 'cipher_base.dart';

class AesCipherAlgo implements CipherBase {
  @override
  String get name => "AES (Modern)";
  @override
  String get id => "aes";

  // Rastgele 32 karakterlik (256-bit) anahtar üretir
  static String generateRandomKey() {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    return String.fromCharCodes(Iterable.generate(32, (_) => chars.codeUnitAt(Random.secure().nextInt(chars.length))));
  }

  @override
  String encrypt(String text, String keyStr) {
    if (keyStr.isEmpty) return text;
    final key = enc.Key.fromUtf8(keyStr.padRight(32, ' ').substring(0, 32));
    final iv = enc.IV.fromLength(16);
    final encrypter = enc.Encrypter(enc.AES(key, mode: enc.AESMode.cbc));

    final encrypted = encrypter.encrypt(text, iv: iv);
    final combined = iv.bytes + encrypted.bytes;
    return base64.encode(combined);
  }

  // Sunucudan gelen mesajı çözmek için gerekli
  String decrypt(String base64Ciphertext, String keyStr) {
    final key = enc.Key.fromUtf8(keyStr.padRight(32, ' ').substring(0, 32));
    final combined = base64.decode(base64Ciphertext);
    final iv = enc.IV(combined.sublist(0, 16));
    final ciphertextBytes = combined.sublist(16);

    final encrypter = enc.Encrypter(enc.AES(key, mode: enc.AESMode.cbc));
    return encrypter.decrypt(enc.Encrypted(ciphertextBytes), iv: iv);
  }
}