import requests
import time
import configparser
import base64
import hmac
import hashlib
import json
import logging as log

class GeminiRequest(object):
    """
    Client that will make requests to Gemini
    """

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../settings.config')
        self.url = config['API_SETTINGS']['url']
        self.api_key = config['API_SETTINGS']['api_key']
        self.api_secret = config['API_SETTINGS']['api_secret']


    def _nonce(self):
        return int(time.time()*1000)

    def _sign(self, data):
        j = json.dumps(data)
        j = base64.standard_b64encode(j.encode('utf8'))
        h = hmac.new(str.encode(self.api_secret), j, hashlib.sha384)
        signature = h.hexdigest()
        return {
            "X-GEMINI-APIKEY": self.api_key,
            "X-GEMINI-SIGNATURE": signature,
            "X-GEMINI-PAYLOAD": j
        }


    def getLastPrice(self, coin='ethusd'):
        path = '/v1/pubticker/%s'%(coin)
        response = requests.get(self.url + path)
        return response.json()['last']


    def getPriceSpread(self, coin='ethusd'):
        path = '/v1/pubticker/%s'%(coin)
        response = requests.get(self.url + path)
        return (response.json()['bid'], response.json()['ask'])


    def checkBalances(self):
        path = '/v1/balances'
        data = {
            "request": "/v1/balances",
            "nonce": self._nonce()
        }
        headers = self._sign(data)
        response = requests.post(self.url + path, headers = headers).json()
        usd = [(x['available'], x['availableForWithdrawal'], x['amount']) for x in response if x['currency'] == 'USD'][0]
        eth = [(x['available'], x['availableForWithdrawal'], x['amount']) for x in response if x['currency'] == 'ETH'][0]
        btc = [(x['available'], x['availableForWithdrawal'], x['amount']) for x in response if x['currency'] == 'BTC'][0]
        ret = {
            'USD': {'Available': usd[0], 'Withdrawable': usd[1], 'Total': usd[2]},
            'ETH': {'Available': eth[0], 'Withdrawable': eth[1], 'Total': eth[2]},
            'BTC': {'Available': btc[0], 'Withdrawable': btc[1], 'Total': btc[2]}
        }
        return ret