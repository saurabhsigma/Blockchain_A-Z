// https://medium.com/programmers-blockchain/create-simple-blockchain-java-tutorial-from-scratch-6eeed3cb03fa

//  in this tutorial i am just writing the code which is imp
// i will not try to run this as i dont have a suitable env
// this is just the code of the main thing - Making a blockchian with Java


// Hash - Digital FingerPrint

import java.util.Date; // for date - timestamp
import java.security.MessageDigest; // to generate a digital fingerprint and get SHA256 algorithm
import java.util.ArrayList;
import com.google.gson.GsonBuilder;



public class Block {
    public String hash;
    public String previousHash;
    private String data; // our data will be a simple message
    private long timeStamp; // as number of milliseconds since 1/1/1970.

    // Block constructor.
    public Block(String data, String previousHash){
        this.data = data;
        this.previousHash = previousHash;
        this.timeStamp = new Date().getTime();
        this.hash = calculateHash();

        
    }

    public String calculateHash(){
    String calculateHash = StringUtil.applySha256(
        previousHash + 
        Long.toString(timeStamp) + 
        data

    );
    return calculateHash;
}




    public void mineBlock(int difficulty) {
		String target = new String(new char[difficulty]).replace('\0', '0'); //Create a string with difficulty * "0" 
		while(!hash.substring( 0, difficulty).equals(target)) {
			nonce ++;
			hash = calculateHash();
		}
		System.out.println("Block Mined!!! : " + hash);
	}

}

public class StringUtil {
    // Aplies SHA256 to a string and returns the result,
    public static String applySha256(String input){
        try {
            MessageDigest digest  = MessageDigest.getInstance("SHA-256");
            // applies sha256 to our input,
            byte[] hash = digest.digest(input.getBytes("UTF-8"));
            SringBuffer hexString = new StringBuffer(); // this will contain hash as hexadecimal
            for(int i =0; i<hash.length;i++){
                String hex = Integer.toHexString(0xff & hash[i]);
                if(hex.length()==1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        }
        catch(Exception e){
            throw new RuntimeException(e);
        }
    }
}


public class NoobChain {
	
	public static ArrayList<Block> blockchain = new ArrayList<Block>();
	public static int difficulty = 5;

	public static void main(String[] args) {	
		//add our blocks to the blockchain ArrayList:
		
		blockchain.add(new Block("Hi im the first block", "0"));
		System.out.println("Trying to Mine block 1... ");
		blockchain.get(0).mineBlock(difficulty);
		
		blockchain.add(new Block("Yo im the second block",blockchain.get(blockchain.size()-1).hash));
		System.out.println("Trying to Mine block 2... ");
		blockchain.get(1).mineBlock(difficulty);
		
		blockchain.add(new Block("Hey im the third block",blockchain.get(blockchain.size()-1).hash));
		System.out.println("Trying to Mine block 3... ");
		blockchain.get(2).mineBlock(difficulty);	
		
		System.out.println("\nBlockchain is Valid: " + isChainValid());
		
		String blockchainJson = new GsonBuilder().setPrettyPrinting().create().toJson(blockchain);
		System.out.println("\nThe block chain: ");
		System.out.println(blockchainJson);
	}

    public static Boolean isChainValid() {
		Block currentBlock; 
		Block previousBlock;
		String hashTarget = new String(new char[difficulty]).replace('\0', '0');
		
		//loop through blockchain to check hashes:
		for(int i=1; i < blockchain.size(); i++) {
			currentBlock = blockchain.get(i);
			previousBlock = blockchain.get(i-1);
			//compare registered hash and calculated hash:
			if(!currentBlock.hash.equals(currentBlock.calculateHash()) ){
				System.out.println("Current Hashes not equal");			
				return false;
			}
			//compare previous hash and registered previous hash
			if(!previousBlock.hash.equals(currentBlock.previousHash) ) {
				System.out.println("Previous Hashes not equal");
				return false;
			}
			//check if hash is solved
			if(!currentBlock.hash.substring( 0, difficulty).equals(hashTarget)) {
				System.out.println("This block hasn't been mined");
				return false;
			}
		}
		return true;
	}

}


public static Boolean isChainValid(){
    Block currentBlock;
    Block previousBlock;

    //loop through blockchain to check hashes:
	for(int i=1; i < blockchain.size(); i++) {
		currentBlock = blockchain.get(i);
		previousBlock = blockchain.get(i-1);
		//compare registered hash and calculated hash:
		if(!currentBlock.hash.equals(currentBlock.calculateHash()) ){
			System.out.println("Current Hashes not equal");			
			return false;
		}
		//compare previous hash and registered previous hash
		if(!previousBlock.hash.equals(currentBlock.previousHash) ) {
			System.out.println("Previous Hashes not equal");
			return false;
		}
	}
	return true;
}