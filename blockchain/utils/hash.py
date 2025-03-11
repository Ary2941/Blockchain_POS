from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec

def load_public_key(pem_data: str) -> ec.EllipticCurvePublicKey:
    """
    Carrega uma chave pública ECC a partir de uma string PEM.
    """
    try:
        public_key = serialization.load_pem_public_key(pem_data.encode())
        if not isinstance(public_key, ec.EllipticCurvePublicKey):
            raise ValueError("A chave pública fornecida não é uma chave ECC válida.")
        return public_key
    except Exception as e:
        print(f"Erro ao carregar chave pública: {e}")
        return None

def get_public_key_hash(public_key: ec.EllipticCurvePublicKey) -> str:
    """
    Gera o hash SHA-256 da chave pública ECC para comparação.
    """
    if public_key is None:
        raise ValueError("Chave pública inválida fornecida.")
    
    try:
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        if not public_bytes:
            raise ValueError("Falha ao serializar a chave pública.")
        
        finalhash = hashes.Hash(hashes.SHA256())
        finalhash.update(public_bytes)
        return finalhash.finalize().hex()
    except Exception as e:
        print(f"Erro ao gerar hash da chave pública: {e}")
        return None
