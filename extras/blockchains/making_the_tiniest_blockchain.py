import hashlib
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.mine_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(
            (str(self.index) + 
             str(self.timestamp) + 
             str(self.data) + 
             str(self.previous_hash) + 
             str(self.nonce)).encode()
        )
        return sha.hexdigest()

    def mine_block(self, difficulty=4):
        """Simple proof-of-work: find a hash with 'difficulty' leading zeros."""
        self.nonce = 0
        computed_hash = self.hash_block()
        while computed_hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            computed_hash = self.hash_block()
        return computed_hash

def create_genesis_block():
    """Create the first block in the chain."""
    return Block(0, date.datetime.now(), "Genesis Block", "0")

def next_block(last_block):
    """Generate a new block, based on the previous block."""
    new_index = last_block.index + 1
    new_timestamp = date.datetime.now()
    new_data = f"Block {new_index} Data"
    return Block(new_index, new_timestamp, new_data, last_block.hash)

# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Number of blocks to add
num_of_blocks_to_add = 5

# Add blocks to the blockchain
for _ in range(num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add

    print(f"Block #{block_to_add.index} has been added!")
    print(f"Hash: {block_to_add.hash}\n")
