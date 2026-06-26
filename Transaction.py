import uuid
import time


class Transaction:
    def __init__(self, senderPublicKey, recipientPublicKey, amount, type):
        self.senderPublicKey = senderPublicKey
        self.recipientPublicKey = recipientPublicKey
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ''
        
        







