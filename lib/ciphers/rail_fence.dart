import 'cipher_base.dart';

class RailFenceCipher implements CipherBase {
  @override
  String get name => "Rail Fence (Zikzak)";
  @override
  String get id => "rail_fence";

  @override
  String encrypt(String text, String key) {
    int? rails = int.tryParse(key);
    if (rails == null || rails < 2) return "Anahtar 2 veya daha büyük bir sayı olmalı.";

    List<StringBuffer> fences = List.generate(rails, (_) => StringBuffer());
    int rail = 0;
    bool down = false;

    for (int i = 0; i < text.length; i++) {
      fences[rail].write(text[i]);
      if (rail == 0 || rail == rails - 1) down = !down;
      rail += down ? 1 : -1;
    }
    return fences.map((e) => e.toString()).join();
  }
}