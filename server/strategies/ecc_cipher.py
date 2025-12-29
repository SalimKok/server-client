
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

class ECCCipher:
    def __init__(self):
        
        self.curve = ec.SECP256R1()

    def sign(self, message: str, pem_private_key: str) -> str:
    
        try:
            private_key = serialization.load_pem_private_key(
                pem_private_key.encode('utf-8'),
                password=None
            )
            data = message.encode('utf-8')
            signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
            return base64.b64encode(signature).decode('utf-8')
        except Exception as e:
            return f"Error: {str(e)}"

    def verify_client_hex(self, message: str, signature_b64: str, public_key_hex: str) -> bool:
        """
        Dart istemcisinden gelen Hex formatındaki Public Key ile doğrulama yapar.
        """
        try:
            public_key = ec.EllipticCurvePublicKey.from_encoded_point(
                self.curve, 
                bytes.fromhex(public_key_hex)
            )

            signature = base64.b64decode(signature_b64)
            data = message.encode('utf-8')

            public_key.verify(
                signature,
                data,
                ec.ECDSA(hashes.SHA256())
            )
            return True 
        except InvalidSignature:
            print("ECC: İmza geçersiz!")
            return False
        except Exception as e:
            print(f"ECC Hatası: {str(e)}")
            return False