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

app = Flask(__name__)
CORS(app)

CIPHER_MAP = {
    'caesar': CaesarCipher(),
    'vigenere': VigenereCipher(),
    'affine': AffineCipher(),
    'rail_fence': RailFenceCipher(),
    'substitution': SubstitutionCipher(),
    'columnar': ColumnarCipher(),
    'aes': AESCipher(),  
    'des': DESCipher(),
}

@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    data = request.json
    
    method = data.get('method')
    ciphertext = data.get('ciphertext')

    if not all([method, ciphertext]):
        return jsonify({"error": "Eksik veri gönderildi (Method veya Ciphertext yok)."}), 400
    
    cipher_strategy = CIPHER_MAP.get(method)
    
    if not cipher_strategy:
        return jsonify({"error": "Geçersiz şifreleme yöntemi."}), 400
        
    try:
        print(f"\n[!] YENİ MESAJ GELDİ ({method})")
        print(f"[!] Şifreli Metin: {ciphertext}")
        print("[?] Mesajı çözmek için anahtarı girin:")
          
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