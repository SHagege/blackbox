# Blackbox

In the recents months we've seen some big privacy and censorship problems coming from Facebook, Twitter and alike social medias.
We can't trust those platforms anymore, as we can't be sure that what we post will stay forever or be suppressed
by those corporations because they don’t like what we've said, or because someone else (e.g., the government) told them to take it down.

Blackbox is a program that uses blockchain to put every single thing an individual do or say on social media on a permisionless blockchain. 
Anyone can join and confirm through proof-of-work that someone said something at some point in time.

## Requirements

- [python-twitter](https://github.com/bear/python-twitter)
- [pyp2p](https://pypi.org/project/py2p/)
- [cryptography](https://pypi.org/project/cryptography/)

## Installing

Run
```
pip3 install -r requirements.txt
```

## Configuration

You'll need to get API access for [Twitter](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)
and [Instagram](https://www.instagram.com/developer/clients/manage/)

Once you have you access tokens, you can edit the config.json file

## Running blackbox

The bin is placed in the bin/ sub-directory. To run in for-ground:
```
./bin/run
```
To list all available options, run `./bin/run --help` 
You need to specify an ip using `--ip`. If you're running on your local machine, use `127.0.0.1`

Running multiple instances of the program will need you to specify a port using `--port`. After launching the first instance
blackbox will tell you which port it's currently using.

## License

Blackbox is available under the MIT license. See the [LICENSE](LICENSE) file for more info.