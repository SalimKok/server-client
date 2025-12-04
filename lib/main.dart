import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'ciphers/cipher_base.dart';
import 'ciphers/caesar.dart';
import 'ciphers/vigenere.dart';
import 'ciphers/affine.dart';
import 'ciphers/rail_fence.dart';
import 'ciphers/substitution.dart';
import 'ciphers/columnar.dart';
import 'ciphers/aes_cipher.dart';
import 'ciphers/des_cipher.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Crypto Client',
      // MATERIAL 3 TEMA AYARLARI
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.indigo, // Ana renk: Indigo mavisi
          brightness: Brightness.light,
        ),
        // AppBar teması
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 2,
          titleTextStyle: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
        ),
        // Input (TextField) genel teması
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.grey.shade100,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide.none,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: Colors.grey.shade300),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: Colors.indigo, width: 2),
          ),
          labelStyle: TextStyle(color: Colors.grey.shade700),
          prefixIconColor: Colors.indigo.shade400,
        ),
        // Buton genel teması
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            elevation: 3,
          ),
        ),
        // cardTheme kısmını buradan kaldırdık, aşağıda manuel vereceğiz.
      ),
      home: const CryptoHome(),
    );
  }
}

class CryptoHome extends StatefulWidget {
  const CryptoHome({super.key});

  @override
  State<CryptoHome> createState() => _CryptoHomeState();
}

class _CryptoHomeState extends State<CryptoHome> {
  final List<CipherBase> algorithms = [
    CaesarCipher(),
    VigenereCipher(),
    AffineCipher(),
    RailFenceCipher(),
    SubstitutionCipher(),
    ColumnarCipher(),
    AesCipherAlgo(),
    DesCipherAlgo(),
  ];

  CipherBase? selectedAlgorithm;
  final TextEditingController msgController = TextEditingController();
  final TextEditingController keyController = TextEditingController();

  String encryptedText = "";
  String serverResponse = "";
  // UI Durumları
  bool _isSending = false;
  bool _isSuccess = false;

  @override
  void initState() {
    super.initState();
    selectedAlgorithm = algorithms[0];
  }

  void performEncryption() {
    if (selectedAlgorithm == null || msgController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Lütfen bir mesaj girin.")));
      return;
    }
    FocusScope.of(context).unfocus();
    setState(() {
      encryptedText = selectedAlgorithm!.encrypt(msgController.text, keyController.text);
      serverResponse = "";
      _isSuccess = false;
    });
  }

  Future<void> sendToServer() async {
    if (encryptedText.isEmpty) return;
    FocusScope.of(context).unfocus();

    const String apiUrl = "http://10.0.2.2:5000/decrypt";

    setState(() {
      _isSending = true;
      serverResponse = "Server yanıtı bekleniyor...\n(Lütfen Server terminaline anahtarı girin)";
      _isSuccess = false;
    });

    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "method": selectedAlgorithm!.id,
          "ciphertext": encryptedText,
        }),
      );

      if (response.statusCode == 200) {
        setState(() {
          serverResponse = "BAŞARILI!\nServer mesajı çözdü ve konsola yazdı.";
          _isSuccess = true;
        });
      } else {
        setState(() {
          serverResponse = "Hata: ${response.statusCode}\nServer isteği reddetti.";
          _isSuccess = false;
        });
      }
    } catch (e) {
      setState(() {
        serverResponse = "Bağlantı Hatası:\n$e\n(Server'ın çalıştığından ve IP'nin doğru olduğundan emin olun)";
        _isSuccess = false;
      });
    } finally {
      setState(() {
        _isSending = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade50,
      appBar: AppBar(
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: const [
            Icon(Icons.security_rounded),
            SizedBox(width: 10),
            Text("Güvenli Mesajlaşma", style: TextStyle(color: Colors.blueAccent),),
          ],
        ),
        backgroundColor: Colors.indigo.shade50,
        foregroundColor: Colors.indigo.shade900,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // --- BÖLÜM 1: GİRİŞLER ---
            Card(
              // TEMA yerine buraya manuel yazdık:
              elevation: 4,
              color: Colors.white,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              // ------------------------------------
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Text("Şifreleme Ayarları", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.indigo.shade800)),
                    const SizedBox(height: 15),
                    InputDecorator(
                      decoration: const InputDecoration(
                        labelText: 'Algoritma Seçin',
                        prefixIcon: Icon(Icons.lock_open_rounded),
                        contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      ),
                      child: DropdownButtonHideUnderline(
                        child: DropdownButton<CipherBase>(
                          value: selectedAlgorithm,
                          isExpanded: true,
                          icon: const Icon(Icons.arrow_drop_down_circle_rounded),
                          items: algorithms.map((e) {
                            return DropdownMenuItem(value: e, child: Text(e.name));
                          }).toList(),
                          onChanged: (val) => setState(() => selectedAlgorithm = val),
                        ),
                      ),
                    ),
                    const SizedBox(height: 15),
                    TextField(
                      controller: msgController,
                      decoration: const InputDecoration(
                        labelText: "Mesajınız",
                        hintText: "Şifrelenecek metni girin",
                        prefixIcon: Icon(Icons.message_rounded),
                      ),
                      maxLines: 3,
                      minLines: 1,
                    ),
                    const SizedBox(height: 15),
                    TextField(
                      controller: keyController,
                      decoration: const InputDecoration(
                        labelText: "Anahtar (Key)",
                        hintText: "Örn: 3, test, sifre123...",
                        prefixIcon: Icon(Icons.vpn_key_rounded),
                      ),
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton.icon(
                      onPressed: performEncryption,
                      style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.indigo,
                          foregroundColor: Colors.white
                      ),
                      icon: const Icon(Icons.enhanced_encryption_rounded),
                      label: const Text("MESAJI ŞİFRELE"),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 25),

            // --- BÖLÜM 2: ÇIKTI VE GÖNDERİM ---
            if (encryptedText.isNotEmpty) ...[
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8.0),
                child: Text("Şifreli Çıktı (Ciphertext):", style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey[700])),
              ),
              const SizedBox(height: 8),
              Card(
                // Şifreli metin kartı (Koyu Renk)
                elevation: 4,
                color: Colors.grey.shade800,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                // -----------------------------
                child: Stack(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: SelectableText(
                        encryptedText,
                        style: const TextStyle(
                            fontFamily: 'Courier',
                            color: Colors.greenAccent,
                            fontSize: 15,
                            fontWeight: FontWeight.w600
                        ),
                      ),
                    ),
                    Positioned(
                        right: 0,
                        top: 0,
                        child: IconButton(
                          icon: Icon(Icons.copy, color: Colors.grey.shade400, size: 20),
                          onPressed: () {
                            ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Metin panoya kopyalandı!"), duration: Duration(milliseconds: 500)));
                          },
                        )
                    )
                  ],
                ),
              ),
              const SizedBox(height: 20),
              SizedBox(
                height: 55,
                child: ElevatedButton.icon(
                  icon: _isSending
                      ? const SizedBox(width: 24, height: 24, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : const Icon(Icons.send_rounded),
                  label: Text(_isSending ? "GÖNDERİLİYOR..." : "SERVER'A GÖNDER"),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.teal,
                    foregroundColor: Colors.white,
                  ),
                  onPressed: _isSending ? null : sendToServer,
                ),
              ),
            ],

            const SizedBox(height: 25),

            // --- BÖLÜM 3: SERVER YANITI ---
            if (serverResponse.isNotEmpty)
              FadeTransition(
                opacity: const AlwaysStoppedAnimation(1),
                child: Card(
                  // Yanıt Kartı (Duruma göre renkli)
                  elevation: 4,
                  color: _isSuccess ? Colors.green.shade50 : Colors.orange.shade50,
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                      side: BorderSide(
                          color: _isSuccess ? Colors.green.shade200 : Colors.orange.shade200,
                          width: 1
                      )
                  ),
                  // ------------------------------
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(
                          _isSuccess ? Icons.check_circle_rounded :
                          (_isSending ? Icons.hourglass_top_rounded : Icons.error_outline_rounded),
                          color: _isSuccess ? Colors.green : Colors.orange.shade800,
                          size: 32,
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Text(
                            serverResponse,
                            style: TextStyle(
                                fontSize: 15,
                                fontWeight: FontWeight.w600,
                                color: _isSuccess ? Colors.green.shade900 : Colors.deepOrange.shade900
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            const SizedBox(height: 50),
          ],
        ),
      ),
    );
  }
}