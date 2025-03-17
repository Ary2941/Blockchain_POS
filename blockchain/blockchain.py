import binascii
import logging

from blockchain.block import Block
from blockchain.pos.proof_of_stake import ProofOfStake
from blockchain.transaction.account_model import AccountModel
from blockchain.utils.helpers import BlockchainUtils


class Blockchain:
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.account_model = AccountModel()
        self.pos = ProofOfStake()

    def add_block(self, block):
        self.execute_transactions(block.transactions)
        self.blocks.append(block)

    def get_transaction(self, transaction_id):
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.id == transaction_id:
                    return transaction
                
        return None

    def to_dict(self):
        data = {}
        blocks_readable = []
        for block in self.blocks:
            blocks_readable.append(block.to_dict())
        data["blocks"] = blocks_readable
        return data

    def block_is_original(self, block):
        if self.blocks[-1].signature == block.signature:
            return False
        return True

    def block_count_valid(self, block):
        return self.blocks[-1].block_count+1 == block.block_count

    def last_block_hash_valid(self, block):
        last_block_chain_block_hash = BlockchainUtils.hash(
            self.blocks[-1].payload()
        ).hex()
        if last_block_chain_block_hash == block.last_hash:
            return True
        return False

    def get_covered_transaction_set(self, transactions):
        covered_transactions = []
        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
            else:
                logging.error("Transaction is not covered by sender")
        return covered_transactions

    def transaction_covered(self, transaction): 
        # se for transação de entrada some no balanço de horas
        # se for outra veja se o balanço é menor do que vai entrar, se sim a transação é coberta

        if transaction.type == "ENTRADA":
            return True
        sender_balance = self.account_model.get_balance(transaction.sender_public_key)
        if sender_balance <= transaction.amount:
            return True
        return False

    def execute_transactions(self, transactions):
        for transaction in transactions:
            self.execute_transaction(transaction)

    def execute_transaction(self, transaction):
        if transaction.type == "ENTRADA":
            sender = transaction.sender_public_key
            amount = transaction.amount
            self.account_model.update_balance(sender, -amount)

        if transaction.type == "SAIDA":
            sender = transaction.sender_public_key
            amount = transaction.amount
            self.account_model.update_balance(sender, amount)

    def next_forger(self):
        last_block_hash = BlockchainUtils.hash(self.blocks[-1].payload()).hex()
        next_forger = self.pos.forger(last_block_hash)
        print(f"NEXT FORGER{next_forger}")
        return next_forger

    def create_block(self, transactions_from_pool, forger_wallet):
        covered_transactions = self.get_covered_transaction_set(transactions_from_pool)
        self.execute_transactions(covered_transactions)
        new_block = forger_wallet.create_block(
            covered_transactions,
            BlockchainUtils.hash(self.blocks[-1].payload()).hex(),
            len(self.blocks),
        )
        self.blocks.append(new_block)
        return new_block

    def transaction_exists(self, transaction):
        for block in self.blocks:
            for block_transaction in block.transactions:
                if transaction.equals(block_transaction):
                    return True
        return False

    def forger_valid(self, block):
        forger_public_key = self.pos.forger(block.last_hash)  # Chave esperada (pode estar em hex)
        proposed_block_forger = block.forger  # Chave proposta (PEM ou hex)

        # Se a chave esperada estiver em hex, converta para PEM
        try:
            forger_public_key_pem = binascii.unhexlify(forger_public_key)
        except (binascii.Error, UnicodeDecodeError):
            forger_public_key_pem = forger_public_key.encode("utf-8")  # Já está em PEM

        # Se a chave proposta estiver em hex, converta para PEM
        try:
            proposed_block_forger_pem = binascii.unhexlify(proposed_block_forger)
        except (binascii.Error, UnicodeDecodeError):
            proposed_block_forger_pem = proposed_block_forger.encode("utf-8")  # Já está em PEM

        return forger_public_key_pem == proposed_block_forger_pem

    def transactions_valid(self, transactions):
        covered_transactions = self.get_covered_transaction_set(transactions)
        if len(covered_transactions) == len(transactions):
            return True
        return False