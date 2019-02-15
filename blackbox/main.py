import datetime
import argparse

from termcolor import colored

from .blockchain import Blockchain

parser = argparse.ArgumentParser(description='Blackbox "Alpha One" (v0.1.0-release)')
parser.add_argument("--ip", required=True, help='The ip you want to connect to')
parser.add_argument("--port", required=False, help='The port associated with the daemon')
opts = parser.parse_args()

def welcome():
    print(str(datetime.datetime.now()) + "\nThis is the command line blackbox project.\nBlackbox 'Alpha One' (v0.1.0-release)")
    print(colored("Specify social media name (e.g., jack)", "yellow"))
    account = input('> Social media name (or Ctrl-C to quit): ')
    print(colored("You chose " + account + """\n******************************************************************************\n""" +
    "Mining process starting", "green"))
    return account

def main():
    account = welcome()
    Blockchain(account, opts.port, opts.ip)
    
if __name__ == "__main__":
    main()

