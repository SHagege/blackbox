import hashlib
import calendar
import time
import datetime as date

class Smdata:
    def __init__(self, data):
        self.smdataID = None
        self.data = data
        self.generate_smadataID()

    def generate_smadataID(self):
        timestamp = calendar.timegm(time.gmtime())
        sha = hashlib.sha256(str(timestamp).encode('utf-8') + 
        str(self.data).encode('utf-8'))
        dsha = hashlib.sha256()
        sha.hexdigest()
        dsha.update(sha.digest())
        self.smdataID = dsha.hexdigest()