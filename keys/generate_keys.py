from Crypto.PublicKey import RSA

# Gerar chave privada (primária)
key = RSA.generate(2048)

# Exportar chave privada
private_key = key.export_key()
with open("keys/private_key.pem", "wb") as priv_file:
    priv_file.write(private_key)

# Exportar chave pública
public_key = key.publickey().export_key()
with open("keys/public_key.pem", "wb") as pub_file:
    pub_file.write(public_key)

print("Chaves RSA geradas com sucesso!")
