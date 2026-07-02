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