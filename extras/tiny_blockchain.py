# Blockchain
# a digital ledger in which transactions made in bitcoin or another cryptocurrency are recorded chronologically and publicly.
# snakeCoin
import hashlib as hasher
import datetime as date
from flask import Flask
from flask import request

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data 
        self.previous_hash = previous_hash
        self.hash = self.hash_block() 

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + 
               str(self.timestamp) + 
               str(self.data) + 
               str(self.previous_hash)).encode())
        # this function will provide the hash we need
        # it takes all the attributes that we have and and then 
        # uses the hashlib lib as hasher to hash it

        return sha.hexdigest()
    # this is the basic structure of our block 

# we will create a function that simply returns  a genesis block .
# this block is of index 0, with arbitrary data value and an arbitrary value in the previous hash
def create_genesis_block():
    # manuaaly construct a block 
    # with index zero and arbitrary previoous hash
    return Block(0, date.datetime.now(), "Genesis Block", "0")

# now we need a function that will generate succeeding blocks in out blockchain
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)

# create the blockchain and add the genesis block
# declaring the blockchain and adding the first block in the list of blockchains
blockchain = [create_genesis_block()]
# previous block will be our previous block for now
previous_block = blockchain[0]

# How many blocs should we ad dto the chain
# aftr the genesis block
num_of_blocks_to_add = 20

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    # tell everyone about it!
    print("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print("Hash: {}\n".format(block_to_add.hash))

# Part 2 - Making our blockchain bigger

# snakecoin's data will be transactions, so each block's data fieldwill be a list of some transactions
# somthing like this
# {
#   "from": "71238uqirbfh894-random-public-key-a-alkjdflakjfewn204ij",
#   "to": "93j4ivnqiopvh43-random-public-key-b-qjrgvnoeirbnferinfo",
#   "amount": 3
# }

