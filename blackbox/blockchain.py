from block import Block
import datetime as date
import twitter
import sys
import os

class Blockchain:
  """
  This class describes how the Blockchain is designed

  Attributes:
    nChain: The list containing all the blocks
    nDifficulty: The overall difficulty to mine a block, the number reprensents the number of zero's
    needed in front of a hash to mine correctly the block
    api: Twitter's api to connect to Twitter and fetch tweets
    MAX_BLOCK_SIZE: The maximum block size of a block, here set to 1MB
    BLOCK_SIZE: The current block size
  """
  def __init__(self):
    self.nChain = []
    self.nDifficulty = 3
    self.api = ""
    self.MAX_BLOCK_SIZE = 1024000
    self.BLOCK_SIZE = 0
    self.currentFileIndex = 0
    self.genesis(Block(0))
    self.configure()

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
    
  def fetch_data(self):
    """Fetch the tweets from Twitter's API"""
    t = self.api.GetUserTimeline(screen_name="WeiRdCroissant", count=1)
    tweets = [i.AsDict() for i in t]
    for t in tweets:
      if (self.BLOCK_SIZE + sys.getsizeof(t['text'].encode('utf-8')) < self.MAX_BLOCK_SIZE):
        self.BLOCK_SIZE += sys.getsizeof(t['text'].encode('utf-8'))
        return (t['text'].encode('utf-8'))
      return ""
     
  def add_block(self, bNew):
    """Set all the block parameters, mine it and add it to the blockchain"""
    bNew.timestamp = date.datetime.now()
    bNew.data = self.fetch_data()
    bNew.previous_hash = self.get_lastBlock()
    bNew.mine_block(self.nDifficulty)
    self.nChain.append(bNew)
    self.save_blocks(bNew)
    print "Block data: " + bNew.data

  def get_lastBlock(self):
    return self.nChain[-1]

  def save_blocks(self, bNew):
    """Save the new blocks in a blk*.dat file"""
    fileName = "./blackbox/blocks/blk" + str(self.currentFileIndex) + ".dat"
    if (os.path.isfile(fileName)):
      statinfo = os.stat(fileName)
      if (statinfo.st_size < 8000000):
        with open(fileName, "a") as blkfile:
          blkfile.write(bNew.data + '\n')
      else:
        self.currentFileIndex += 1
        fileName = "./blackbox/blocks/blk" + str(self.currentFileIndex) + ".dat"
        with open(fileName, "a") as blkfile:
          blkfile.write(bNew.data + '\n')
    else:
      with open(fileName, "a") as blkfile:
          blkfile.write(bNew.data + '\n')