from block import Block
import datetime as date
import twitter
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
    api: Twitter's api to connect to Twitter and fetch tweets
  """
  def __init__(self):
    self.blockHeight = 1
    self.nChain = []
    self.MAX_BLOCK_SIZE = 1024
    self.currentFileIndex = 0
    self.api = ""
    self.genesis(Block(0))
    self.configure()
    self.run()

  def configure(self):
    """Read the config file to get user's credentials and connect to Twitter's API"""
    fp = open('./config.txt')
    lines = fp.read().split("\n")
    fp.close()
    with open('./config.txt') as fp:
      lines = fp.readlines()
    self.api = twitter.Api(consumer_key=lines[0].split('=')[1].strip('\n').strip("'"), 
      consumer_secret=lines[1].split('=')[1].strip('\n').strip("'"),
      access_token_key=lines[2].split('=')[1].strip('\n').strip("'"), 
      access_token_secret=lines[3].split('=')[1].strip('\n').strip("'"))

  def genesis(self, bGen):
    """Create the genesis block of the blockchain with nothing in it"""
    bGen.timestamp = date.datetime.now()
    bGen.previous_hash = 0
    bGen.data = "Genesis Block"
    self.nChain.append(bGen)
    print "Block data: " + bGen.data
    
  def run(self):
    while True:
      self.fill_block(Block(self.blockHeight))

  def fill_block(self, bNew):
    """Fetch the tweets from Twitter's API"""
    t = self.api.GetUserTimeline(screen_name="WeiRdCroissant", count=2)
    tweets = [i.AsDict() for i in t]
    for t in tweets:
      if (bNew.BLOCK_SIZE + sys.getsizeof(t['text'].encode('utf-8')) < self.MAX_BLOCK_SIZE):
        bNew.BLOCK_SIZE += sys.getsizeof(t['text'].encode('utf-8'))
        bNew.data.append((t['text'].encode('utf-8')))
      else:
        self.add_block(bNew)
    self.add_block(bNew)

  def add_block(self, bNew):
    """Block is full, meaning it needs to be mined and added to the blockchain"""
    bNew.previous_hash = self.get_lastBlock()
    bNew.mine_block()
    self.nChain.append(bNew)
    self.save_blocks(bNew)
    self.blockHeight += 1
    print "Block's hash: " + bNew.hash

  def get_lastBlock(self):
    return self.nChain[-1]

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