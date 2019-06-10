import requests

BOT_TOKEN = '839788663:AAH27x33UCfsiWyyP8DJSBVqjYjOyrd4gv4'

url = 'https://api.telegram.org/bot{}/sendPhoto'

photo_channel = '@photoforchannel'
channel = '@jeleveuxtest'

class TGPhotoError(Exception):
    pass

class TGPostError(Exception):
    pass

def upload_tg_photo(photo_data):
    try:
        data = {
            "chat_id": photo_channel
        }
        response = requests.post(url=url.format(BOT_TOKEN), data=data, files={'photo': photo_data}).json()
        return response['result']['photo'][0]['file_id']
    except:
        raise TGPhotoError

def send_tg_post(message, photo_data):
    try:
        data = {
            "chat_id": channel,
            "caption": message,
            "parse_mode": "HTML",
            "photo": photo_data
        }
        response = requests.post(url=url.format(BOT_TOKEN), data=data).json()
        return response
    except:
        raise TGPostError
