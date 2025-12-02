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
      theme: ThemeData(primarySwatch: Colors.blue),
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
  // Algoritma Listesi
  final List<CipherBase> algorithms = [
    CaesarCipher(),
    VigenereCipher(),
    AffineCipher(),
    RailFenceCipher(),
    SubstitutionCipher(),
    ColumnarCipher(),
  ];

  CipherBase? selectedAlgorithm;
  final TextEditingController msgController = TextEditingController();
  final TextEditingController keyController = TextEditingController();

  String encryptedText = "";
  String serverResponse = "";

  @override
  void initState() {
    super.initState();
    selectedAlgorithm = algorithms[0]; // Varsayılan seçim
  }

  // Mesajı şifrele
  void performEncryption() {
    if (selectedAlgorithm == null) return;
    setState(() {
      encryptedText = selectedAlgorithm!.encrypt(msgController.text, keyController.text);
    });
  }

  // Server'a gönder (GÜNCELLENMİŞ VERSİYON)
  Future<void> sendToServer() async {
    if (encryptedText.isEmpty) return;

    // Emülatör: 10.0.2.2, Gerçek Cihaz: Bilgisayarının IPv4 adresi
    const String apiUrl = "http://10.0.2.2:5000/decrypt";

    setState(() {
      serverResponse = "Server yanıtı bekleniyor... (Lütfen Server terminaline anahtarı girin)";
    });

    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "method": selectedAlgorithm!.id,
          "ciphertext": encryptedText,
          // DİKKAT: Artık 'key' göndermiyoruz!
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          serverResponse = "BAŞARILI! Server Çözdü: ${data['original_message']}";
        });
      } else {
        setState(() {
          serverResponse = "Hata: ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        serverResponse = "Bağlantı Hatası: $e";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(

      appBar: AppBar(title: const Text("Güvenli Mesajlaşma")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              DropdownButton<CipherBase>(
                value: selectedAlgorithm,
                items: algorithms.map((e) {
                  return DropdownMenuItem(value: e, child: Text(e.name));
                }).toList(),
                onChanged: (val) {
                  setState(() => selectedAlgorithm = val);
                },
              ),
              const SizedBox(height: 10),
              TextField(
                controller: msgController,
                decoration: const InputDecoration(labelText: "Mesajınız", border: OutlineInputBorder()),
              ),
              const SizedBox(height: 10),
              TextField(
                controller: keyController,
                decoration: const InputDecoration(labelText: "Anahtar (Key)", border: OutlineInputBorder()),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: performEncryption,
                child: const Text("Mesajı Şifrele"),
              ),
              const SizedBox(height: 20),
              Text("Şifreli Mesaj:", style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey[700])),
              Container(
                padding: const EdgeInsets.all(10),
                color: Colors.grey[200],
                child: Text(encryptedText, style: const TextStyle(fontFamily: 'Courier')),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                icon: const Icon(Icons.send),
                label: const Text("Server'a Gönder"),
                style: ElevatedButton.styleFrom(backgroundColor: Colors.green, foregroundColor: Colors.white),
                onPressed: encryptedText.isNotEmpty ? sendToServer : null,
              ),
              const SizedBox(height: 20),
              if (serverResponse.isNotEmpty)
                Card(
                  color: Colors.green[50],
                  child: Padding(
                    padding: const EdgeInsets.all(10.0),
                    child: Text(serverResponse, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.green)),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}