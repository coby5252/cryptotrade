import requests
import logging as log

class GeminiRequest(object):
    """
    Class that makes calls to the Gemini API.

    methods:
    
    __init__..............................initialize the current request.  Uses the 
                                          sandbox url, and 'GET' by default for url
                                          and request method.  Other features are 
                                          left blank.
    call..................................execute the current request
    update_headers........................update the headers of the current request
    """

    def __init__(self, request_type = None, base_url = None, path = None, port = None, 
                 headers = None, auth = None, verify = None, key = None, data = None):

        if request_type is None:
            self.request_type = 'GET'
        else:
            self.request_type = request_type

        if base_url is None:
            self.base_url = 'https://api.sandbox.gemini.com'
            log.info('URL Not set.  Using %s by default'%self.base_url)
        else:
            self.base_url = base_url

        if path is None:
            self.path = ''
            log.warning('Path not set.  Request will most likely fail.')
        else:
            self.path = path

        if port is None:
            self.port = ''
        else:
            self.port = port

        if headers is None:
            self.headers = {}
        else:
            self.headers = headers

        if auth is None:
            self.auth = ()
            log.warning('Auth not set.  Request will most likely fail.')
        else:
            self.auth = auth

        if verify is None:
            self.verify = False
        else:
            self.verify = verify

        if key is None:
            self.key = ''
            log.warning('No API key given.  Request will most likely fail.')
        else:
            self.key = key

        if data is None:
            self.data = {}
        else:
            self.data = data

        self.url = '%(url)s/%(path)s' % {'url':self.base_url, 'path':self.path}


    def call(self):
        if self.request_type == 'GET':
            req = requests.get(url = self.url, headers = self.headers)
            req.raise_for_status()
            return req
        elif self.request_type == 'POST':
            req = requests.get(url = self.url, headers = self.headers, data = self.data)
            req.raise_for_status()
            return req
        else:
            raise Exception('Requersts other than GET or POST are not supported')


    def update_headers(self, new_headers):
        self.headers.update(new_headers)


req = GeminiRequest(base_url = 'https://api.gemini.com', path = 'v1/pubticker/ethusd')
response = req.call()
print(response.json())