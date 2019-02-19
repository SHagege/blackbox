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
    account: The social media account to monitor
    ip: The ip to connect to
    port: The port to connect to
  """
  def __init__(self, account, port, ip):
    self.blockHeight = 0
    self.nChain = []
    self.MAX_BLOCK_SIZE = 1024
    self.currentFileIndex = 0
    self.openingPort = 0
    self.mempool = []
    self.account = account
    self.ip = ip
    self.port = port
    self.sm = Smapi()
    self.Node = self.startNode()
    self.sync()
    self.genesis(Block(0))
    self.mempoolHandling()
    self.run()

  def startNode(self):
    """Each blockchain instance is a node which other nodes can connect to
    Each node broadcast new blocks to other nodes"""
    self.openingPort = randint(4000, 5000)
    print("Node operating at " + str(self.openingPort))
    sock = mesh.MeshSocket('0.0.0.0', self.openingPort, prot=base.Protocol('mesh', 'SSL'))
    if self.port:
      sock.connect(self.ip, int(self.port))
    else:
      sock.connect(self.ip, self.openingPort)
    return sock

  def sync(self):
     threading.Timer(10.0, self.sync).start()
     msg = self.Node.recv()
     if msg:
       fileName = "./blackbox/blocks/blk" + str(self.currentFileIndex) + ".dat"
       if (os.path.isfile(fileName)):
         statinfo = os.stat(fileName)
         if (statinfo.st_size < 8000000):
           with open(fileName, "a") as blkfile:
             blkfile.write(str(msg) + '\n')
             self.blockHeight += 1


  def genesis(self, bGen):
    """Create the genesis block of the blockchain with nothing in it"""
    bGen.timestamp = date.datetime.now()
    bGen.previous_hash = 0
    bGen.data.append("genesis_block")
    self.add_block(bGen)
    
  def run(self):
    while True:
      self.fill_block(Block(self.blockHeight))

  def mempoolHandling(self):
    """Starts a new thread that will handle the memory pool, putting inside it every X seconds Y 
    tweets from a social media account"""
    threading.Timer(120.0, self.mempoolHandling).start()
    t = self.sm.apiTwitter.GetUserTimeline(screen_name=self.account, count=10)
    tweets = [i.AsDict() for i in t]
    for t in tweets:
      smdata = Smdata(t['text'])
      self.mempool.append(smdata.inFileContent)

  def fill_block(self, bNew):
    """Fetch the tweets from Twitter's API"""
    while self.mempool:
      smdata = self.mempool.pop(0)
      if (bNew.BLOCK_SIZE + sys.getsizeof(smdata) < self.MAX_BLOCK_SIZE):
        bNew.data.append(smdata)
        bNew.BLOCK_SIZE += sys.getsizeof(smdata)
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
    print(colored("Block " + str(bNew.height) + " content: ", "green") + bNew.content)
    self.Node.send("Block height: " + str(bNew.height) + " Block hash: " + bNew.block_header + " Timestamp " + str(bNew.timestamp) + '\n')
    self.blockHeight += 1

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
          blkfile.write(bNew.content + '\n')
      else:
        self.currentFileIndex += 1
        fileName = "./blackbox/blocks/blk" + str(self.currentFileIndex) + ".dat"
        with open(fileName, "a") as blkfile:
          blkfile.write(bNew.content + '\n')
    else:
      with open(fileName, "a") as blkfile:
          blkfile.write(bNew.content + '\n')