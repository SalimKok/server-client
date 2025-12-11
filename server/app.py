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


@app.route('/decrypt_message', methods=['POST'])
def decrypt_message():
    data = request.json
    
    method = data.get('method')
    ciphertext = data.get('ciphertext')

    if not all([method, ciphertext]):
        return jsonify({"error": "Eksik veri gönderildi."}), 400
    
    cipher_strategy = CIPHER_MAP.get(method)
    
    if not cipher_strategy:
        return jsonify({"error": "Geçersiz şifreleme yöntemi."}), 400
        
    try:
        print(f"\n[!] YENİ MESAJ GELDİ ({method})")
        print(f"[!] Şifreli Metin: {ciphertext}")
        
        server_side_key = None

        if method in ['aes', 'des']:
            server_side_key = CURRENT_SESSION["symmetric_key"]
            if not server_side_key:
                return jsonify({"error": "AES/DES için önce /handshake yapılmalı!"}), 400
            print(f"[otomatik] RSA Handshake ile alınan anahtar kullanılıyor: {server_side_key}")

        else:
            print("[?] Mesajı çözmek için anahtarı girin (Server Konsolu):")
            server_side_key = input("Anahtar: ") 

        plaintext = cipher_strategy.decrypt(ciphertext, server_side_key)
        
        print(f"✅️ Mesaj çözüldü: {plaintext}\n")

        return jsonify({
            "success": True,
            "method": method,
            "original_message": plaintext
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)