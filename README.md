# Proof of Stake POC

This README explains how to build the current application from scratch.

At this stage, the project is not a full proof-of-stake blockchain yet. It is the foundation piece where we learn how to:

- create a wallet
- generate RSA public and private keys
- create a transaction object
- hash transaction data
- sign the transaction
- verify the signature

If you want the higher-level flow and architecture diagrams, see `PROJECT_ARCHITECTURE.md`.

## What We Are Building

We are building a small cryptographic transaction demo.

The flow is:

1. Create a wallet
2. Create a transaction
3. Remove the signature field from the transaction payload
4. Hash the payload
5. Sign the hash with the sender's private key
6. Store the signature in the transaction
7. Verify that the signature matches the sender's public key

In blockchain systems, we usually identify accounts by public keys instead of human-readable names.

## Final Project Structure

By the end, your project will look like this:

```text
proof_of_stake/
|-- BlockchainUtils.py
|-- Main.py
|-- Transaction.py
|-- Wallet.py
|-- PROJECT_ARCHITECTURE.md
|-- README.md
|-- requirements.txt
`-- resources/
```

## Step 1: Create the Project Folder

Create a new folder and move into it:

```powershell
mkdir proof_of_stake
cd proof_of_stake
```

## Step 2: Create and Activate a Virtual Environment

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

If you are using Command Prompt instead of PowerShell:

```bat
.venv\Scripts\activate.bat
```

## Step 3: Install the Required Packages

For the current application code, install:

```powershell
pip install pycryptodome rich devtools
```

If you want a `requirements.txt`, create this file:

```txt
jsonpickle==1.4.1
json5==0.8.4
Flask==1.1.1
Flask-Classful==0.14.2
p2pnetwork==0.0.3
requests==2.22.0
pycryptodome==3.23.0
```

Note:
`Main.py` also imports `rich` and `devtools`, so if you want to run the current demo exactly as written, those should be installed too even though they are not listed in the current `requirements.txt`.

## Step 4: Create `BlockchainUtils.py`

This file is responsible for hashing data with SHA-256.

Create `BlockchainUtils.py`:

```python
from Crypto.Hash import SHA256
import json


class BlockchainUtils:

    @staticmethod
    def hash(data):
        dataString = json.dumps(data, sort_keys=True).encode('utf-8')
        dataHash = SHA256.new(dataString)
        return dataHash
```

### Why this file matters

- We need a consistent way to hash transaction data
- `json.dumps(..., sort_keys=True)` makes the payload deterministic
- deterministic formatting is important because the same logical data must always produce the same hash

## Step 5: Create `Transaction.py`

This file defines the transaction object.

Create `Transaction.py`:

```python
import uuid
import time
import copy


class Transaction:
    def __init__(self, senderPublicKey, recipientPublicKey, amount, type):
        self.senderPublicKey = senderPublicKey
        self.recipientPublicKey = recipientPublicKey
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ''

    def toJson(self):
        return self.__dict__

    def sign(self, signature):
        self.signature = signature

    def payload(self):
        jsonRepesentation = copy.deepcopy(self.toJson())
        jsonRepesentation['signature'] = ''
        return jsonRepesentation
```

### Why this file matters

This class stores all transaction data:

- `senderPublicKey`
- `recipientPublicKey`
- `amount`
- `type`
- `id`
- `timestamp`
- `signature`

The most important method is `payload()`.

Why?
Because we do not sign the transaction with its own signature already included. Instead, we create a copy of the transaction and temporarily clear the `signature` field before hashing and signing.

## Step 6: Create `Wallet.py`

This file handles key generation, signing, and signature verification.

Create `Wallet.py`:

```python
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from BlockchainUtils import BlockchainUtils
from Transaction import Transaction


class Wallet:
    def __init__(self, balance=0):
        self.keyPare = RSA.generate(2048)

    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = pkcs1_15.new(self.keyPare).sign(dataHash)
        return signatureSchemeObject.hex()

    @staticmethod
    def signatureValidate(data, signature, publicKeyString):
        signature = bytes.fromhex(signature)
        publicKey = RSA.import_key(publicKeyString)
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = pkcs1_15.new(publicKey)
        try:
            signatureSchemeObject.verify(dataHash, signature)
            return True
        except (ValueError, TypeError):
            return False

    def publicKeyString(self):
        return self.keyPare.publickey().exportKey('PEM').decode('utf-8')

    def createTransaction(self, receiver, amount, type):
        transaction = Transaction(self.publicKeyString(), receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction
```

### Why this file matters

This class does the main cryptographic work.

#### `RSA.generate(2048)`

This creates a 2048-bit RSA keypair for the wallet.

- private key: used to sign data
- public key: shared with others so they can verify signatures

#### `sign(data)`

This method:

1. hashes the payload
2. signs the hash using the wallet's private key
3. returns the signature as a hex string

#### `signatureValidate(data, signature, publicKeyString)`

This method:

1. converts the hex signature back into bytes
2. imports the provided public key
3. hashes the data again
4. verifies the signature with that public key

If the public key belongs to the original signer, validation returns `True`. Otherwise it returns `False`.

#### `createTransaction(receiver, amount, type)`

This method connects everything together:

1. create the transaction
2. build the signable payload
3. sign the payload
4. attach the signature to the transaction
5. return the signed transaction

## Step 7: Create `Main.py`

This file is the entry point of the application.

Create `Main.py`:

```python
from Transaction import Transaction
from Wallet import Wallet
from rich import print
from devtools import debug

if __name__ == "__main__":
    # Example usage of the Transaction class
    sender = "sender_public_key"
    recipient = "recipient_public_key"
    amount = 100
    transaction_type = "transfer"

    wallet = Wallet()
    fraudWallet = Wallet()
    transaction = wallet.createTransaction(recipient, amount, transaction_type)
    signatureValid = wallet.signatureValidate(transaction.payload(), transaction.signature, fraudWallet.publicKeyString())
    print(signatureValid)  # Should print True if the signature is valid
```

### What this script is doing

- `wallet` is the real sender
- `fraudWallet` is another wallet with a different keypair
- the transaction is signed by `wallet`
- the signature is then checked against `fraudWallet`'s public key

Because the signature was not created by `fraudWallet`, the result should actually be `False`.

So the comment in the current code is misleading.

If you change this line:

```python
signatureValid = wallet.signatureValidate(transaction.payload(), transaction.signature, fraudWallet.publicKeyString())
```

to this:

```python
signatureValid = wallet.signatureValidate(transaction.payload(), transaction.signature, wallet.publicKeyString())
```

then the result should be `True`.

## Step 8: Run the Application

Run:

```powershell
python Main.py
```

Expected behavior:

- with `fraudWallet.publicKeyString()`, output should be `False`
- with `wallet.publicKeyString()`, output should be `True`

## Step 9: Understand the Build Order

If you are teaching or learning this project, the best order is:

1. Build the hashing helper
2. Build the transaction model
3. Build the wallet class
4. Build the entry point
5. Run the demo
6. Test valid and invalid signature verification

This order works well because each file depends on the one before it.

## How All Files Connect

```text
Main.py
  -> uses Wallet.py
Wallet.py
  -> uses Transaction.py
  -> uses BlockchainUtils.py
Transaction.py
  -> provides the transaction payload
BlockchainUtils.py
  -> provides deterministic SHA-256 hashing
```

## What This Project Does Not Do Yet

Right now, this project does not yet include:

- blocks
- blockchain state
- proof-of-stake validator selection
- staking balances
- networking between nodes
- Flask endpoints
- transaction pools
- mining or consensus logic

So think of the current code as the cryptographic base layer for a future blockchain project.

## Suggested Next Steps

Once this part is working, a good next path would be:

1. add a `Block` class
2. add a `Blockchain` class
3. add transaction lists inside blocks
4. add wallet balance tracking
5. load keys from `resources/*.pem`
6. add staking and validator logic
7. expose the node through Flask APIs
8. add peer-to-peer communication

## Reference

- Architecture and diagrams: `PROJECT_ARCHITECTURE.md`
