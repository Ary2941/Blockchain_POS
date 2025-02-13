import time
import requests

from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils


def post_transaction(sender, amount=None, type=None,employee_id=None,location=None,replacing_id=None,replacement_reason=None,adjusted_by=None):
    transaction = sender.create_transaction(amount, type,employee_id,location,replacing_id,replacement_reason,adjusted_by)
    url = "http://localhost:8050/api/v1/transaction/create/"
    package = {"transaction": BlockchainUtils.encode(transaction)}
    response = requests.post(url, json=package, timeout=120)
    print(response.text)


if __name__ == "__main__":
    john = Wallet()
    john.from_key("./keys/node1_private_key.pem")

    jane = Wallet()
    jane.from_key("./keys/node2_private_key.pem")
    # Block size: 2 transactions / block

    # Forger: Genesis
    post_transaction(john, time.time(), "ENTRADA","1234","1,2")
    post_transaction(john, time.time(), "ENTRADA","1234","1,2","1","Logou atrasado","id")

    post_transaction(john, time.time(), "ENTRADA")
    post_transaction(john, time.time(), "ENTRADA")

    post_transaction(john, time.time(), "ENTRADA")
    post_transaction(john, time.time(), "ENTRADA")

    post_transaction(john, time.time(), "ENTRADA")
    post_transaction(john, time.time(), "ENTRADA")

    post_transaction(john, time.time(), "ENTRADA")
    post_transaction(john, time.time(), "ENTRADA")

    post_transaction(john, time.time(), "ENTRADA")
    post_transaction(john, time.time(), "ENTRADA")

    post_transaction(john, time.time(), "ENTRADA")
    post_transaction(john, time.time(), "ENTRADA")

    post_transaction(john, time.time(), "ENTRADA")
    post_transaction(john, time.time(), "ENTRADA")

    post_transaction(john, time.time(), "ENTRADA")
    post_transaction(john, time.time(), "ENTRADA")
    
    post_transaction(john, time.time(), "ENTRADA")
    post_transaction(john, time.time(), "ENTRADA")

#TODO: fix freezing on third transaction

'''

import requests

from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils


def post_transaction(sender, receiver, amount, type):
    transaction = sender.create_transaction(receiver.public_key_string(), amount, type)
    url = "http://localhost:8050/api/v1/transaction/create/"
    package = {"transaction": BlockchainUtils.encode(transaction)}
    response = requests.post(url, json=package, timeout=15)
    print(response.text)


if __name__ == "__main__":
    john = Wallet()
    jane = Wallet()
    jane.from_key("./keys/staker_private_key.pem")

    exchange = Wallet()

    # Block size: 2 transactions / block

    # Forger: Genesis
    post_transaction(exchange, jane, 100, "EXCHANGE")
    post_transaction(exchange, john, 100, "EXCHANGE")
    post_transaction(exchange, john, 10, "EXCHANGE")
    post_transaction(jane, jane, 25, "STAKE")

    # Forger: Probably Jane (the Genesis forger has 1 token staked, therefore Jane will most likely be the next forger)
    post_transaction(jane, john, 1, "TRANSFER")
    post_transaction(jane, john, 1, "TRANSFER")

    # One remaining in transaction pool
    post_transaction(jane, john, 1, "TRANSFER")

'''