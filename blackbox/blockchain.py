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
    self.MainNode = False
    self.sm = Smapi()
    self.Node = self.startNode()
    self.gossip()
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
      return sock
    else:
      self.MainNode = True
      sock.connect(self.ip, self.openingPort)
      return sock

  def gossip(self):
    """Every X seconds this thread will listen to any blocks this node receives
    and add it or not to the blk*.dat file depending if the smdata has already been
    added by other nodes"""
    threading.Timer(1.0, self.gossip).start()
    msg = self.Node.recv()
    if msg:
      if (self.blockHeight == 0):
        self.blockHeight = int(msg.packets[2][0])
        return
      fileName = "./blackbox/blocks/blk" + str(self.currentFileIndex) + ".dat"
      if (os.path.isfile(fileName)):
        statinfo = os.stat(fileName)
        if (statinfo.st_size < 8000000):
          with open(fileName, "r+") as blkfile:
            for smdataID in msg.packets[1]:
              if smdataID in blkfile.read():
                print ("Not adding MainNode faster")
                self.blockHeight = int(msg.packets[2])
                return False
              else:
                print("Adding MainNode late")
                blkfile.write(str(msg) + '\n')
                self.blockHeight = int(msg.packets[2])
                return True
    return False

  def genesis(self, bGen):
    """Create the genesis block of the blockchain"""
    bGen.timestamp = date.datetime.now()
    bGen.previous_hash = 0
    bGen.data.append("genesis_block")
    self.add_block(bGen)
    
  def run(self):
    while True:
      if (self.MainNode == True):
        while True:
          self.fill_block(Block(self.blockHeight))
      if (self.blockHeight != 0):
        self.blockHeight += 1
        while True:
          self.fill_block(Block(self.blockHeight))

  def mempoolHandling(self):
    """Starts a new thread that will handle the memory pool, putting inside it every X seconds Y 
    tweets from a social media account"""
    threading.Timer(30.0, self.mempoolHandling).start()
    t = self.sm.apiTwitter.GetUserTimeline(screen_name=self.account, count=20)
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
    goss = self.gossip()
    if goss is False:
      self.save_blocks(bNew)
    else:
      bNew.blockFound = True
    if self.port is not None and goss is True:
      return
    print(colored("Block " + str(bNew.height) + " content: ", "green") + bNew.content)
    self.Node.send(bNew.data, str(self.blockHeight))
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