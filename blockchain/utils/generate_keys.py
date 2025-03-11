from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import binascii


# Gerar chave privada usando secp256k1
private_key = ec.generate_private_key(ec.SECP256K1())

# Exportar chave privada para PEM
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

with open("ec_private_key.pem", "wb") as priv_file:
    priv_file.write(private_pem)

# Exportar chave pública para PEM
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

with open("ec_public_key.pem", "wb") as pub_file:
    pub_file.write(public_pem)

print("Chaves EC (secp256k1) geradas com sucesso!")


def hex_to_pem(hex_str, is_private=True):
    pem_bytes = binascii.unhexlify(hex_str)
    if is_private:
        return serialization.load_pem_private_key(pem_bytes, password=None)
    return serialization.load_pem_public_key(pem_bytes)

def pem_to_hex(hex_str):
    binascii.hexlify(hex_str).decode()