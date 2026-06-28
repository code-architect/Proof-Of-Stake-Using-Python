from Crypto.Hash import SHA256
import json

class BlockchainUtils:
    
    @staticmethod
    def hash(data):
        dataString = json.dumps(data, sort_keys=True).encode('utf-8')
        dataHash = SHA256.new(dataString)
        return dataHash
        
        