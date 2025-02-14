from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/", name="View blockchain")
async def blockchain(request: Request):
    node = request.app.state.node    
    blockchain_data = node.blockchain.to_dict()
    print(f"Número de blocos: {len(blockchain_data['blocks'])}")
    
    for block in blockchain_data["blocks"]:
        print(f"Bloco: {block['block_count']}, Hash: {block['last_hash']}, Transações: {len(block['transactions'])}")
    
    
    return blockchain_data

