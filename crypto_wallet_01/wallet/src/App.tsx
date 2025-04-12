import React, { useState, useEffect } from 'react';
import { generateMnemonic, mnemonicToSeed } from 'bip39';
import { Wallet, Plus, Send, RefreshCw } from 'lucide-react';
import { ethers } from 'ethers';
import { Connection, PublicKey, LAMPORTS_PER_SOL } from '@solana/web3.js';
import * as ed25519 from 'ed25519-hd-key';
import nacl from 'tweetnacl';

interface Account {
  type: 'ETH' | 'SOL';
  address: string;
  balance: string;
}

function App() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [seedPhrase, setSeedPhrase] = useState('');
  const [showSeedPhrase, setShowSeedPhrase] = useState(false);

  useEffect(() => {
    if (!seedPhrase) {
      const newSeedPhrase = generateMnemonic();
      setSeedPhrase(newSeedPhrase);
    }
  }, [seedPhrase]);

  const createNewAccount = async (type: 'ETH' | 'SOL') => {
    try {
      if (type === 'ETH') {
        const wallet = ethers.Wallet.fromPhrase(seedPhrase);
        const provider = new ethers.JsonRpcProvider('https://eth-mainnet.g.alchemy.com/v2/demo');
        const balance = await provider.getBalance(wallet.address);

        setAccounts(prev => [
          ...prev,
          {
            type: 'ETH',
            address: wallet.address,
            balance: ethers.formatEther(balance),
          },
        ]);
      } else {
        const seed = await mnemonicToSeed(seedPhrase); // returns Buffer
        const derived = ed25519.derivePath("m/44'/501'/0'/0'", seed.toString('hex'));
        const keypair = nacl.sign.keyPair.fromSeed(Buffer.from(derived.key));
        const publicKey = new PublicKey(keypair.publicKey);

        const connection = new Connection('https://api.mainnet-beta.solana.com');
        const balance = await connection.getBalance(publicKey);

        setAccounts(prev => [
          ...prev,
          {
            type: 'SOL',
            address: publicKey.toBase58(),
            balance: (balance / LAMPORTS_PER_SOL).toString(),
          },
        ]);
      }
    } catch (error) {
      console.error('Error creating account:', error);
    }
  };

  const refreshBalances = async () => {
    try {
      const updatedAccounts = await Promise.all(
        accounts.map(async (account) => {
          if (account.type === 'ETH') {
            const provider = new ethers.JsonRpcProvider('https://eth-mainnet.g.alchemy.com/v2/demo');
            const balance = await provider.getBalance(account.address);
            return {
              ...account,
              balance: ethers.formatEther(balance),
            };
          } else {
            const connection = new Connection('https://api.mainnet-beta.solana.com');
            const publicKey = new PublicKey(account.address);
            const balance = await connection.getBalance(publicKey);
            return {
              ...account,
              balance: (balance / LAMPORTS_PER_SOL).toString(),
            };
          }
        })
      );
      setAccounts(updatedAccounts);
    } catch (error) {
      console.error('Error refreshing balances:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-2">
            <Wallet className="w-8 h-8" />
            <h1 className="text-2xl font-bold">Crypto Wallet</h1>
          </div>
          <button
            onClick={refreshBalances}
            className="p-2 rounded-full hover:bg-gray-800 transition-colors"
          >
            <RefreshCw className="w-5 h-5" />
          </button>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Seed Phrase</h2>
            <button
              onClick={() => setShowSeedPhrase(!showSeedPhrase)}
              className="text-sm text-gray-400 hover:text-white transition-colors"
            >
              {showSeedPhrase ? 'Hide' : 'Show'}
            </button>
          </div>
          <p className="font-mono text-sm bg-gray-700 p-4 rounded">
            {showSeedPhrase ? seedPhrase : '••••• ••••• ••••• •••••'}
          </p>
        </div>

        <div className="grid gap-4 mb-8">
          {accounts.map((account, index) => (
            <div key={`${account.type}-${account.address}-${index}`} className="bg-gray-800 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-semibold text-gray-400">{account.type}</span>
                <span className="text-sm">{account.balance} {account.type}</span>
              </div>
              <div className="font-mono text-sm break-all">{account.address}</div>
              <div className="mt-4 flex gap-2">
                <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">
                  <Send className="w-4 h-4" />
                  Send
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="flex gap-4">
          <button
            onClick={() => createNewAccount('ETH')}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Add ETH Account
          </button>
          <button
            onClick={() => createNewAccount('SOL')}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Add SOL Account
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
