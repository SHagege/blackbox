import sys
import os
import time
import threading
import datetime as date
from datetime import timedelta
from random import randint
import asyncio

from termcolor import colored

from .block import Block
from .smapi import Smapi
from .smdata import Smdata
from .node import Node


class Blockchain:
    """This class describes how the Blockchain is designed

    Attributes:
      blockHeight: The height of the highest block
      MAX_BLOCK_SIZE: The maximum block size of a block, here set to 1MB
      currentFileIndex: The current index of the files where the blocks are saved
      mempool: Temporary list of unconfirmed social media data, keep track of transactions
      that are known to the network but are not yet included in the blockchain
      account: The social media account to monitor
    """

    def __init__(self, account, port, ip):
        """Creates a blockchain instance

        Args:
            account: The Twitter account you wish to monitor
            port: The port you wish to bootstrap to
            ip: The ip you wish to connect to
        """
        self.MAX_BLOCK_SIZE = 4096
        self.currentFileIndex = 0
        self.openingPort = 0
        self.difficulty = 1
        self.mempool = []
        self.chains_of_blocks = []
        self.account = account
        self.last_block_hash = None
        self.sm = Smapi()
        self.Node = Node(port, ip)
        self.mempoolHandling()
        self.run()

    def set_difficulty(self):
        """Set the difficulty on the network based on how much time has been elapsed between a certain
        amount of blocks"""
        if len(self.chains_of_blocks) > 10:
            average_block_time = 0
            expected_block_time = 14
            for block in range(1, 9):
                average_block_time = average_block_time + (self.chains_of_blocks[-block+1] - self.chains_of_blocks[-block])
            average_block_time = average_block_time / 10
            self.difficulty = self.difficulty * expected_block_time / average_block_time

    def genesis(self, bGen):
        """Create the genesis block of the blockchain"""
        bGen.timestamp = date.datetime.now()
        bGen.previous_hash = 0
        bGen.data.append("genesis_block")
        self.add_block(bGen)

    def run(self):
        while True:
            if (self.Node.block_height % 10 == 0):
                self.set_difficulty()
            if self.Node.nodes_connected is True:
                self.Node.block_height = self.Node.loop.run_until_complete(
                    self.Node.node.get("block_height"))
            self.fill_block(Block(self.Node.block_height, self.difficulty))

    def mempoolHandling(self):
        """Starts a new thread that will handle the memory pool, putting inside it every X seconds Y 
        tweets from a social media account"""
        threading.Timer(60.0, self.mempoolHandling).start()
        t = self.sm.apiTwitter.GetUserTimeline(
            screen_name=self.account, count=10)
        tweets = [i.AsDict() for i in t]
        for t in tweets:
            smdata = Smdata(t['text'])
            self.mempool.append(smdata)

    def fill_block(self, bNew):
        """Fetch the tweets from Twitter's API
        
        Args:
            bNew: The current block
        """
        while self.mempool:
            smdata = self.mempool.pop(0)
            if (bNew.BLOCK_SIZE + sys.getsizeof(smdata.inFileContent) < self.MAX_BLOCK_SIZE):
                bNew.data.append(smdata)
                bNew.BLOCK_SIZE += sys.getsizeof(smdata.inFileContent)
                if not self.mempool:
                    self.add_block(bNew)
            else:
                self.mempool.append(smdata)
                self.add_block(bNew)
                self.fill_block(Block(self.Node.block_height, self.difficulty))

    def add_block(self, bNew):
        """Block is full, meaning it needs to be mined and added to the blockchain
        
        Args:
            bNew: The current block
        """
        bNew.previous_hash = self.last_block_hash
        block_hash = bNew.mine_block(self.Node)
        self.Node.set_hash(block_hash)
        self.Node.verified_block = False
        verified_block = self.Node.verify(self.difficulty)
        if verified_block is True:
            self.last_block_hash = self.Node.get_last_block()
            self.save_blocks(bNew)
            self.chains_of_blocks.append(bNew)
            print(colored("Block " + str(bNew.height) +
                          " content: ", "green") + bNew.content)
            self.Node.block_height += 1
            for smdata in bNew.data:
                smdata.belong_to_block = bNew.block_header
                smdata.generate_object()
            if self.Node.connecting_port is None:
                asyncio.run_coroutine_threadsafe(self.Node.node.set("verified_block", False), self.Node.loop)
            else:
                self.Node.loop.run_until_complete(self.Node.node.set("verified_block", False))

    def save_blocks(self, bNew):
        """Save the new blocks in a blk*.dat file
        
        Args:
            bNew: The current block
        """
        fileName = "./blackbox/blocks/blk" + \
            str(self.currentFileIndex) + ".dat"
        if (os.path.isfile(fileName)):
            statinfo = os.stat(fileName)
            if (statinfo.st_size < 8000000):
                with open(fileName, "a") as blkfile:
                    blkfile.write(bNew.content + '\n')
            else:
                self.currentFileIndex += 1
                fileName = "./blackbox/blocks/blk" + \
                    str(self.currentFileIndex) + ".dat"
                with open(fileName, "a") as blkfile:
                    blkfile.write(bNew.content + '\n')
        else:
            with open(fileName, "a") as blkfile:
                blkfile.write(bNew.content + '\n')
