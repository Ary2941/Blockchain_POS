from datetime import datetime
from json import JSONDecodeError

from fastapi import APIRouter, HTTPException, Request

from blockchain.utils.helpers import BlockchainUtils

from collections import defaultdict

router = APIRouter()


from fastapi import APIRouter, Request, Query

router = APIRouter()

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

        if replacing_id and replacing_id in transaction_map:
            # Se a transação está sendo substituída, troca pela nova
            transaction_map[replacing_id] = tx
        else:
            # Senão, adiciona normalmente
            transaction_map[transaction_id] = tx

    # Pegamos apenas as transações finais, sem duplicatas
    all_transactions = list(transaction_map.values())

    if employee_id:
        # Filtrar apenas transações do employee_id
        filtered_transactions = [tx for tx in all_transactions if tx.get("employee_id") == employee_id]
        return {"filtered_transactions": filtered_transactions}

    return {"all_transactions": all_transactions}



@router.get("/CH", name="return working wours")
async def blockchain(request: Request, employee_id: str = Query(None)):
    node = request.app.state.node
    blockchain_data = node.blockchain.to_dict()

    all_transactions = [
        tx for block in blockchain_data.get("blocks", []) for tx in block.get("transactions", [])
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

    if employee_id:
        filtered_transactions = [tx for tx in all_transactions if tx.get("employee_id") == employee_id]
    else:
        filtered_transactions = all_transactions

    return {"seconds_worked": work_hours, "transactions": filtered_transactions}







@router.get("/transaction_pool/", name="Get all transactions in pool")
async def transaction_pool(request: Request):
    node = request.app.state.node
    return node.transaction_pool.transactions


@router.post("/create/", name="Create transaction")
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
    node.handle_transaction(transaction)

    return {"message": "Received transaction"}
