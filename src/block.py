import hashlib as hasher
import datetime as date

class Block:
    timestamp = ""
    data = ""
    previous_hash = ""
    nonce = 0
    def __init__(self, index):
        self.index = index
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce))
        return sha.hexdigest()

    def mine_block(self, nDifficulty):
        cstr = [0] * nDifficulty
        cstr[nDifficulty - 1] = '\0'
        difficulty = "".join(str(x) for x in cstr)
        while ((self.hash[0:nDifficulty - 1].strip('\0')) != difficulty.strip('\0')):
            self.nonce += 1
            self.hash = self.hash_block()
        print "Block mined: " + self.hash