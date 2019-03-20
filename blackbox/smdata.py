import hashlib
import calendar
import time
import base64
import datetime as date
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "explorer.settings")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/explorer"
sys.path.append(BASE_DIR)
import django
django.setup()

from smdataxs.models import Smdatax

class Smdata:
    """
    This class represents each piece of social media data

    Attributes:
       smdataID: The ID of the data to find it quickly
       data: The actual raw data
       inFileContent: DataID + data in base64
    """
    def __init__(self, data):
        """Create an smdata instance

        Args:
            data: The data of the smdata (i.e the tweet)
        """
        self.smdataID = None
        self.data = data
        self.belong_to_block = None
        self.inFileContent = None
        self.generate_smadataID()
        self.generate_inFile()

    def generate_smadataID(self):
        """Create a unique dataID through sha256 encoding"""
        sha = hashlib.sha256(str(self.data).encode('utf-8'))
        dsha = hashlib.sha256()
        sha.hexdigest()
        dsha.update(sha.digest())
        self.smdataID = dsha.hexdigest()

    def generate_inFile(self):
        """Create what's being printed in the file, mix of dataID + the data in base64"""
        self.inFileContent = self.smdataID + ':' + str(base64.b64encode(bytes(str(self.data),
        'utf-8')).decode('utf-8')) + '/'
        
    def generate_object(self):
        Smdatax.objects.create(unique_id=self.smdataID, data=self.data, host_block=self.belong_to_block)