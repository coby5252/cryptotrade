import requests
import logging as log

class AbstractGeminiRequest(object):
    """
    Base class for all Gemini API Requests.
    """

    def __init__(self, base_url = None, path = None, port = None, 
                 headers = None, auth = None, verify = None, key = None):

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

    def call():
        """
        This method must be implemented by any class that extends this one.this
        """
        pass


x = AbstractGeminiRequest()