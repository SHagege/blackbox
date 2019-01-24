import hashlib
import datetime as date
import calendar
import time

class Smdata:
    def __init__(self, data):
        self.smdataID = None
        self.data = data
        self.generate_smadataID()

    def generate_smadataID(self):
        timestamp = calendar.timegm(time.gmtime())
        sha = hashlib.sha256(str(timestamp) + 
        str(self.data))
        dsha = hashlib.sha256()
        sha.hexdigest()
        dsha.update(sha.digest())
        self.smdataID = dsha.hexdigest()