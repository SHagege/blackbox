from block import Block
import datetime as date
from smapi import Smapi
from smdata import Smdata
import threading
import twitter
import instagram
import sys
import os

class Blockchain:
  """
  This class describes how the Blockchain is designed

  Attributes:
    blockHeight: The height of the highest block
    nChain: The list containing all the blocks
    MAX_BLOCK_SIZE: The maximum block size of a block, here set to 1MB
    currentFileIndex: The current index of the files where the blocks are saved
    mempool: Temporary list of unconfirmed social media data, keep track of transactions
    that are known to the network but are not yet included in the blockchain
  """
  def __init__(self):
    self.blockHeight = 1
    self.nChain = []
    self.MAX_BLOCK_SIZE = 1024
    self.currentFileIndex = 0
    self.mempool = []
    self.sm = Smapi()
    self.genesis(Block(0))
    self.run()

  def genesis(self, bGen):
    """Create the genesis block of the blockchain with nothing in it"""
    bGen.timestamp = date.datetime.now()
    bGen.previous_hash = 0
    bGen.data = "Genesis Block"
    self.add_block(bGen)
    
  def run(self):
    """"""
    self.mempoolHandling()
    while True:
      self.fill_block(Block(self.blockHeight))

  def mempoolHandling(self):
    """Starts a new thread that will handle the memory pool, putting inside it every X seconds Y 
    tweets from a social media account"""
    threading.Timer(14.0, self.mempoolHandling).start()
    t = self.sm.apiTwitter.GetUserTimeline(screen_name="NESbot_feed", count=10)
    tweets = [i.AsDict() for i in t]
    for t in tweets:
      self.mempool.append(Smdata(t['text'].encode('utf-8')))

  def fill_block(self, bNew):
    """Fetch the tweets from Twitter's API"""
    while self.mempool:
      smdata = self.mempool.pop(0)
      if (bNew.BLOCK_SIZE + sys.getsizeof(smdata) < self.MAX_BLOCK_SIZE):
        bNew.data.append(smdata.data)
        bNew.BLOCK_SIZE += sys.getsizeof(smdata.data)
        if not self.mempool:
          self.add_block(bNew)
      else:
        self.mempool.append(smdata)
        self.add_block(bNew)
        self.fill_block(Block(self.blockHeight))

  def add_block(self, bNew):
    """Block is full, meaning it needs to be mined and added to the blockchain"""
    bNew.previous_hash = self.get_lastBlock()
    bNew.mine_block()
    self.nChain.append(bNew)
    self.save_blocks(bNew)
    self.blockHeight += 1
    print "Block's hash: " + bNew.hash

  def get_lastBlock(self):
    if self.nChain:
      return self.nChain[-1]
    return None

  def save_blocks(self, bNew):
    """Save the new blocks in a blk*.dat file"""
    fileName = "./blackbox/blocks/blk" + str(self.currentFileIndex) + ".dat"
    if (os.path.isfile(fileName)):
      statinfo = os.stat(fileName)
      if (statinfo.st_size < 8000000):
        with open(fileName, "a") as blkfile:
          blkfile.write("Block height: " + str(bNew.height) + " Block hash: " + bNew.hash + " Timestamp " + str(bNew.timestamp) + '\n')
          for item in bNew.data:
            blkfile.write("%s\n" % item)
      else:
        self.currentFileIndex += 1
        fileName = "./blackbox/blocks/blk" + str(self.currentFileIndex) + ".dat"
        with open(fileName, "a") as blkfile:
          blkfile.write("Block height: " + str(bNew.height) + " Block hash: " + bNew.hash + " Timestamp " + str(bNew.timestamp) + '\n')
          for item in bNew.data:
            blkfile.write("%s\n" % item)
    else:
      with open(fileName, "a") as blkfile:
          blkfile.write("Block height: " + str(bNew.height) + " Block hash: " + bNew.hash + " Timestamp " + str(bNew.timestamp) + '\n')
          for item in bNew.data:
            blkfile.write("%s\n" % item)