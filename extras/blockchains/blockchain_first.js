// https://medium.com/@spenserhuang/learn-build-a-javascript-blockchain-part-1-ca61c285821e

// Learn and Build a Javascript Blockchain

// building a basic blockchain with a built-in proof of work system.

// main.js
// blockchains are built through a combination of linked lists and merkle trees.
// the linked list structure allows for the chain to continually build on top of itself.
// and is where the name blockchain derives from.

// hash
// hashes are simply deterministic functions that ccreate specfic outputs for each input,
// and they  are ususally irreversible menaing it is extremely difficult to derive the input from the output.
// They are critical to blockchain as they are key to making the chain immutable and to maintaining the integrity of the data.

const SHA256 = require('crypto-js/sha256')


class Block {
    // each block object takes in a timestampt and block data 
    constructor(timestamp, data) {
        this.index = 0;
        this.timestamp = timestamp;
        this.data = data;
        this.previousHash = "0";
        this.hash = this.calculateHash();
        this.nonce = 0;
    }

    calculateHash() {
        return SHA256(this.index + this.previousHash + this.timestamp + this.data + this.nonce).toString();
    }

    mineBlock(difficulty) {

    }
}

class Blockchain{
    // this is the main function of the blockchain and when this will be called it will generate a genesis block
    // and initiate the Blockchain - constructor function
    constructor(){
        this.chain = [this.createGenesis()];
    }

    createGenesis(){
        // you need to give the index, timestamp, data, and the previous hash
        return new Block(0,"01/01/2017")
    }


}


// all the function we gonna be having are 
// createGenesis, constructor, latestBlock, addBlock, checkValid


// cryptojs library and use their sha256 hash function
// the sha256 hash function was developed by the NSA and is an irreversible hash function.
// This is actually used in BTC mining as its prooof of work algorithm adn in the BTC address creation thanks to its security.