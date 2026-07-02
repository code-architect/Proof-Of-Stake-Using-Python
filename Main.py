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
    