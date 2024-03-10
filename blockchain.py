# Module 1 : create a Blockchain
# only mine some blocks and finding the actual state of the blockchain 
# building the blockchain
import datetime
import hashlib
import json
from flask import Flask, jsonify

# we will get index of the new block, the proof of the new block, the previous hash attached to the new block and also the message attached to the block...
# 4 essential componenets of a block 1.index 2. the timestamp 3. proof of the block 4. the previous hash
# part 1: building our blockchain
print("hello")

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash = '0')

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestampt': str(datetime.datetime.now()),
                 'proof': proof,
                  'previous_hash': previous_hash }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while (check_proof is False):
            hash_operations = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operations[:4] == '0000':
                check_proof = True
            else:
                new_proof +=1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index<len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operations = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operations[:4]!='0000':
                return False
            previous_block = block
            block +=1
        return True
    
# part 2: mining our blockchain
