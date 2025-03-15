import dill
import time,datetime,random,requests

from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils


def seeds_from_30(client,user="nouser"):
    numdays = 1

    base = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
    date_list = [base - datetime.timedelta(days=x) for x in range(numdays+1)]
    print(date_list)
    loccount = 0
    for date in date_list:
        x = date + datetime.timedelta(hours=6,minutes=random.randint(0,61),seconds=random.randint(0,11))
        post_transaction(client,x.timestamp(),"ENTRADA",user,str(loccount))
        x = x + datetime.timedelta(hours=6,minutes=random.randint(0,61),seconds=random.randint(0,11))
        post_transaction(client,x.timestamp(),"SAIDA",user,str(loccount))
        loccount += 1

def post_transaction(sender, amount=None, type=None,employee_id=None,location=None,replacing_id=None,replacement_reason=None,adjusted_by=None):
    transaction = sender.create_transaction(amount, type,employee_id,location,replacing_id,replacement_reason,adjusted_by)
    url = f"http://localhost:{Portgoal}/api/v1/transaction/create/"

    print(transaction.to_dict())

    package = {"transaction": BlockchainUtils.encode(dill.dumps(transaction))}

    response = requests.post(url, json=package)
    print(response.text)


if __name__ == "__main__":
    Portgoal = 8050

    john = Wallet()
    john.from_key("./keys/node1_private_key.pem")

    jane = Wallet()
    jane.from_key("./keys/node2_private_key.pem")
    # Block size: 2 transactions / block
    
    tempo = datetime.datetime.now()
    seeds_from_30(john,"Oldegario")
    tempa = datetime.datetime.now()

    print(tempa-tempo)

'''
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
