# Blackbox

There's been some big privacy and censorship problems coming from Facebook, Twitter and alike social medias.

You can't be sure that what you post will stay forever or be suppressed by those companies because they don’t like what you've said, 
or because someone else (e.g., the government) told them to take it down.
There's also more and more individuals trying to delete social media posts because they want to cover something they said at some point
in time.

Blackbox put everything an individual do or say on social media on a permisionless blockchain built from scratch.
Anyone can join and confirm through proof-of-work that someone said something at some point in time. 
It's censorship resistant, and act as a great surveillance tool for malicious individuals.

## Requirements

- [Kademlia](https://github.com/bmuller/kademlia)
- [Django](https://github.com/django/django)
- [Bulma](https://github.com/jgthms/bulma)
- [python-twitter](https://github.com/bear/python-twitter)

## Installation

Run in the root directory
```
./setup.sh
```

## Configuration

You'll need to get API access for [Twitter](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)
and [Instagram](https://www.instagram.com/developer/clients/manage/).

Once you have your access tokens, you can edit the config.json file.

## Kademlia
Blackbox utilizes the [Kademlia Protocol](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf). Kademlia is a distributed
hash table for building decentralized peer-to-peer networks (used in well known products like [BitTorrent](https://en.wikipedia.org/wiki/BitTorrent) or [Ethereum](https://www.ethereum.org/)).

## Block Explorer
Blackbox's block explorer is built using [Django](https://www.djangoproject.com/). You can run your own server instance by running at the root directory
`python3 explorer/manage.py runserver`.

By default the explorer is available at `127.0.0.1:8000`.

## Running blackbox

The bin is placed in the `bin/` sub-directory. To run in for-ground:
```
./bin/run
```
To list all available options, run `./bin/run --help` .
You need to specify an ip using `--ip`. If you're running on your local machine, use `127.0.0.1`.

Running multiple instances of the program will need you to specify a port using `--port`. After launching the first instance
blackbox will tell you which port it's currently using. Solo mining is a posibility but defeats the main purpose of a decentralized network. 

All the data is stored in `blackbox/blocks/` into `blk*.dat` files. How they are stored is similar to [Bitcoin](http://learnmeabitcoin.com/glossary/blkdat)'s approach.
Blocks start with a magic byte, the block header, each social media ID alongside the data inside it encoded in base64.

## License

Blackbox is available under the MIT license. See the [LICENSE](LICENSE) file for more info.