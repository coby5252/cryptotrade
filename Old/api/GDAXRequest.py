import os
import requests
import time
import configparser
import base64
import hmac
import hashlib
import json

class GDAXRequest(object):
    """
    Client that will make requests to GDAX
    """

    def __init__(self):
        config_file = os.path.join(os.path.dirname(__file__), 'settings.config')
        config = configparser.ConfigParser()
        config.read(config_file)
        self.url = config['GDAX_API_SETTINGS']['url']
        self.api_key = config['GDAX_API_SETTINGS']['api_key']
        self.api_secret = config['GDAX_API_SETTINGS']['api_secret']


    def _timestamp(self):
        return str(time.time())


    def _auth(self):
        