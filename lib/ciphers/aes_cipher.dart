import 'package:encrypt/encrypt.dart' as enc;
import 'dart:convert';
import 'cipher_base.dart';

class AesCipherAlgo implements CipherBase {
  @override
  String get name => "AES (Modern)";
  @override
  String get id => "aes";

  @override
  String encrypt(String text, String keyStr) {
    if (keyStr.isEmpty) return text;

    String paddedKey = keyStr.padRight(32, ' ').substring(0, 32);
    final key = enc.Key.fromUtf8(paddedKey);

    final iv = enc.IV.fromLength(16);

    final encrypter = enc.Encrypter(enc.AES(key, mode: enc.AESMode.cbc));
    final encrypted = encrypter.encrypt(text, iv: iv);

    final combined = iv.bytes + encrypted.bytes;
    return base64.encode(combined);
  }
}