class Block:
    """
    Block is  a storage container
    """
    
    def __init__(self, hight, blockSize, blockHeader, txCount, txs):
        self.hight = hight
        self.blockSize = blockSize
        self.blockHeader = blockHeader
        self.txCount = txCount
        self.txs = txs
       