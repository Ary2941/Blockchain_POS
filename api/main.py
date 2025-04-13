import os
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from flask import jsonify
import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from api.api_v1.api import router as api_router
from api.utils.log_middleware import LogMiddleware
from blockchain.transaction.getAmount import getAmount
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils

templates_dir = os.path.join(os.path.dirname(__file__), "api_v1", "templates")

if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

app = FastAPI(
    docs_url="/api/v1/docs/",
    title="Blockchain API",
    description="This is an API communication interface to the node blockchain.",
    version="0.1.0",
)

app.add_middleware(LogMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=templates_dir)
session = requests.Session()

class NodeAPI:
    def __init__(self):
        global app
        self.app = app

    def start(self, ip, api_port):
        app.state.api_port = api_port
        uvicorn.run(self.app, host=ip, port=api_port, log_config=None)

    def inject_node(self, injected_node):
        self.app.state.node = injected_node


@app.get("/ping/", name="Healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return {"success": "pong!"}

# FACULTATIVOS
@app.get("/create/", name="Create transaction page")
async def transaction_pool(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "responseMessage": "_"})

@app.get("/edit/", name="edit transaction page")
async def transaction_pool(request: Request):
    return templates.TemplateResponse("outdex.html", {"request": request, "responseMessage": "_"})

class TransactionData(BaseModel):
    key_pair: str
    employee_id: str
    transaction_type: str
    location: str
    replacing_id: str

class TransactionData2(BaseModel):
    key_pair: str
    amount: int
    employee_id: str
    transaction_type: str
    location: str
    replacing_id: str
    replacement_reason: str

def post_transaction(sender, amount=None, type=None,employee_id=None,location=None,replacing_id=None,replacement_reason=None,adjusted_by=None):        

    transaction = sender.create_transaction(amount, type,employee_id,location,replacing_id,replacement_reason,adjusted_by)
    url = f"http://localhost:{app.state.api_port}/api/v1/transaction/create/"
    package = {"transaction": BlockchainUtils.encode(transaction)}
    response = requests.post(url, json=package, timeout=1) #response = requests.post(url, json=package, timeout=15)response = requests.post(url, json=package, timeout=5)
    print ("response status", response.status_code)
    return "True"
    
@app.post("/send_transaction")
async def send_transaction(transaction: TransactionData):  
    amount = getAmount()  
    try:
        john = Wallet()
        john.from_key(transaction.key_pair)
        type = transaction.transaction_type
        employee_id = transaction.employee_id
        location = transaction.location
        replacing_id = transaction.replacing_id

        result = post_transaction(john, 
            amount, 
            type,
            employee_id,
            location,
            replacing_id
        )
        #print("result",result)
        return jsonify({"message": result})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/edit_transaction")
async def edit_transaction(transaction: TransactionData2):  
    try:
        if transaction.replacing_id == "":
            raise ValueError("replacing_id is required")
        john = Wallet()
        john.from_key(transaction.key_pair)
        amount = transaction.amount
        type = transaction.transaction_type
        employee_id = transaction.employee_id
        location = transaction.location
        replacing_id = transaction.replacing_id
        replacement_reason = transaction.replacement_reason

        result = post_transaction(john, 
            amount,
            type,
            employee_id,
            location,
            replacing_id,
            replacement_reason
        )
        #print("result",result)
        return jsonify({"message": result})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# Incluindo os roteadores API
app.include_router(api_router, prefix="/api/v1")


