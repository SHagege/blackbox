import datetime as date
from block import Block

def genesis():
    return Block(0, date.datetime.now(), "Genesis", "0")