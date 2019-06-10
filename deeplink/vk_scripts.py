import requests
import re
ACCESS_TOKEN = '92ee55e0ea487f17cf35f03d74ab66d0e1e3cacef0f6866285002edb48050efbb8052ba54e98365dd4d32'

VERSION_API = '5.95'

#id группы vk
OWNER_ID = '-158372227'

class VKPhotoError(Exception):
    pass

class VKPostError(Exception):
    pass

def clean_html(html_text):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', html_text)
    return cleantext

def get_upload_url():
    response = requests.get('https://api.vk.com/method/photos.getUploadServer?&album_id={}&access_token={}&v={}'.format('265319960', ACCESS_TOKEN, VERSION_API)).json()
    return response['response']['upload_url']

def upload_file(photo_data):
    response = requests.post(get_upload_url(), files={'file1': photo_data}).json()
    return response

def save_photo(photo_data):
    try:
        file_params = upload_file(photo_data)
        response = requests.get('https://api.vk.com/method/photos.save?&album_id={}&server={}&photos_list={}&hash={}&access_token={}&v={}'.format('265319960', file_params['server'], file_params['photos_list'], file_params['hash'], ACCESS_TOKEN, VERSION_API)).json()
        photo_info = 'photo{}_{}'.format(response['response'][0]['owner_id'], response['response'][0]['id'])
        return photo_info
    except:
        raise VKPhotoError

def send_vk_post(message, photo_data):
    try:
        response = requests.get('https://api.vk.com/method/wall.post?owner_id={}&message={}&attachments={}&access_token={}&v={}'.format(OWNER_ID, message, photo_data, ACCESS_TOKEN, VERSION_API)).json()
        return response['response']['post_id']
    except:
        raise VKPostError

