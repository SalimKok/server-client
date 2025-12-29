import 'dart:convert';
import 'dart:math';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'ciphers/cipher_base.dart';
import 'ciphers/aes_cipher.dart';
import 'ciphers/des_cipher.dart';
import 'ciphers/caesar.dart';
import 'ciphers/vigenere.dart';
import 'ciphers/affine.dart';
import 'ciphers/rail_fence.dart';
import 'ciphers/substitution.dart';
import 'ciphers/columnar.dart';
import 'ciphers/rsa_cipher.dart';
import 'ciphers/hill.dart';
import 'ciphers/playfair.dart';
import 'ciphers/polybius.dart';
import 'ciphers/vernam.dart';
import 'ciphers/route.dart';
import 'package:elliptic/elliptic.dart' as elliptic;
import 'ciphers/ecc_algo.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'TERMINAL_CRYPT_V2',
      theme: ThemeData(
        brightness: Brightness.dark,
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFF000000),
        fontFamily: 'monospace',
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00FF41),
          secondary: Color(0xFF00F3FF),
          surface: Color(0xFF0D0D0D),
        ),
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
    AesCipherAlgo(), DesCipherAlgo(),
    EccCipherAlgo(),
    CaesarCipher(), VigenereCipher(),
    AffineCipher(), RailFenceCipher(), SubstitutionCipher(), ColumnarCipher(),
    HillCipher(), PlayfairCipher(), PolybiusCipher(), VernamCipher(), RouteCipher()
  ];

  CipherBase? selectedAlgorithm;
  final TextEditingController msgController = TextEditingController();
  final TextEditingController keyController = TextEditingController();

  String encryptedText = "";
  String serverResponse = "";
  String decryptedServerMsg = "";
  double encryptionDuration = 0.0;
  bool _isSending = false;
  bool _isSuccess = false;

  final String baseUrl = "http://10.0.2.2:5000";
  String? serverPublicKey;

  @override
  void initState() {
    super.initState();
    selectedAlgorithm = algorithms[0];
    fetchPublicKey();
  }

  void generateRandomKey() {
    setState(() {
      if (selectedAlgorithm is AesCipherAlgo) {
        keyController.text = AesCipherAlgo.generateRandomKey();
      } else if (selectedAlgorithm is DesCipherAlgo) {
        keyController.text = DesCipherAlgo.generateRandomKey();
      } else if (selectedAlgorithm is EccCipherAlgo) {

        final ec = elliptic.getP256();
        final private = ec.generatePrivateKey();
        keyController.text = private.toHex();
      } else {
        keyController.text = (Random().nextInt(20) + 1).toString();
      }
    });
  }

  Future<void> fetchPublicKey() async {
    try {
      final response = await http.get(Uri.parse("$baseUrl/get_public_key"));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() { serverPublicKey = data['public_key']; });
      }
    } catch (e) {
      setState(() { serverResponse = "SYSTEM_ERROR: CONNECTION_REFUSED"; });
    }
  }

  void performEncryption() {
    if (selectedAlgorithm == null || msgController.text.isEmpty || keyController.text.isEmpty) return;
    FocusScope.of(context).unfocus();

    try {
      final stopwatch = Stopwatch()..start();
      String result = selectedAlgorithm!.encrypt(msgController.text, keyController.text);
      stopwatch.stop();

      setState(() {
        encryptedText = result;
        encryptionDuration = stopwatch.elapsedMicroseconds / 1000.0;
        serverResponse = "";
        decryptedServerMsg = "";
        _isSuccess = false;
      });
    } catch (e) {
      setState(() {
        encryptedText = "ERROR: ${e.toString()}";
        _isSuccess = false;
      });
    }
  }

  Future<void> pickAndSendFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();
    if (result != null) {
      File file = File(result.files.single.path!);
      List<int> fileBytes = await file.readAsBytes();
      String fileName = result.files.single.name;
      setState(() { _isSending = true; serverResponse = "UPLOADING_ENCRYPTED_STREAM..."; });
      try {
        String base64File = base64Encode(fileBytes);
        String encryptedFileContent = selectedAlgorithm!.encrypt(base64File, keyController.text);
        final response = await http.post(Uri.parse("$baseUrl/encrypt_file"),
          headers: {"Content-Type": "application/json"},
          body: jsonEncode({"ciphertext": encryptedFileContent, "fileName": fileName, "method": selectedAlgorithm!.id}),
        );
        if (response.statusCode == 200) {
          setState(() { serverResponse = "DATA_TRANSFER_COMPLETE: $fileName"; _isSuccess = true; });
        }
      } catch (e) {
        setState(() { serverResponse = "UPLD_ERROR: $e"; _isSuccess = false; });
      } finally {
        setState(() { _isSending = false; });
      }
    }
  }


  Future<void> sendToServer() async {
    if (encryptedText.isEmpty) return;

    setState(() { _isSending = true; serverResponse = "CONNECTING_TO_CORE..."; });

    try {
      if (selectedAlgorithm is EccCipherAlgo) {

        final ec = elliptic.getP256();
        final private = elliptic.PrivateKey.fromHex(ec, keyController.text);
        final publicHex = private.publicKey.toHex();

        final response = await http.post(Uri.parse("$baseUrl/verify_signature"),
          headers: {"Content-Type": "application/json"},
          body: jsonEncode({
            "message": msgController.text,
            "signature": encryptedText,
            "public_key": publicHex,
            "method": "ecc"
          }),
        );

        final responseData = jsonDecode(response.body);
        if (response.statusCode == 200) {
          setState(() {
            serverResponse = "INTEGRITY_CHECK: ${responseData['status']}";
            _isSuccess = responseData['valid'] == true;
          });
        } else {
          throw Exception(responseData['error']);
        }

      } else {

        bool needsHandshake = (selectedAlgorithm is AesCipherAlgo || selectedAlgorithm is DesCipherAlgo);

        if (needsHandshake) {
          if (serverPublicKey == null) await fetchPublicKey();
          String sessionKey = keyController.text;
          String encryptedSessionKey = RsaCipher().encrypt(sessionKey, serverPublicKey!);

          await http.post(Uri.parse("$baseUrl/handshake"),
            headers: {"Content-Type": "application/json"},
            body: jsonEncode({"encrypted_session_key": encryptedSessionKey, "method": selectedAlgorithm!.id}),
          );
        }

        final msgResponse = await http.post(Uri.parse("$baseUrl/decrypt_message"),
          headers: {"Content-Type": "application/json"},
          body: jsonEncode({"ciphertext": encryptedText, "method": selectedAlgorithm!.id}),
        );

        final responseData = jsonDecode(msgResponse.body);

        if (msgResponse.statusCode == 200) {
          String serverCiphertext = responseData['server_response'] ?? "";
          String plainResponse = "";

          if (selectedAlgorithm is AesCipherAlgo) {
            plainResponse = (selectedAlgorithm as AesCipherAlgo).decrypt(serverCiphertext, keyController.text);
          } else if (selectedAlgorithm is DesCipherAlgo) {
            plainResponse = (selectedAlgorithm as DesCipherAlgo).decrypt(serverCiphertext, keyController.text);
          } else {
            plainResponse = "RESPONSE_DECRYPTED";
          }

          setState(() {
            serverResponse = "ACCESS_GRANTED: DECRYPTED";
            decryptedServerMsg = plainResponse;
            _isSuccess = true;
          });
        } else {
          throw Exception(responseData['error'] ?? "AUTH_FAILED");
        }
      }

    } catch (e) {
      setState(() { serverResponse = "FATAL_ERROR: $e"; _isSuccess = false; });
    } finally {
      setState(() { _isSending = false; });
    }
  }


  @override
  Widget build(BuildContext context) {
    const neonGreen = Color(0xFF00FF41);
    const cyberBlue = Color(0xFF00F3FF);

    return Scaffold(
      appBar: AppBar(
        title: const Text("> CRYPT_V2",
            style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 2)),
        backgroundColor: Colors.black,
        elevation: 0,
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(1),
          child: Container(color: neonGreen.withOpacity(0.5), height: 1),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [

            Container(
              decoration: BoxDecoration(
                border: Border.all(color: neonGreen.withOpacity(0.3)),
                color: const Color(0xFF0A0A0A),
              ),
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  DropdownButtonFormField<CipherBase>(
                    isExpanded: true,
                    value: selectedAlgorithm,
                    dropdownColor: Colors.black,
                    decoration: const InputDecoration(
                      labelText: "SELECTED_ALGO",
                      labelStyle: TextStyle(color: neonGreen),
                      prefixIcon: Icon(Icons.settings_input_component, color: neonGreen),
                    ),
                    items: algorithms.map((e) => DropdownMenuItem(value: e, child: Text(e.name))).toList(),
                    onChanged: (val) => setState(() => selectedAlgorithm = val),
                  ),
                  const SizedBox(height: 15),
                  TextField(
                    controller: msgController,
                    maxLines: 2,
                    style: const TextStyle(color: Colors.white, fontSize: 14),
                    decoration: const InputDecoration(
                      labelText: "PLAINTEXT_BUFFER",
                      labelStyle: TextStyle(color: neonGreen),
                      prefixIcon: Icon(Icons.code, color: neonGreen),
                    ),
                  ),
                  const SizedBox(height: 15),
                  TextField(
                    controller: keyController,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      labelText: "ACCESS_KEY",
                      labelStyle: const TextStyle(color: neonGreen),
                      prefixIcon: const Icon(Icons.vpn_key_rounded, color: neonGreen),
                      suffixIcon: IconButton(
                        icon: const Icon(Icons.casino, color: neonGreen),
                        onPressed: generateRandomKey,
                      ),
                    ),
                  ),
                  const SizedBox(height: 25),
                  OutlinedButton.icon(
                    onPressed: performEncryption,
                    icon: const Icon(Icons.lock_open_rounded),
                    label: const Text("EXECUTE_ENCRYPTION"),
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: neonGreen),
                      foregroundColor: neonGreen,
                      minimumSize: const Size(double.infinity, 50),
                    ),
                  ),
                  const SizedBox(height: 10),
                  OutlinedButton.icon(
                    onPressed: _isSending ? null : pickAndSendFile,
                    icon: const Icon(Icons.file_upload_outlined),
                    label: const Text("SEND_file"),
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: cyberBlue),
                      foregroundColor: cyberBlue,
                      minimumSize: const Size(double.infinity, 50),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 25),

            // Analiz Bölümü
            if (encryptedText.isNotEmpty) ...[
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(">> CIPHERTEXT_OUTPUT",
                      style: TextStyle(fontWeight: FontWeight.bold, color: neonGreen, fontSize: 12)),
                  Text("PROC_TIME: ${encryptionDuration.toStringAsFixed(3)}ms",
                      style: const TextStyle(color: Colors.orange, fontSize: 13)),
                ],
              ),
              const SizedBox(height: 10),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.black,
                  border: Border.all(color: Colors.orange.withOpacity(0.5)),
                ),
                child: SelectableText(
                  encryptedText,
                  style: const TextStyle(color: Color(0xFFE0E0E0), fontSize: 13),
                ),
              ),
              const SizedBox(height: 15),
              ElevatedButton.icon(
                onPressed: _isSending ? null : sendToServer,
                icon: _isSending
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))
                    : const Icon(Icons.cloud_sync_rounded),
                label: Text(_isSending ? "UPLOADING..." : "SEND_TO_SERVER"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: neonGreen,
                  foregroundColor: Colors.black,
                  shape: const RoundedRectangleBorder(),
                ),
              ),
            ],

            const SizedBox(height: 25),

            // Sistem Logları
            if (serverResponse.isNotEmpty)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  border: Border.all(color: _isSuccess ? neonGreen : Colors.red),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text("SYSLOG: $serverResponse",
                        style: TextStyle(fontWeight: FontWeight.bold, color: _isSuccess ? neonGreen : Colors.red)),
                    if (decryptedServerMsg.isNotEmpty) ...[
                      const Divider(color: neonGreen),
                      const Text("DECRYPTED_PAYLOAD:", style: TextStyle(fontSize: 10, color: Colors.grey)),
                      const SizedBox(height: 5),
                      Text(decryptedServerMsg, style: const TextStyle(fontSize: 14, color: Colors.white)),
                    ]
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}