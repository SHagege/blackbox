import hashlib as hasher
import datetime as date

class Block:
    """
    This class describes what a block contains and functions to mine them

    Attributes:
        index: The index of the block
        timestamp: When the block was created
        data: Which data is put in the block
        previous_hash: The hash from the last block
        nonce: How many times the system had to mine to find the correct hash
        hash: The hash of the block
    """

    def __init__(self, index):
        self.index = index
        self.timestamp = ""
        self.data = ""
        self.previous_hash = ""
        self.nonce = 0
        self.hash = self.hash_block()

    def hash_block(self):
        """Take all the block's attributes and create a unique hash (SHA256)"""
        sha = hasher.sha256()
        sha.update(str(self.index) + str(self.timestamp) + 
        str(self.data) + str(self.previous_hash) + str(self.nonce))
        return sha.hexdigest()

    def mine_block(self, nDifficulty):
        """Create the difficulty (i.e how many zero's need to be in front of the hash)
        and loop through hash_block until the system finds the correct hash"""
        cstr = [0] * nDifficulty
        cstr[nDifficulty - 1] = '\0'
        difficulty = "".join(str(x) for x in cstr)
        while ((self.hash[0:nDifficulty - 1].strip('\0')) != difficulty.strip('\0')):
            self.nonce += 1
            self.hash = self.hash_block()
        print "Block mined: " + self.hash