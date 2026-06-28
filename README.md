# 1
D:\xampp\htdocs\sand_box\poc\proof_of_stake\Transaction.py
In blockchain world we don't send tokens to human entity with name or address, we use public keys instead,
for now we are only Concentrating on this basic transaction, Where we transfer some token from one account to another account. This is implemented in the Transaction class where sender and recipient public keys are stored along with the amount and type of transaction. But later on we will find out there is a need for a few more types of transactions. To distinguish different kinds of transactions, we introduce these "type" Variable,To know what kind of transaction we are dealing with. 
"self.id" - Unique identifier for each transaction generated using UUID. We are using Python's UUID to create and generate an ID, because coming up with a unique ID every time is impossible for a human to do. 
"self.signature" - Cryptographic signature of the transaction data to verify the authenticity and integrity of the transaction. The signature is used to guarantee that only The owner of a private key is really entitled to create transactions in its name. 
"self.timestamp" - Unix timestamp indicating when the transaction was created, providing chronological order and temporal context.
"self.amount" - The amount of tokens being transferred from the sender to the recipient.
"self.senderPublicKey" - The public key of the sender's account, identifying who is sending the tokens.
"self.recipientPublicKey" - The public key of the recipient's account, identifying who is receiving the tokens.
"self.type" - The type of transaction indicating the category or purpose (e.g., transfer, mint, burn).

"Main.py" - Example usage of the Transaction class demonstrating how to create and initialize a transaction object with sample data.

"toJson" - Method that returns the transaction object as a JSON-serializable dictionary containing all transaction attributes.

# 2
RSA.generate(2048) - Generates a new RSA key pair with a 2048-bit modulus, providing cryptographic security for the wallet's private and public keys.

"D:\xampp\htdocs\sand_box\poc\proof_of_stake\BlockchainUtils.py" - def hash(data):
This can be anything. The data can be anything. It can be a class or a string. That's the reason we need the JSON library, so we can use JSON dump to dump the data. It's kind of like a string representation of the data. 
Then we encode this string to bytes using UTF-8 encoding and compute its SHA256 hash to get a fixed-size, unique identifier for the transaction data.