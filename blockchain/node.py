import copy
from datetime import datetime

from api.main import NodeAPI
from blockchain.blockchain import Blockchain
from blockchain.p2p.message import Message
from blockchain.p2p.socket_communication import SocketCommunication
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils
from blockchain.utils.logger import logger
from blockchain.utils.hippocampus import Hippocampus #HIPPOCAMPUS

def nownownow ():
    agora = datetime.now()
    return agora.strftime("%H:%M:%S")+ agora.strftime("%f")[:3]

class Node:
    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transaction_pool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()


        self.hippocampus = Hippocampus(self.port) #HIPPOCAMPUS
        self.blockchain.blocks = self.hippocampus.dejavu() #HIPPOCAMPUS
        if key:
            self.wallet.from_key(key)
            self.blockchain.pos.update(self.wallet.public_key_string(),1)

    def start_p2p(self):
        self.p2p = SocketCommunication(self.ip, self.port,self.wallet.public_key_string())
        self.p2p.start_socket_communication(self)

    def start_node_api(self, api_port):
        self.api = NodeAPI()
        self.api.inject_node(self)
        self.api.start(self.ip, api_port)

    def add_stakers(self,list_of_ns):
        for n in list_of_ns:
            self.blockchain.pos.update(n,1)

    #TESTE diminuição de eco
    def handle_transaction_self(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key
        signature_valid = Wallet.signature_valid(data, signature, signer_public_key)
        transaction_exists = self.transaction_pool.transaction_exists(transaction)
        transaction_in_block = self.blockchain.transaction_exists(transaction)
        
        
        if transaction.replacing_id:
            xelement = self.blockchain.get_transaction(transaction.replacing_id)
            if xelement: # replacing_id is a transaction
                if xelement.replacing_id: # replacing_id is replacing someone
                    print(f"🔴 Transaction rejected: try replacing id by {xelement.replacing_id}")
                    return f"🔴 Transaction rejected: did you mean {xelement.replacing_id}?"
            else: 
                print(f"🔴 Transaction rejected: {transaction.replacing_id} does not exists or is on transaction pool!")
                return f"🔴 Transaction rejected: {transaction.replacing_id} does not exists or is on transaction pool!"

        if not transaction_exists and not transaction_in_block and signature_valid:
            self.transaction_pool.add_transaction(transaction)
            message = Message(self.p2p.socket_connector, "TRANSACTION", transaction)
            self.p2p.broadcast(BlockchainUtils.encode(message))

            forging_required = self.transaction_pool.forging_required()
            if forging_required:
                self.forge()
            print(f"✅ transação {str(transaction.id)} adicionada!")
            return f"✅ transação {str(transaction.id)} adicionada!"

    def handle_transaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key
        signature_valid = Wallet.signature_valid(data, signature, signer_public_key)
        transaction_exists = self.transaction_pool.transaction_exists(transaction)
        transaction_in_block = self.blockchain.transaction_exists(transaction)

        if transaction.replacing_id:
            xelement = self.blockchain.get_transaction(transaction.replacing_id)
            if xelement: # replacing_id is a transaction
                if xelement.replacing_id: # replacing_id is replacing someone
                    print(f"🔴 Transaction rejected: try replacing id by {xelement.replacing_id}")
                    return f"🔴 Transaction rejected: did you mean {xelement.replacing_id}?"
            else: 
                print(f"🔴 Transaction rejected: {transaction.replacing_id} does not exists or is on transaction pool!")
                return f"🔴 Transaction rejected: {transaction.replacing_id} does not exists or is on transaction pool!"

        if not transaction_exists and not transaction_in_block and signature_valid:
            self.transaction_pool.add_transaction(transaction)
            '''
            message = Message(self.p2p.socket_connector, "TRANSACTION", transaction)
            self.p2p.broadcast(BlockchainUtils.encode(message))
            '''
            forging_required = self.transaction_pool.forging_required()
            if forging_required:
                self.forge()
            
            print(f"✅ transação {str(transaction.id)} adicionada!")
            return f"✅ transação {str(transaction.id)} adicionada!"

    def handle_block(self, block):
        print('bloco:',block.block_count,self.blockchain.blocks[-1].block_count)
        forger = block.forger
        block_hash = block.payload()
        signature = block.signature

        block_is_original = self.blockchain.block_is_original(block)
        block_count_valid = self.blockchain.block_count_valid(block)
        last_block_hash_valid = self.blockchain.last_block_hash_valid(block)
        forger_valid = self.blockchain.forger_valid(block)
        transactions_valid = self.blockchain.transactions_valid(block.transactions)
        signature_valid = Wallet.signature_valid(block_hash, signature, forger)

        if  not( block.block_count == self.blockchain.blocks[-1].block_count+1):
            # if is the same block DON'T request chain
            print(f"\nRequesting chain! our size {len(self.blockchain.blocks)} to his {block.block_count} {block_count_valid}")
            self.request_chain()
            
        if (
            last_block_hash_valid
            and forger_valid
            and transactions_valid
            and signature_valid
            and block_is_original
        ):
            print(f"🟢 Bloco {block.block_count} adicionado!")
            self.blockchain.add_block(block)
            curr = len(self.blockchain.blocks)
            self.nogemini()
            if curr == len(self.blockchain.blocks):

                self.transaction_pool.remove_from_pool(block.transactions)
                self.hippocampus.update_memory(block)  #HIPPOCAMPUS

                ''' #teste: diminuição de eco
                message = Message(self.p2p.socket_connector, "BLOCK", block)
                self.p2p.broadcast(BlockchainUtils.encode(message))
                print(f"⬆️ sending blockchain with {len(self.blockchain.blocks)-1} txs")
                '''
        else:
            print("algo não está certo!",last_block_hash_valid,forger_valid,transactions_valid,signature_valid,block_is_original)
            #TODO: FIX THIS
    def request_chain(self):
        message = Message(self.p2p.socket_connector, "BLOCKCHAINREQUEST", len(self.blockchain.blocks))
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.broadcast(encoded_message)

    def nogemini(self): 
        seen_signatures = set()  # Conjunto para armazenar assinaturas já vistas
        newblocks = []

        for block in self.blockchain.blocks:
            signature = block.signature
            #print(str(signature)[:6])
            if signature in seen_signatures:
                print(f"🔴 Duplicated block {signature} discarded")
            else:
                seen_signatures.add(signature)  # Adiciona ao conjunto
                newblocks.append(block)

        self.blockchain.blocks = newblocks
        return self.blockchain

    def handle_blockchain_request(self, requesting_node,data):
        print(f"{requesting_node.port} is requesting blockchain {data} (ours: {len(self.blockchain.blocks)})")
        message = Message(self.p2p.socket_connector, "BLOCKCHAIN", copy.deepcopy(self.blockchain)) #se blockdup: trocar self.blockchain por self.nogemini()
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.send(requesting_node, encoded_message)

    def handle_blockchain(self, blockchain):
        local_blockchain_copy = copy.deepcopy(self.blockchain)
        local_block_count = len(local_blockchain_copy.blocks)
        received_chain_block_count = len(blockchain.blocks)        
        print(f"⬇️ blockchain received with {received_chain_block_count-1} txs (ours: {local_block_count-1})")
        if local_block_count < received_chain_block_count:
            for block_number, block in enumerate(blockchain.blocks):
                if block_number >= local_block_count:
                    print(f"🟢 Block {block.block_count} added from blockchian received!")
                    self.hippocampus.update_memory(block) #hippocampus
                    local_blockchain_copy.add_block(block)
                    self.transaction_pool.remove_from_pool(block.transactions)
            self.blockchain = local_blockchain_copy

    def forge(self):
        forger = self.blockchain.next_forger()
        if forger == self.wallet.public_key_string():
            print("It's us!")
            block = self.blockchain.create_block(
                self.transaction_pool.transactions, self.wallet
            )
            ''' #DEBUG LOGGER
            logger.info(
                {
                    "message": "Next forger chosen",
                    "block": block.block_count,
                    "whoami": self.p2p,
                }
            )
            '''
            self.transaction_pool.remove_from_pool(self.transaction_pool.transactions)
            self.hippocampus.update_memory(block) #hippocampus
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            self.p2p.broadcast(BlockchainUtils.encode(message))
            print(f"We forged this block!")
        else:
            self.transaction_pool.remove_from_pool(self.transaction_pool.transactions)

    def broadcast_ping(self):
        """
        Envia uma mensagem de PING
        """
        message = Message(self.p2p.socket_connector, "PING", {"sender": self.port})
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.broadcast(encoded_message)
        print(f"[PING] Enviado")
        

    def send_ping(self, target_node):
        """
        Envia uma mensagem de PING para um nó alvo.
        """
        message = Message(self.p2p.socket_connector, "PING", {"sender": self.port})
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.send(target_node, encoded_message)
        print(f"[PING] Enviado para o nó {target_node.port}")

    def handle_ping(self, connected_node, message):
        """
        Responde um PING com um PONG.
        """
        print(message,message.keys())
        sender_port = message["sender"]
        response_message = Message(self.p2p.socket_connector, "PONG", {"sender": self.port})
        encoded_message = BlockchainUtils.encode(response_message)
        self.p2p.send(connected_node, encoded_message)
        print(f"[PONG] Respondido para o nó {sender_port}")

    def handle_pong(self, message):
        """
        Confirma que o PONG foi recebido.
        """
        sender_port = message["sender"]
        print(f"[PONG] Recebido de {sender_port}")


        