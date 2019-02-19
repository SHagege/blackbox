import hashlib
import calendar
import time
import base64
import datetime as date

class Smdata:
    """
    This class represents each piece of social media data

    Attributes:
       smdataID: The ID of the data to find it quickly
       data: The actual raw data
       inFileContent: DataID + data in base64
    """
    def __init__(self, data):
        self.smdataID = None
        self.data = data
        self.inFileContent = None
        self.generate_smadataID()
        self.generate_inFile()

    def generate_smadataID(self):
        """Create a unique dataID through sha256 encoding"""
        timestamp = calendar.timegm(time.gmtime())
        sha = hashlib.sha256(str(timestamp).encode('utf-8') + 
        str(self.data).encode('utf-8'))
        dsha = hashlib.sha256()
        sha.hexdigest()
        dsha.update(sha.digest())
        self.smdataID = dsha.hexdigest()

    def generate_inFile(self):
        """Create what's being printed in the file, mix of dataID + the data in base64"""
        self.inFileContent = self.smdataID + ':' + str(base64.b64encode(bytes(str(self.data),
        'utf-8')).decode('utf-8')) + '/'
        