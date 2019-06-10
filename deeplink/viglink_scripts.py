import requests

api_key = '9d99dbe46c42b6f85f33504b3635c50c'

secret_key = 'c12492de2a6149089c9cb4b180318974ece1bb44'

url = 'http://api.viglink.com/api/click?out={}&key={}&format=txt&cuid={}'

class VigLinkError(Exception):
    pass

def get_viglink_link(net_link, subid):
    try:
        response = requests.get(url.format(net_link, api_key, subid)).json()
        return response
    except:
        raise VigLinkError("Данная партнерская программа не поддерживается")



