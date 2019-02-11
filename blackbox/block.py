import hashlib
import calendar
import time
import datetime as date

class Block:
    """
    This class describes what a block contains and functions to mine them

    Attributes:
        height: The height of the block
        merkleTree: hash of all the hash of the data inside the block
        nDifficulty: The difficulty of the current block
        timestamp: When the block was created
        data: Which data is put in the block
        prevhash: The hash from the last block
        nonce: How many times the system had to mine to find the correct hash
        BLOCK_SIZE: The current size of the block
        hash: The hash of the block
    """

    def __init__(self, height):
        self.height = height
        self.merkleTree = None
        self.nDifficulty = 5
        self.timestamp = 0
        self.data = []
        self.prevhash = None
        self.nonce = 0
        self.BLOCK_SIZE = 0
        self.hash = self.hash_block()

    def hash_block(self):
        """Hash the block by doing a double SHA256 encoding with the block's attributes"""
        self.timestamp = calendar.timegm(time.gmtime())
        sha = hashlib.sha256(str(self.height).encode('utf-8') + str(self.timestamp).encode('utf-8') + 
        str(self.data).encode('utf-8') + str(self.prevhash).encode('utf-8') + str(self.nonce).encode('utf-8') + str(self.nDifficulty).encode('utf-8'))
        dsha = hashlib.sha256()
        sha.hexdigest()
        dsha.update(sha.digest())
        return dsha.hexdigest()

    def mine_block(self):
        """Create the difficulty (i.e how many zero's need to be in front of the hash)
        and loop through hash_block until the system finds the correct hash"""
        cstr = [0] * self.nDifficulty
        cstr[self.nDifficulty - 1] = '\0'
        difficulty = "".join(str(x) for x in cstr)
        while ((self.hash[0:self.nDifficulty - 1].strip('\0')) != difficulty.strip('\0')):
            self.nonce += 1
            self.hash = self.hash_block()

    def print_block_content(self):
        print(self.data)

    def formating(self):
        magic_number = "0xD9B4BEF9"
        size = 0

