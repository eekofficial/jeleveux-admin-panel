import requests

signature = '05e2685fc7'

url = 'http://jlvx.ru/yourls-api.php'

class JLVXLinkError(Exception):
    pass

def get_short_link(link):
    try:
        params = {
            'signature': signature,
            'action': 'shorturl',
            'format': 'json',
            'url': link
        }
        response = requests.get(url, params).json()
        short_url = response['shorturl']
        return short_url
    except:
        raise JLVXLinkError

