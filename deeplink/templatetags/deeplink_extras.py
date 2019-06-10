from django import template
import requests

BOT_TOKEN = '839788663:AAH27x33UCfsiWyyP8DJSBVqjYjOyrd4gv4'

register = template.Library()

@register.filter(name='get_photo')
def get_photo(value):
    url = 'https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, value)
    response = requests.get(url).json()
    return 'https://api.telegram.org/file/bot{}/{}'.format(BOT_TOKEN, response['result']['file_path'])
