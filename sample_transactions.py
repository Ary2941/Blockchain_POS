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
    post_transaction(john, 1, "ENTRADA","1","1,2")
    post_transaction(john, 2, "ENTRADA","1","1,2","1","Logou atrasado","id")

    post_transaction(john, 3, "ENTRADA","2")
    post_transaction(john, 4, "ENTRADA","2")

    post_transaction(john, 5, "ENTRADA","3")
    post_transaction(john, 6, "ENTRADA","3")

    post_transaction(john, 7, "ENTRADA","4")
    post_transaction(john, 8, "ENTRADA","4")

    post_transaction(john, 9, "ENTRADA","5")
    post_transaction(john, 10, "ENTRADA","5")

    post_transaction(john, 11, "ENTRADA","6")
    post_transaction(john, 12, "ENTRADA","6")

    post_transaction(john, 13, "ENTRADA","7")
    post_transaction(john, 14, "ENTRADA","7")

    post_transaction(john, 15, "ENTRADA","8")
    post_transaction(john, 16, "ENTRADA","8")

    post_transaction(john, 17, "ENTRADA","9")
    post_transaction(john, 18, "ENTRADA","9")
    


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