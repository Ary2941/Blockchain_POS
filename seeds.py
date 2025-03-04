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



john = Wallet()
john.from_key("./keys/node1_private_key.pem")

jane = Wallet()
jane.from_key("./keys/node2_private_key.pem")

jill = Wallet()
jill.from_key("./keys/node2_private_key.pem")



post_transaction(john, 1740680022, "ENTRADA", "1", "48.862140, 2.289971")
post_transaction(john, 1740680123, "SAIDA", "1", "48.862150, 2.289972")
post_transaction(jane, 1740680224, "ENTRADA", "2", "48.862160, 2.289973")
post_transaction(jane, 1740680325, "SAIDA", "2", "48.862170, 2.289974")
post_transaction(jill, 1740680426, "ENTRADA", "3", "48.862180, 2.289975")
post_transaction(jill, 1740680527, "SAIDA", "3", "48.862190, 2.289976")
post_transaction(john, 1740680628, "ENTRADA", "4", "48.862200, 2.289977")
post_transaction(john, 1740680729, "SAIDA", "4", "48.862210, 2.289978")
post_transaction(john, 1740680830, "ENTRADA", "5", "48.862220, 2.289979")
post_transaction(john, 1740680931, "SAIDA", "5", "48.862230, 2.289980")
post_transaction(john, 1740681032, "ENTRADA", "6", "48.862240, 2.289981")
post_transaction(john, 1740681133, "SAIDA", "6", "48.862250, 2.289982")
post_transaction(john, 1740681234, "ENTRADA", "7", "48.862260, 2.289983")
post_transaction(john, 1740681335, "SAIDA", "7", "48.862270, 2.289984")
post_transaction(john, 1740681436, "ENTRADA", "8", "48.862280, 2.289985")
post_transaction(john, 1740681537, "SAIDA", "8", "48.862290, 2.289986")
post_transaction(john, 1740681638, "ENTRADA", "9", "48.862300, 2.289987")
post_transaction(john, 1740681739, "SAIDA", "9", "48.862310, 2.289988")
post_transaction(john, 1740681840, "ENTRADA", "10", "48.862320, 2.289989")
post_transaction(john, 1740681941, "SAIDA", "10", "48.862330, 2.289990")
