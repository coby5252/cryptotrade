from GeminiRequest import GeminiRequest as greq

def getLastPrice(coin='ethusd'):
    url = 'https://api.gemini.com'
    path = 'v1/pubticker/%s'%(coin)
    req = greq(base_url = url, path = path)
    response = req.call()
    return response['']


def getPriceSpread(coin='ethusd'):
    url = 'https://api.gemini.com'
    path = 'v1/pubticker/%s'%(coin)
    req = greq(base_url = url, path = path)
    response = req.call()
    return (response['bid'], response['ask'])