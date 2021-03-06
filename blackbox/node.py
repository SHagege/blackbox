import sys
import os
import time
import asyncio
from threading import Thread
import datetime as date
from random import randint
import logging

from kademlia.network import Server

class Node:
    """This is the object that should be created to start listening 
    as an active node on the network.

    Attributes:
        connecting_port: The port to connect to
        ip: The ip to connect to
        block_height: The height of the blockchain of the node
        nodes: If other nodes are connected or not
        node: The actual node
        loop: The loop tied to the node
        verified_block: Boolean that check if a block_hash is correct or not
    """

    def __init__(self, connecting_port, ip):
        """
        Create a node instance. This will start listening on the given port.

        Args:
            connecting_port: The port to connect to
            ip: The ip to connect to
        """
        self.connecting_port = connecting_port
        self.opening_port = randint(8800, 9000)
        self.TARGET_MAX = 0x0000FFFFFFFFFFFFFFFFFFFFFFF000000000000000000000000000000000000
        self.target = 1
        self.ip = ip
        self.block_height = 0
        self.nodes_connected = None
        self.node = None
        self.loop = None
        self.verified_block = False
        if self.connecting_port is None:
            bootstrap_node = Thread(target=self.bootstrap)
            bootstrap_node.start()
        else:
            self.start_node()
            self.get_blockheight()

    def bootstrap(self):
        """Bootstrap the server by connecting to other known nodes in the network."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
        print("Node operating at " + str(self.opening_port))
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.set_debug(True)
        self.node = Server()
        self.loop.run_until_complete(self.node.listen(self.opening_port))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.node.stop()
            self.loop.close()

    def start_node(self):
        """Each blackbox instance is a node which other nodes can connect to"""
        print("Node operating at " + str(self.opening_port))
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)
        self.node = Server()
        self.loop.run_until_complete(self.node.listen(self.opening_port))
        bootstrap_node = (self.ip, int(self.connecting_port))
        self.loop.run_until_complete(self.node.bootstrap([bootstrap_node]))
        self.loop.run_until_complete(self.node.set("nodes", True))

    def get_blockheight(self):
        """When other nodes join the network they need to start mining at the most
        up-to-date block"""
        block_height = self.loop.run_until_complete(self.node.get("block_height"))
        if self.block_height is None or block_height is None or 0:
            self.get_blockheight()
            return
        if (block_height > self.block_height):
            self.block_height = block_height

    def set_hash(self, block_hash):
        """When a new block is found, sets in the DHT the associated block_hash and block_height
        
        Args:
            block_hash: The hash of the block found by the participating node
        """
        key = "blk" + str(self.block_height)
        if self.connecting_port is None and block_hash is not None:
            asyncio.run_coroutine_threadsafe(self.node.set("block_height", self.block_height + 1), self.loop)
            asyncio.run_coroutine_threadsafe(self.node.set(key, block_hash), self.loop)
        elif block_hash is not None and self.block_height is not 0:
            self.loop.run_until_complete(self.node.set("block_height", self.block_height + 1))
            self.loop.run_until_complete(self.node.set(key, block_hash))

    def get_last_block(self):
        key = "blk" + str(self.block_height)
        if self.connecting_port is None:
            return asyncio.run_coroutine_threadsafe(self.node.get(key), self.loop)
        return self.loop.run_until_complete(self.node.get(key))

    def broadcast(self, hash_broadcasted, difficulty):
        """
        Args:
            hash_broadcasted: The hash that a node broadcasted to the network
            difficulty: The current difficulty on the network
        """
        if self.connecting_port is None:
            hash_broadcasted = hash_broadcasted.result()
        if hash_broadcasted is not None:
            self.target = self.TARGET_MAX / difficulty
            if int(hash_broadcasted, 16) < int(self.target):
                if self.connecting_port is None:
                    asyncio.run_coroutine_threadsafe(self.node.set("verified_block", True), self.loop)
                else:
                    self.loop.run_until_complete(self.node.set("verified_block", True))
                return True
        return False

    def verify(self, difficulty):
        """Verify if a block_hash found by a node is a correct one

        Args:
            difficulty: The current difficulty of the network
        """
        key = "blk" + str(self.block_height)
        if self.connecting_port is None:
            self.nodes_connected = asyncio.run_coroutine_threadsafe(self.node.get("nodes"), self.loop)
            if self.nodes_connected.result() is not True:
                asyncio.run_coroutine_threadsafe(self.node.set("verified_block", True), self.loop)
                return True
            else:
                hash_broadcasted = asyncio.run_coroutine_threadsafe(self.node.get(key), self.loop)
                return (self.broadcast(hash_broadcasted, difficulty))
        else:
            hash_broadcasted = self.loop.run_until_complete(self.node.get(key))
            return (self.broadcast(hash_broadcasted, difficulty))