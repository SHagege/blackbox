#!/usr/bin/env python

from block import Block
from blockchain import Blockchain

def main():
    blockchain = Blockchain()
    index = 0
    while True:
        blockchain.add_block(Block(index))
        index += 1

if __name__ == "__main__":
    main()

