from datetime import datetime
from json import JSONDecodeError

from fastapi import APIRouter, HTTPException, Request, Query

from blockchain.utils.decodificate import generateUserId
from blockchain.transaction.getAmount import getAmount
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils,convert_seconds
from blockchain.utils.hash import load_public_key, get_public_key_hash

from collections import defaultdict

from blockchain.transaction.transaction import Transaction

router = APIRouter()


@router.get("/", name="view all valid transactions")
async def blickchain(
    request: Request, 
    id: str = Query(None), 
    employee_id: str = Query(None),
    start: float = Query(None),
    end: float = Query(None),
    architects: str = ""
    ):
    architects = architects.split(",") if architects else []
    work_hours_string = '' 
    points_string = ''
    transactions_edited_string = ''
    node = request.app.state.node
    blockchain_data = node.blockchain.to_dict()

    

    # Extraindo todas as transações da blockchain
    all_transactions = [
        tx for block in blockchain_data.get("blocks", []) for tx in block.get("transactions", [])
        if (not id or tx.get("id") == id)
        and (not employee_id or tx.get("employee_id") == employee_id)
        and (not start or tx.get("amount") > start)
        and (not end or tx.get("amount") < end)
        and ((not(architects) or not(tx.get("adjusted_by"))) or (tx.get("adjusted_by") in architects))
    ]
    
    return {
        "all_transactions": all_transactions
        }


@router.get("/CH", name="return working wours")
async def blockchain(request: Request, employee_id: str = Query(None)):

    
    node = request.app.state.node
    blockchain_data = node.blockchain.to_dict()

    all_transactions = [
        tx for block in blockchain_data.get("blocks", []) for tx in block.get("transactions", [])  if (not employee_id or tx.get("employee_id") == employee_id)
    ]

    transactions_edited = {}

    transaction_map = {}

    for tx in all_transactions:
        replacing_id = tx.get("replacing_id")
        transaction_id = tx.get("id")
        amount = tx.get("amount")
        transaction_type = tx.get("type")
        replacement_reason = tx.get("replacement_reason")
        
        steptx = dict(amount=amount,transaction_id=transaction_id,replacing_id=replacing_id,type=transaction_type,replacement_reason=replacement_reason)

        if replacing_id and replacing_id in transaction_map:
            

            timestamp = datetime.fromtimestamp(transaction_map[replacing_id].get("amount"))
            hour_str = timestamp.strftime("%H:%M:%S")
            date_str = timestamp.strftime("%d-%m-%Y")
            motivo = transaction_map[replacing_id].get("replacement_reason")
            if not motivo:
                motivo = "não informado"
            tipo = transaction_map[replacing_id].get("type")

            stepted = dict(
                id = transaction_id,
                data = date_str,
                hora = hour_str,
                tipo = tipo,
                motivo = motivo 
            )
            transactions_edited[transaction_id] = stepted

            transaction_map[replacing_id] = steptx
        else:
            transaction_map[transaction_id] = steptx
    
    all_transactions = list(transaction_map.values())
    transactions_edited = list(transactions_edited.values())

    work_hours = []
    transactions_by_date = defaultdict(list)
    points = []
    for tx in all_transactions:
        transaction_id = tx.get("transaction_id")
        timestamp = datetime.fromtimestamp(tx.get("amount"))
        hour_str = timestamp.strftime("%H:%M:%S")
        date_str = timestamp.strftime("%d-%m-%Y")
        ch = 1
        tipo = tx.get("type")
        transactions_by_date[date_str].append(tx)

        stepted = dict(
            id = transaction_id,
            data = date_str,
            hora = hour_str,
            tipo = tipo,
            CH  = ch,
            )

        points.append(stepted)

    return {
        "Marcações registradas no ponto eletrônico:": points,
        "Tratamentos efetuados sobre os dados originais:": transactions_edited,
        }

@router.get("/relatory", name="return working wours")
async def blockchain(request: Request, 
    employee_id: str = Query(None),
    start: float = Query(None),
    end: float = Query(None)
    ):
    work_hours_string = '' 
    points_string = ''
    transactions_edited_string = ''
    
    node = request.app.state.node
    blockchain_data = node.blockchain.to_dict()
    
    all_transactions = [
        tx for block in blockchain_data.get("blocks", []) for tx in block.get("transactions", []) 
        if (not employee_id or tx.get("employee_id") == employee_id)
        and (not start or tx.get("amount") > start)
        and (not end or tx.get("amount") < end)
    ]

    transaction_map = {}

    for tx in all_transactions:
        replacing_id = tx.get("replacing_id")
        transaction_id = tx.get("id")
        amount = tx.get("amount")
        transaction_type = tx.get("type")
        replacement_reason = tx.get("replacement_reason")
        
        steptx = dict(amount=amount,transaction_id=transaction_id,replacing_id=replacing_id,type=transaction_type,replacement_reason=replacement_reason)

        if replacing_id and replacing_id in transaction_map:
            

            timestamp = datetime.fromtimestamp(transaction_map[replacing_id].get("amount"))
            hour_str = timestamp.strftime("%H:%M:%S")
            date_str = timestamp.strftime("%d-%m-%Y")
            motivo = transaction_map[replacing_id].get("replacement_reason")
            if not motivo:
                motivo = "não informado"
            tipo = transaction_map[replacing_id].get("type")

            stepted = dict(data = date_str,
                 hora = hour_str,
                 tipo = tipo,
                 motivo = motivo 
            )
            transactions_edited_string +="\n\hline "+ hour_str+' & '+tipo+' & '+motivo+" \\\\"

            transaction_map[replacing_id] = steptx
        else:
            transaction_map[transaction_id] = steptx
    
    all_transactions = list(transaction_map.values())

    transactions_by_date = defaultdict(list)
    for tx in all_transactions:
        timestamp = datetime.fromtimestamp(tx.get("amount"))
        hour_str = timestamp.strftime("%H:%M:%S")
        date_str = timestamp.strftime("%d-%m-%Y")
        ch = 1
        transactions_by_date[date_str].append(tx)
        points_string += "\n\hline "+ date_str+' & '+hour_str+' & '+str(ch)+" \\\\"

    for date, transactions in transactions_by_date.items():
        transactions.sort(key=lambda x: x["amount"])
        daily_hours = 0
        last_entry = None
        
        stringHours = ""

        for tx in transactions:

            timestamp = datetime.fromtimestamp(tx.get("amount"))
            stringHours += ' '+ timestamp.strftime("%H:%M:%S") 


            if tx["type"] == "ENTRADA":
                last_entry = tx["amount"]
            elif tx["type"] == "SAIDA" and last_entry:
                daily_hours += tx["amount"] - last_entry
                last_entry = None


        work_hours_string += "\n\hline "+ date+' & '+stringHours[1:]+' & '+convert_seconds(daily_hours)+" \\\\"

    return {
        "tratamentos":transactions_edited_string[8:],
        "marcacoes":points_string[8:],
        "jornada":work_hours_string[8:]
        }

@router.get("/transaction_pool/", name="Get all transactions in pool")
async def transaction_pool(request: Request):
    node = request.app.state.node
    return node.transaction_pool.transactions

@router.post("/create/", name="Create transaction by coded transaction")
async def create_transaction(request: Request):
    node = request.app.state.node
    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Can not parse request body.")
    if "transaction" not in payload:
        raise HTTPException(status_code=400, detail="Missing transaction value")
        
    transaction = BlockchainUtils.decode(payload["transaction"])
    #BREAKPOINT
    if type(transaction) == dict and transaction['py/object'] == 'utils.transaction.Transaction':

        sender_public_key = transaction['sender_public_key'].replace(r'\n', '\\n')
        txid = transaction['id']
        amount = transaction['amount']
        tipo = transaction['type']
        employee_id = transaction['employee_id']
        location = transaction['location']
        replacing_id = transaction['replacing_id']
        replacement_reason = transaction['replacement_reason']
        adjusted_by= transaction['adjusted_by']
        signature = transaction['signature']
        transaction = Transaction(sender_public_key, amount, tipo,employee_id,location,replacing_id,replacement_reason,adjusted_by)
        transaction.id = txid
        transaction.sign(signature)


    result = await node.handle_transaction(transaction)
    print ("RESULT", result)
    return result
