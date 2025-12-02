abstract class CipherBase {
  String encrypt(String text, String key);
  String get name; // UI'da göstermek için
  String get id;   // Server'a göndermek için (api key)
}