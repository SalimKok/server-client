import 'dart:convert';
import 'package:elliptic/elliptic.dart';
import 'package:ecdsa/ecdsa.dart';
import 'package:crypto/crypto.dart' as crypto;
import 'cipher_base.dart';

class EccCipherAlgo implements CipherBase {
  @override
  String get name => "ECC (Dijital İmza)";
  @override
  String get id => "ecc";

  @override
  String encrypt(String text, String privateKeyHex) {
    try {
      final ec = getP256();
      final privateKey = PrivateKey.fromHex(ec, privateKeyHex);

      final messageBytes = utf8.encode(text);

      final digest = crypto.sha256.convert(messageBytes);

      final sig = signature(privateKey, digest.bytes);


      return base64.encode(sig.toASN1());
    } catch (e) {
      return "Hata: $e";
    }
  }

  String decrypt(String signatureBase64, String publicKeyHex) {

    try {
      final ec = getP256();

      final publicKey = PublicKey.fromHex(ec, publicKeyHex);

      final sigBytes = base64.decode(signatureBase64);
      final sig = Signature.fromASN1(sigBytes);

      return "ECC Doğrulama işlemi için Orijinal Mesaj gereklidir.";
    } catch (e) {
      return "Doğrulama Hatası";
    }
  }

  bool verifyProperly(String message, String signatureBase64, String publicKeyHex) {
    final ec = getP256();
    final publicKey = PublicKey.fromHex(ec, publicKeyHex);
    final sigBytes = base64.decode(signatureBase64);
    final sig = Signature.fromASN1(sigBytes);
    final hash = List<int>.from(utf8.encode(message));

    return verify(publicKey, hash, sig);
  }
}