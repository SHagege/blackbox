import sys
import os
import time
import threading
import datetime as date
from random import randint

from py2p import mesh, base
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
      self.MAX_BLOCK_SIZE = 1024
      self.currentFileIndex = 0
      self.openingPort = 0
      self.mempool = []
      self.account = account
      self.last_block_hash = None
      self.sm = Smapi()
      self.Node = Node(port, ip)
      self.mempoolHandling()
      self.run()

    def genesis(self, bGen):
      """Create the genesis block of the blockchain"""
      bGen.timestamp = date.datetime.now()
      bGen.previous_hash = 0
      bGen.data.append("genesis_block")
      self.add_block(bGen)
      
    def run(self):
      while True:
        self.fill_block(Block(self.Node.block_height))

    def mempoolHandling(self):
      """Starts a new thread that will handle the memory pool, putting inside it every X seconds Y 
      tweets from a social media account"""
      threading.Timer(10.0, self.mempoolHandling).start()
      t = self.sm.apiTwitter.GetUserTimeline(screen_name=self.account, count=5)
      tweets = [i.AsDict() for i in t]
      for t in tweets:
        smdata = Smdata(t['text'])
        self.mempool.append(smdata)

    def fill_block(self, bNew):
      """Fetch the tweets from Twitter's API"""
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
          self.fill_block(Block(self.Node.block_height))

    def add_block(self, bNew):
      """Block is full, meaning it needs to be mined and added to the blockchain"""
      bNew.previous_hash = self.last_block_hash
      block_hash = bNew.mine_block(self.Node)
      self.Node.set_hash(block_hash)
      self.Node.verify()
      if self.Node.verified_block is True:
        self.last_block_hash = self.Node.get_last_block()
        self.save_blocks(bNew)
        print(colored("Block " + str(bNew.height) + " content: ", "green") + bNew.content)
        self.Node.block_height += 1
        self.Node.verified_block = False
        return

    def save_blocks(self, bNew):
      """Save the new blocks in a blk*.dat file"""
      fileName = "./blackbox/blocks/blk" + str(self.currentFileIndex) + ".dat"
      if (os.path.isfile(fileName)):
        statinfo = os.stat(fileName)
        if (statinfo.st_size < 8000000):
          with open(fileName, "a") as blkfile:
            blkfile.write(bNew.content + '\n')
        else:
          self.currentFileIndex += 1
          fileName = "./blackbox/blocks/blk" + str(self.currentFileIndex) + ".dat"
          with open(fileName, "a") as blkfile:
            blkfile.write(bNew.content + '\n')
      else:
        with open(fileName, "a") as blkfile:
            blkfile.write(bNew.content + '\n')