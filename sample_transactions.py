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
    post_transaction(john, 10, "ENTRADA","1","1,2")
    post_transaction(john, 20, "ENTRADA","1","1,2","1","Logou atrasado","id")

    post_transaction(john, 30, "ENTRADA","2")
    post_transaction(john, 40, "ENTRADA","2")

    post_transaction(john, 50, "ENTRADA","3")
    post_transaction(john, 60, "ENTRADA","3")

    post_transaction(john, 70, "ENTRADA","4")
    post_transaction(john, 80, "ENTRADA","4")

    post_transaction(john, 90, "ENTRADA","5")
    post_transaction(john, 100, "ENTRADA","5")

    post_transaction(john, 110, "ENTRADA","6")
    post_transaction(john, 120, "ENTRADA","6")

    post_transaction(john, 130, "ENTRADA","7")
    post_transaction(john, 140, "ENTRADA","7")

    post_transaction(john, 150, "ENTRADA","8")
    post_transaction(john, 160, "ENTRADA","8")

    post_transaction(john, 170, "ENTRADA","9")
    post_transaction(john, 180, "ENTRADA","9")
    


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