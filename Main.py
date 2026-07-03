from Transaction import Transaction
from Wallet import Wallet
from rich import print
from devtools import debug
from TransactionPool import TransactionPool

if __name__ == "__main__":
    # Example usage of the Transaction class
    sender = "sender_public_key"
    recipient = "recipient_public_key"
    amount = 100
    transaction_type = "transfer"

    wallet = Wallet()
    pool = TransactionPool()
    transaction = wallet.createTransaction(recipient, amount, transaction_type)
   
    if pool.transactionExists(transaction) == False:
        pool.addTransaction(transaction)
        
    if pool.transactionExists(transaction) == False:
        pool.addTransaction(transaction)
    
    print(pool.transactions)