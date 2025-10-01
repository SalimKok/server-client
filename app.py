from flask import Flask, request, jsonify
from flask_cors import CORS
from ciphers import sezar, affine, substitution, vigenere

app = Flask(__name__)
CORS(app)

@app.route("/encrypt", methods=["POST"])
def encrypt_route():
    data = request.get_json(force=True)
    cipher = data.get("cipher")
    key = data.get("key")
    text = data.get("text","")
    try:
        if cipher=="caesar":
            result = sezar.encrypt(text,key)
        elif cipher=="affine":
            result = affine.encrypt(text,key)
        elif cipher=="substitution":
            result = substitution.encrypt(text,key)
        elif cipher=="vigenere":
            result = vigenere.encrypt(text,key)
        else:
            return jsonify({"error":"Bilinmeyen algoritma"}),400
        return jsonify({"ciphertext": result})
    except ValueError as e:  
        return jsonify({"error": str(e)}), 400
    except Exception as e:   
        return jsonify({"error": "Bilinmeyen hata: "+str(e)}), 400

@app.route("/decrypt", methods=["POST"])
def decrypt_route():
    data = request.get_json(force=True)
    cipher = data.get("cipher")
    key = data.get("key")
    text = data.get("text","")
    try:
        if cipher=="caesar":
            result = sezar.decrypt(text,key)
        elif cipher=="affine":
            result = affine.decrypt(text,key)
        elif cipher=="substitution":
            result = substitution.decrypt(text,key)
        elif cipher=="vigenere":
            result = vigenere.decrypt(text,key)
        else:
            return jsonify({"error":"Bilinmeyen algoritma"}),400
        return jsonify({"plaintext": result})
    except Exception as e:
        return jsonify({"error": str(e)}),400
    except Exception as e:   
        return jsonify({"error": "Bilinmeyen hata: "+str(e)}), 400

if __name__=="__main__":
    app.run(debug=True)
