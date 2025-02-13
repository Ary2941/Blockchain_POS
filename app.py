import time
from flask import Flask, render_template, request, jsonify
import requests
import json


from blockchain.transaction.getAmount import getAmount
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils


sender_private_key = "./keys/genesis_private_key.pem"

app = Flask(__name__)

def post_transaction(sender, amount, type,employee_id,location):
    transaction = sender.create_transaction(amount, type,employee_id,location)
    url = "http://localhost:8050/api/v1/transaction/create/"
    package = {"transaction": BlockchainUtils.encode(transaction)}
    response = requests.post(url, json=package, timeout=15)
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    amount = getAmount()

    transaction_type = request.form['transaction_type']
    employee_id = request.form['employee_id']
    
    # Pegando a string de localização e separando as coordenadas
    location_str = request.form['location']

    print(f"location got: {location_str}")
    print(f"timestamp got: {str(time.ctime(amount))}")

    # Seu código de transação aqui

    #sender_private_key = request.form['sender_private_key']
    #now sender_private_key defined on this program
    
    sender = Wallet()
    sender.from_key(sender_private_key)


    response = post_transaction(sender, amount, transaction_type,employee_id,location_str)
    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)
