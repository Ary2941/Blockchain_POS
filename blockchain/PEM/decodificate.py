import hashlib
from cryptography.hazmat.primitives import serialization

from Crypto.PublicKey import RSA

import string

# Alfabeto Base62
BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase

def encode_base62(num):
    """Codifica um número inteiro em Base62."""
    if num == 0:
        return BASE62_ALPHABET[0]
    
    base62 = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(BASE62_ALPHABET[rem])
    
    return ''.join(reversed(base62))

def generate_username_from_rsa_key(private_key):
    """Gera um nome de usuário a partir da chave privada RSA."""
    # Gerar o hash SHA256 da chave privada
    private_key_hash = hashlib.sha256(private_key).digest()
    
    # Converter o hash para um número inteiro
    private_key_int = int.from_bytes(private_key_hash, byteorder='big')

    # Codificar o número inteiro em Base62
    username = encode_base62(private_key_int)

    return username

def generateUserId(file):
    return generate_username_from_rsa_key(file.encode("utf-8"))
