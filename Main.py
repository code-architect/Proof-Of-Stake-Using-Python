from Transaction import Transaction

if __name__ == "__main__":
    # Example usage of the Transaction class
    sender = "sender_public_key"
    recipient = "recipient_public_key"
    amount = 100
    transaction_type = "transfer"

    transaction = Transaction(sender, recipient, amount, transaction_type)
    print(f"Transaction ID: {transaction.id}")
    print(f"Timestamp: {transaction.timestamp}")
    print(f"Signature: {transaction.signature}")
    print(f"Sender: {transaction.senderPublicKey}")
    print(f"Recipient: {transaction.recipientPublicKey}")
    print(f"Amount: {transaction.amount}")
    print(f"Type: {transaction.type}")