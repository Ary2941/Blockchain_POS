from datetime import datetime
from json import JSONDecodeError

from fastapi import APIRouter, HTTPException, Request, Query

from blockchain.PEM.decodificate import generateUserId
from blockchain.transaction.getAmount import getAmount
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils,convert_seconds
from blockchain.utils.hash import load_public_key, get_public_key_hash

from collections import defaultdict

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
    work_hours_string = '' 
    points_string = ''
    transactions_edited_string = ''
    
    node = request.app.state.node
    blockchain_data = node.blockchain.to_dict()

    all_transactions = [
        tx for block in blockchain_data.get("blocks", []) for tx in block.get("transactions", [])  if tx.get("employee_id") == employee_id
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

            stepted = dict(data = date_str,
                 hora = hour_str,
                 tipo = tipo,
                 motivo = motivo 
            )
            transactions_edited[transaction_id] = stepted
            transactions_edited_string +="\n "+ hour_str+' & '+tipo+' & '+motivo+" \\\\"

            transaction_map[replacing_id] = steptx
        else:
            transaction_map[transaction_id] = steptx
    
    all_transactions = list(transaction_map.values())
    transactions_edited = list(transactions_edited.values())

    work_hours = []
    transactions_by_date = defaultdict(list)
    points = []
    for tx in all_transactions:
        timestamp = datetime.fromtimestamp(tx.get("amount"))
        hour_str = timestamp.strftime("%H:%M:%S")
        date_str = timestamp.strftime("%d-%m-%Y")
        ch = 1
        tipo = tx.get("type")
        transactions_by_date[date_str].append(tx)
        points.append(dict(data = date_str,hora = hour_str,tipo=tipo,CH = ch))
        points_string += "\n "+ date_str+' & '+hour_str+' & '+str(ch)+" \\\\"

    print(points)
             
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


        work_hours_string += "\n "+ date+' & '+stringHours[1:]+' & '+convert_seconds(daily_hours)+" \\\\"

        work_hours.append(dict(data=date,horas_trabalhadas=convert_seconds(daily_hours),registros=stringHours[1:]))

    return {
        "Jornada realizada": work_hours, 
        "Marcações registradas no ponto eletrônico:": points,
        "Tratamentos efetuados sobre os dados originais:": transactions_edited,
        "tratamentos":transactions_edited_string[2:],
        "marcacoes":points_string[2:],
        "jornada":work_hours_string[2:]
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
    result = await node.handle_transaction(transaction)
    print ("RESULT", result)
    return result

@router.post("/createRAW/", name="Create transaction by dictionary")
async def create_transactionRAW(request: Request):
    node = request.app.state.node
    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Can not parse request body.")
    payload = BlockchainUtils.decode(payload)
    
    client = Wallet()
    employee_id = payload.get("employee_id")

    if payload.get("file"):
        client.from_file(payload["file"])
        employee_id = generateUserId(client.public_key_string())
    
    elif payload.get("sender_private_key"):
        client.from_key(payload["sender_private_key"])
    print(f"PUBKEY{client.public_key_string() }")
    amount = getAmount()
    type = payload.get("type")
    print(f"EMPLOYEE_ID{employee_id}")
    
    
    ###
    ### TODO: employee_id vai ser a chave pública da chave privada de quem publica convertido em base64
    ###
    location = payload.get("location")
    replacing_id = payload.get("replacing_id")
    replacement_reason = payload.get("replacement_reason")
    adjusted_by = payload.get("adjusted_by")
    transaction = client.create_transaction(amount, type,employee_id,location,replacing_id,replacement_reason,adjusted_by)
    result = await node.handle_transaction(transaction)
    print ("RESULT", result)


#TODO: add coding and decoding for safety
@router.post("/editRAW/", name="Edit transaction by dictionary")
async def edit_transactionRAW(request: Request):
    node = request.app.state.node
    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Can not parse request body.")
    payload = BlockchainUtils.decode(payload)
    

    client = Wallet()
    adjusted_by = payload.get("adjusted_by")
    if payload.get("file"):
        try:
            client.from_file(payload["file"])
            adjusted_by = generateUserId(client.public_key_string())
        except:
            print("FAILED TO LOAD FILE IN PAYLOAD")

    elif payload.get("sender_private_key"):
        client.from_key(payload["sender_private_key"])
    
    type = payload.get("type")
    amount = payload.get("amount")
    location = payload.get("location")
    replacing_id = payload.get("replacing_id")
    replacement_reason = payload.get("replacement_reason")
    employee_id = payload.get("employee_id")
    print(replacing_id,"replacing this id")
    transaction = client.create_transaction(
        amount=int(amount), 
        type=type,
        employee_id=employee_id,
        location=location,
        replacing_id=replacing_id,
        replacement_reason=replacement_reason,
        adjusted_by=adjusted_by
        )
    result = await node.handle_transaction(transaction)
    print ("RESULT", result)

