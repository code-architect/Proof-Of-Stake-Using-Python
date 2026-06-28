from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from BlockchainUtils import BlockchainUtils

class Wallet:
    def __init__(self, balance=0):
        self.keyPare = RSA.generate(2048)

    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = pkcs1_15.new(self.keyPare).sign(dataHash)
        return signatureSchemeObject.hex()