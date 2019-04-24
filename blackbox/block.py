import hashlib
import calendar
import time
import datetime as date
from datetime import datetime
import os
import sys
import json
import asyncio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "explorer.settings")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/explorer"
sys.path.append(BASE_DIR)
import django
django.setup()

from blocks.models import BlockModel

class Block:
    """
    This class describes what a block contains and functions to mine them

    Args:
        height: The height of the block
        merkleTree: hash of all the hash of the data inside the block
        nDifficulty: The difficulty of the current block
        timestamp: When the block was created
        data: Which data is put in the block
        previous_hash: The hash from the last block
        nonce: How many times the system had to mine to find the correct hash
        BLOCK_SIZE: The current size of the block
        content: The content of the block
        block_header: The hash of the block
    """

    def __init__(self, height, difficulty):
        """
        Create a new block

        Args:
            height: The height at which the block needs to be created 
        """
        self.height = height
        self.merkleTree = None
        self.nDifficulty = difficulty
        self.timestamp = 0
        self.data = []
        self.previous_hash = None
        self.nonce = 0
        self.BLOCK_SIZE = 0
        self.blockFound = False
        self.content = None
        self.block_header = self.proof_of_work()

    def proof_of_work(self):
        """Hash the block by doing a double SHA256 encoding with the block's attributes"""
        sha = hashlib.sha256(str(self.height).encode('utf-8') + 
        str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8') + str(self.nonce).encode('utf-8') + str(self.nDifficulty).encode('utf-8'))
        dsha = hashlib.sha256()
        sha.hexdigest()
        dsha.update(sha.digest())
        return dsha.hexdigest()

    def mine_block(self, node):
        """Do a proof-of-work until the hash found is lower than the difficulty target
        
        Args:
            node: The node of the blockchain
        """
        target = node.TARGET_MAX / self.nDifficulty
        while (int(self.block_header, 16) > int(target)):
                self.nonce += 1
                self.block_header = self.proof_of_work()
        self.timestamp = calendar.timegm(time.gmtime())
        self.constructFileContent()
        BlockModel.objects.create(block_height=self.height, block_hash=self.block_header, block_size=self.BLOCK_SIZE, 
        timestamp=datetime.utcfromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S'), smdatax_count=len(self.data))
        return self.block_header

    def constructFileContent(self):
        """What is written inside the blk*.dat files"""
        all_data = ""
        magic_bytes = "f9beb4d9"
        dataCount = len(self.data)
        for id_data in self.data:
            all_data += id_data.inFileContent
        self.content = magic_bytes + str(dataCount) + self.block_header + '|' + all_data
