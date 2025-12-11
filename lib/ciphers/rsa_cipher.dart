import 'package:encrypt/encrypt.dart' as enc;
import 'package:pointycastle/asymmetric/api.dart';
import 'cipher_base.dart';

class RsaCipher implements CipherBase {
  @override
  String get name => "RSA (Key Exchange)";
  @override
  String get id => "rsa";

  @override
  String encrypt(String text, String keyStr) {
    try {
      final parser = enc.RSAKeyParser();
      final RSAPublicKey publicKey = parser.parse(keyStr) as RSAPublicKey;

      final encrypter = enc.Encrypter(
        enc.RSA(publicKey: publicKey, encoding: enc.RSAEncoding.OAEP),
      );

      final encrypted = encrypter.encrypt(text);

      return encrypted.base64;

    } catch (e) {
      print("RSA Şifreleme Hatası: $e");
      return "";
    }
  }
}