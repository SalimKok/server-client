import os
import base64
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from strategies.caesar import CaesarCipher
from strategies.vigenere import VigenereCipher
from strategies.affine import AffineCipher
from strategies.rail_fence import RailFenceCipher
from strategies.substitution import SubstitutionCipher
from strategies.columnar import ColumnarCipher
from strategies.aes import AESCipher
from strategies.des import DESCipher
from strategies.rsa import RSACipher as RSAStrategy 
from strategies.hill import HillCipher
from strategies.playfair import PlayfairCipher
from strategies.polybius import PolybiusCipher
from strategies.vernam import VernamCipher
from strategies.route import RouteCipher
from strategies.ecc_cipher import ECCCipher

try:
    from strategies.rsa import RSACipher as RSATool
except ImportError:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    import base64
    class RSATool:
        def __init__(self):
            self.key = RSA.generate(2048)
            self.private_key = self.key
            self.public_key = self.key.publickey()
        def get_public_key_pem(self):
            return self.public_key.export_key()
        def decrypt_session_key(self, encrypted_key_b64):
            try:
                encrypted_bytes = base64.b64decode(encrypted_key_b64)
                cipher_rsa = PKCS1_OAEP.new(self.private_key)
                return cipher_rsa.decrypt(encrypted_bytes).decode('utf-8')
            except Exception as e:
                print(f"RSA Decrypt Error: {e}")
                return None

app = Flask(__name__)
CORS(app)

rsa_handshake_tool = RSATool()

CURRENT_SESSION = {
    "symmetric_key": None
}

CIPHER_MAP = {
    'caesar': CaesarCipher(),
    'vigenere': VigenereCipher(),
    'affine': AffineCipher(),
    'rail_fence': RailFenceCipher(),
    'substitution': SubstitutionCipher(),
    'columnar': ColumnarCipher(),
    'aes': AESCipher(),  
    'des': DESCipher(),
    'rsa': RSAStrategy(), 
    'playfair' : PlayfairCipher(),
    'polybius' : PolybiusCipher(),
    'hill' : HillCipher(),
    'vernam' : VernamCipher(),
    'route' : RouteCipher(),
    'ecc' : ECCCipher(),
}

@app.route('/get_public_key', methods=['GET'])
def get_public_key():
    """İstemciye RSA Public Key gönderir."""
    try:
        pem_key = rsa_handshake_tool.get_public_key_pem()
        return jsonify({
            "success": True,
            "public_key": pem_key.decode('utf-8')
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/handshake', methods=['POST'])
def handshake():
    """İstemciden gelen şifreli AES/DES anahtarını çözer ve kaydeder."""
    data = request.json
    encrypted_key = data.get('encrypted_session_key')

    if not encrypted_key:
        return jsonify({"error": "Şifreli anahtar bulunamadı."}), 400

    decrypted_key = rsa_handshake_tool.decrypt_session_key(encrypted_key)

    if decrypted_key:
        CURRENT_SESSION["symmetric_key"] = decrypted_key
        print(f"\n[HANDSHAKE] ✅ Başarılı! Yeni Oturum Anahtarı Alındı: {decrypted_key}")
        return jsonify({"success": True, "message": "Handshake başarılı."})
    else:
        return jsonify({"success": False, "error": "RSA çözme hatası."}), 400

@app.route('/verify_signature', methods=['POST'])
def verify_signature():
    """ECC İmzası Doğrulama Servisi"""
    try:
        data = request.json
        method = data.get('method')

        if method != 'ecc':
            return jsonify({'error': 'Invalid method'}), 400

        message = data.get('message')       
        signature = data.get('signature')   
        public_key_hex = data.get('public_key')

        if not all([message, signature, public_key_hex]):
            return jsonify({'error': 'Eksik parametreler'}), 400

        print(f"\n[ECC] Doğrulama İsteği Geldi...")
        print(f"Mesaj: {message}")
        print(f"İmza: {signature[:30]}...") 

        ecc_strategy = CIPHER_MAP.get('ecc')
        is_valid = ecc_strategy.verify_client_hex(message, signature, public_key_hex)

        if is_valid:
            print("[ECC] ✅ İMZA GEÇERLİ! Mesaj bütünlüğü doğrulandı.")
            return jsonify({
                'status': 'VERIFIED',
                'valid': True,
                'message': 'İmza doğrulandı. Mesaj güvenilir.'
            }), 200
        else:
            print("[ECC] ❌ İMZA GEÇERSİZ! Güvenlik uyarısı.")
            return jsonify({
                'status': 'FAILED',
                'valid': False,
                'error': 'İmza geçersiz! Mesaj değiştirilmiş olabilir.'
            }), 200

    except Exception as e:
        print(f"[ECC ERROR] {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/decrypt_message', methods=['POST'])
def decrypt_message():
    data = request.json
    method = data.get('method')
    ciphertext = data.get('ciphertext')

    if not all([method, ciphertext]):
        return jsonify({"error": "Eksik veri"}), 400
    
    cipher_strategy = CIPHER_MAP.get(method)
    
    try:
        start_time = time.perf_counter() 

        if method in ['aes', 'des']:
            server_side_key = CURRENT_SESSION["symmetric_key"]
        else:
            server_side_key = data.get('key') or input(f"{method} için anahtar girin: ")

        plaintext = cipher_strategy.decrypt(ciphertext, server_side_key)
      
        print(f"\n[?] İstemciden gelen mesaj çözüldü: {plaintext}")
        response_text = input("İstemciye gönderilecek şifreli cevabı girin: ")

        if hasattr(cipher_strategy, 'encrypt'):
            server_encrypted_response = cipher_strategy.encrypt(response_text, server_side_key)
        else:
            server_encrypted_response = response_text 

        end_time = time.perf_counter()
        process_ms = (end_time - start_time) * 1000

        print(f"\n[INFO] {method.upper()} İşlemi Tamamlandı")
        print(f"[*] Çözülen Metin: {plaintext}")
        print(f"[*] Sunucu İşlem Süresi: {process_ms:.4f} ms")

        return jsonify({
            "success": True,
            "method": method,
            "server_response": server_encrypted_response, 
            "server_duration_ms": process_ms
        })

    except Exception as e:
        print(f"[!] Hata: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/encrypt_file', methods=['POST'])
def encrypt_file():
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext')
        file_name = data.get('fileName')
        method = data.get('method')
        
        cipher_strategy = CIPHER_MAP.get(method)
        server_side_key = CURRENT_SESSION.get("symmetric_key")

        decrypted_payload = cipher_strategy.decrypt(ciphertext, server_side_key)
        
        try:
            file_bytes = base64.b64decode(decrypted_payload.strip())
        except Exception as b64e:
            return jsonify({"success": False, "error": f"Base64 hatası: {str(b64e)}"}), 400

        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        file_path = os.path.join(upload_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(file_bytes)
            
        print(f"\n[FILE_SUCCESS] ✅ {file_name} kaydedildi.")
        return jsonify({"success": True, "message": f"{file_name} başarıyla yüklendi."})
        
    except Exception as e:
        print(f"[ERROR] Dosya işleme hatası: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)