from datetime import datetime
from json import JSONDecodeError

from fastapi import APIRouter, HTTPException, Request, Query

from blockchain.transaction.getAmount import getAmount
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils
from blockchain.utils.hash import load_public_key, get_public_key_hash

from collections import defaultdict

router = APIRouter()
'''
@router.get("/", name="view all valid transactions")
async def blockchain(request: Request, employee_id: str = Query(None)):
    node = request.app.state.node
    blockchain_data = node.blockchain.to_dict()

    # Extraindo todas as transações da blockchain
    all_transactions = [
        tx for block in blockchain_data.get("blocks", []) for tx in block.get("transactions", [])
    ]

    # Dicionário para substituir transações por replacing_id
    transaction_map = {}

    for tx in all_transactions:
        replacing_id = tx.get("replacing_id")
        transaction_id = tx.get("id")

        dia = tx["amount"]
        dia = datetime.fromtimestamp(dia).date()
        horario = tx["amount"]
        horario = datetime.fromtimestamp(horario)
        horario = horario.strftime("%H:%M:%S")

        tipo = tx["type"]
        xas = load_public_key(tx["sender_public_key"])
        yas = get_public_key_hash(xas)
        
        if replacing_id and replacing_id in transaction_map:
            # Se a transação está sendo substituída, troca pela nova
            transaction_map[replacing_id]   = dict(sender=yas, id=tx["id"], employee_id = tx["employee_id"], Dia = dia, Horário = horario, Tipo = tipo, CH =  1)
        else:
            # Senão, adiciona normalmente
            transaction_map[transaction_id] = dict(sender=yas,id =tx["id"], employee_id = tx["employee_id"], Dia = dia, Horário = horario, Tipo = tipo, CH =  1)

    # Pegamos apenas as transações finais, sem duplicatas
    all_transactions = list(transaction_map.values())

    if employee_id:
        filtered_transactions = [
            {key: value for key, value in tx.items() if key != "employee_id"}  # Remove a chave 'employee_id' da transação
            for tx in all_transactions
            if tx.get("employee_id") == employee_id  # Filtra pelas transações com o 'employee_id' correspondente
        ]
        return filtered_transactions
    return {"all_transactions": all_transactions}

'''

@router.get("/", name="view all valid transactions")
async def blickchain(request: Request, sender: str = Query(None)):
    node = request.app.state.node
    blockchain_data = node.blockchain.to_dict()

    # Extraindo todas as transações da blockchain
    all_transactions = [
        tx for block in blockchain_data.get("blocks", []) for tx in block.get("transactions", [])
    ]

    # Dicionário para substituir transações por replacing_id
    transaction_map = {}

    for tx in all_transactions:
        replacing_id = tx.get("replacing_id")
        transaction_id = tx.get("id")

        dia = tx["amount"]
        dia = datetime.fromtimestamp(dia).date()
        horario = tx["amount"]
        horario = datetime.fromtimestamp(horario)
        horario = horario.strftime("%H:%M:%S")

        tipo = tx["type"]
        xas = load_public_key(tx["sender_public_key"])
        yas = get_public_key_hash(xas)
        
        if replacing_id and replacing_id in transaction_map:
            # Se a transação está sendo substituída, troca pela nova
            transaction_map[replacing_id]   = dict(sender=yas, id=replacing_id, employee_id = tx["employee_id"], Dia = dia, Horário = horario, Tipo = tipo, CH =  1)
        else:
            # Senão, adiciona normalmente
            transaction_map[transaction_id] = dict(sender=yas,id =tx["id"], employee_id = tx["employee_id"], Dia = dia, Horário = horario, Tipo = tipo, CH =  1)

    # Pegamos apenas as transações finais, sem duplicatas
    all_transactions = list(transaction_map.values())

    if sender:
        filtered_transactions = [
            tx #{key: value for key, value in tx.items() if key != "employee_id"}  # Remove a chave 'employee_id' da transação
            for tx in all_transactions
            if tx.get("sender") == sender  # Filtra pelas transações com o 'employee_id' correspondente
        ]
        return filtered_transactions
    return {"all_transactions": all_transactions}


@router.get("/CH", name="return working wours")
async def blockchain(request: Request, employee_id: str = Query(None)):
    node = request.app.state.node
    blockchain_data = node.blockchain.to_dict()

    all_transactions = [
        tx for block in blockchain_data.get("blocks", []) for tx in block.get("transactions", [])  if tx.get("employee_id") == employee_id
    ]

    transaction_map = {}

    for tx in all_transactions:
        replacing_id = tx.get("replacing_id")
        transaction_id = tx.get("id")

        if replacing_id and replacing_id in transaction_map:
            transaction_map[replacing_id] = tx
        else:
            transaction_map[transaction_id] = tx

    all_transactions = list(transaction_map.values())

    work_hours = defaultdict(float)
    transactions_by_date = defaultdict(list)

    for tx in all_transactions:
        timestamp = datetime.fromtimestamp(tx.get("amount"))
        date_str = timestamp.strftime("%Y-%m-%d")
        transactions_by_date[date_str].append(tx)

    for date, transactions in transactions_by_date.items():
        transactions.sort(key=lambda x: x["amount"])
        daily_hours = 0
        last_entry = None

        for tx in transactions:
            if tx["type"] == "ENTRADA":
                last_entry = tx["amount"]
            elif tx["type"] == "SAIDA" and last_entry:
                daily_hours += tx["amount"] - last_entry
                last_entry = None

        work_hours[date] = daily_hours
    

    return {"seconds_worked": work_hours, "transactions": all_transactions}

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
    if payload.get("file"):
        client.from_file(payload["file"])
    elif payload.get("sender_private_key"):
        client.from_key(payload["sender_private_key"])
    
    amount = getAmount()
    type = payload.get("type")
    employee_id = payload.get("employee_id")
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
    if payload.get("file"):
        client.from_file(payload["file"])
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
        replacement_reason=replacement_reason
        )
    result = await node.handle_transaction(transaction)
    print ("RESULT", result)

