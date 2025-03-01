# The tiniest blockchain was extremely simple, and it was relatively easy to make.
# But, with its simplicity came a few flaws. First, SnakeCoin only ran on one single machine,
# so it was far from distributed, let alone decentralized. Second, blocks could be added to the 
# chain as fast as the host computer could create a Python object and add it to a list. In the case 
# of a simple blockchain, that’s not a problem, but we’re now going to let SnakeCoin be an actual 
# cryptocurrency so we’ll need control the amount of blocks (and coins) that can be created at a time.

# from now on snakecoins data will be transactions, so each block's data field will be a list of some transactions.


# this is how a normal transaction will look like, and this is our data
# {
#   "from": "71238uqirbfh894-random-public-key-a-alkjdflakjfewn204ij",
#   "to": "93j4ivnqiopvh43-random-public-key-b-qjrgvnoeirbnferinfo",
#   "amount": 3
# }

from flask import Flask
from flask import request
node = Flask(__name__)

# store the transactions that
# this node has in a list
this_nodes_transactions = []

@node.route('/txion', method= ['POST'])
def transaction():
    if request.method == "POST":
        # on each new POST request,
        # we extract the transaction data
        new_txion = request.get_json()
        # Then we add the transaction to our list
        this_nodes_transactions.append(new_txion)
        # Because the transaction was successfully
        # submitted, we log it to our console
        print("New transaction")
        print("FROM: {}".format(new_txion['from']))
        print("TO: {}".format(new_txion['to']))
        print("AMOUNT: {}\n".format(new_txion['amount']))
        # Then we let the client know it worked out
        return "Transaction submission successful\n"
    
node.run()