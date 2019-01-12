from block import Block
import datetime as date
import twitter
import sys

class Blockchain:
  api = ""
  nDifficulty = 0
  nChain = []
  MAX_BLOCK_SIZE = 1024
  BLOCK_SIZE = 0

  def __init__(self):
    self.genesis(Block(0))
    self.nDifficulty = 2
    self.configure()

  def configure(self):
    fp = open('config.txt')
    lines = fp.read().split("\n")
    fp.close()
    with open('config.txt') as fp:
      lines = fp.readlines()
    self.api = twitter.Api(consumer_key=lines[0].split('=')[1].strip('\n').strip("'"), 
      consumer_secret=lines[1].split('=')[1].strip('\n').strip("'"),
      access_token_key=lines[2].split('=')[1].strip('\n').strip("'"), 
      access_token_secret=lines[3].split('=')[1].strip('\n').strip("'"))

  def genesis(self, bGen):
    bGen.timestamp = date.datetime.now()
    bGen.previous_hash = 0
    bGen.data = "Genesis Block"
    self.nChain.append(bGen)
    print "Block data: " + bGen.data
    
  def fetch_data(self):
    t = self.api.GetUserTimeline(screen_name="WeiRdCroissant", count=1)
    tweets = [i.AsDict() for i in t]
    for t in tweets:
      if (self.BLOCK_SIZE + sys.getsizeof(t['text'].encode('utf-8')) < self.MAX_BLOCK_SIZE):
        self.BLOCK_SIZE += sys.getsizeof(t['text'].encode('utf-8'))
        return (t['text'].encode('utf-8'))
      return ""
     
  def add_block(self, bNew):
        print self.BLOCK_SIZE
        bNew.timestamp = date.datetime.now()
        bNew.data = self.fetch_data()
        bNew.previous_hash = self.get_lastBlock()
        bNew.mine_block(self.nDifficulty)
        self.nChain.append(bNew)
        print "Block data: " + bNew.data

  def get_lastBlock(self):
    return self.nChain[-1]
