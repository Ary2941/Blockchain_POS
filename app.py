import time
from flask import Flask, render_template, request, jsonify
import requests
from blockchain.transaction.getAmount import getAmount
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils

app = Flask(__name__)

def post_transaction(sender, amount, type):
    transaction = sender.create_transaction(amount, type)
    url = "http://localhost:8050/api/v1/transaction/create/"
    package = {"transaction": BlockchainUtils.encode(transaction)}
    response = requests.post(url, json=package, timeout=15)
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    sender_private_key = request.form['sender_private_key']
    amount = getAmount()

    print(f"timestamp got: {str(time.ctime(amount))}")
    trans_type = request.form['transaction_type']
    
    sender = Wallet()
    sender.from_key(sender_private_key)


    response = post_transaction(sender, amount, trans_type)
    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)
