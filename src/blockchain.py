from block import Block
from genesis import genesis
import datetime as date

class Blockchain:
  nDifficulty = 0
  nChain = []
  
  def __init__(self):
    self.nChain = [self.genesis(Block(0))]
    self.nDifficulty = 4

  def genesis(self, bGen):
    bGen.timestamp = date.datetime.now()
    bGen.previous_hash = 0
    bGen.data = "Genesis Block"
    return bGen

  def add_block(self, bNew):
        bNew.previous_hash = self.get_lastBlock()
        bNew.timestamp = date.datetime.now()
        bNew.data = "Hey! I'm block " + str(bNew.index)
        bNew.mine_block(6)
        self.nChain.append(bNew)

  def get_lastBlock(self):
    return self.nChain[-1]
