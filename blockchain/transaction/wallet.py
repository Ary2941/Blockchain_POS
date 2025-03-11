import binascii
import logging

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

from blockchain.block import Block
from blockchain.transaction.transaction import Transaction
from blockchain.utils.helpers import BlockchainUtils

class Wallet:
    def __init__(self):
        self.key_pair = ec.generate_private_key(ec.SECP256K1())

    def from_key(self, file_path):
        with open(file_path, "rb") as key_file:
            key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
        self.key_pair = key

    def from_file(self, file):
        key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )
        self.key_pair = key

    def sign(self, data):
        data_hash = BlockchainUtils.hash(data)
        signature = self.key_pair.sign(
            data_hash,
            ec.ECDSA(hashes.SHA256())
        )
        return signature.hex()

    @staticmethod
    def signature_valid(data, signature, public_key_string):
        signature = bytes.fromhex(signature)
        data_hash = BlockchainUtils.hash(data)
        public_key = serialization.load_pem_public_key(
            bytes(public_key_string, "utf-8")
        )

        try:
            public_key.verify(
                signature,
                data_hash,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            logging.error(f"Invalid signature, data hash: {data_hash}")

        return False

    def public_key_string(self):
        public_key_pem = self.key_pair.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return public_key_pem.decode("utf-8")
    
    def public_key_hex(self):
        public_key_pem = self.key_pair.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        public_key_hex = binascii.hexlify(public_key_pem).decode("utf-8")
        return public_key_hex


    def create_transaction(self, amount=None, type=None, employee_id=None, location=None, replacing_id=None, replacement_reason=None, adjusted_by=None):
        transaction = Transaction(self.public_key_string(), amount, type, employee_id, location, replacing_id, replacement_reason, adjusted_by)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction

    def create_block(self, transactions, last_hash, block_count):
        block = Block(transactions, last_hash, self.public_key_string(), block_count)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block
