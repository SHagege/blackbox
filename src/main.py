import twitter
import datetime as date
from block import Block
from blockchain import Blockchain

def main():
    blockchain = Blockchain()
    print "Mining block 1..."
    blockchain.add_block(Block(1))
    print "Mining block 2..."
    blockchain.add_block(Block(2))
    print "Mining block 3..."
    blockchain.add_block(Block(3))

if __name__ == "__main__":
    main()

