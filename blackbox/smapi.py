import twitter
import instagram

class Smapi:
    """
    Social Media class, read config file and setup Twitter and Instagram API's
    """
    def __init__(self):
        self.apiTwitter = None
        self.apiInstagram = None
        self.configure()

    def configure(self):
        """Read the config file to get user's credentials and connect to Twitter's API"""
        fp = open('config.txt')
        lines = fp.read().split("\n")
        fp.close()
        with open('config.txt') as fp:
            lines = fp.readlines()
        self.apiTwitter = twitter.Api(consumer_key=lines[0].split('=')[1].strip('\n').strip("'"), 
            consumer_secret=lines[1].split('=')[1].strip('\n').strip("'"),
            access_token_key=lines[2].split('=')[1].strip('\n').strip("'"), 
            access_token_secret=lines[3].split('=')[1].strip('\n').strip("'"))