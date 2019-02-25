import twitter
import json

class Smapi:
    """
    Social Media class, read config file and setup Twitter and Instagram API's

    Attributes:
       apiTwitter: Twitter API
       apiInstagram: Instagram API
    """
    def __init__(self):
        self.apiTwitter = None
        self.apiInstagram = None
        self.configure()

    def configure(self):
        """Read config file and set the Twitter API"""
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        self.apiTwitter = twitter.Api(consumer_key=data["twitter"]["consumer_key"],
            consumer_secret=data["twitter"]["consumer_secret"],
            access_token_key=data["twitter"]["access_token_key"],
            access_token_secret=data["twitter"]["access_token_secret"])