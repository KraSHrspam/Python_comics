from dotenv import load_dotenv
from pprint import pprint
from PIL import Image
import requests
import random
import os

load_dotenv()
_ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

def download_comic():
    comic_num = random.randint(1,2842)
    filename = f'random_comic_num{comic_num}.png'
    url = f'https://xkcd.com/{comic_num}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    image_url = response.json()['img']
    image = requests.get(image_url)
    image.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(image.content)
    authors_comment = response.json()['alt']
    return authors_comment, filename


def get_groups_id():
    params = {
        'access_token': _ACCESS_TOKEN,
        'v': '5.131', 
        'filter': 'admin'
    }
    response = requests.get(f'https://api.vk.com/method/groups.get', params=params)
    group_id = response.json()['response']['items'][0]
    response.raise_for_status
    return group_id


def get_servers_address():
    params = {
        'access_token': _ACCESS_TOKEN,
        'v': '5.131', 
    }
    response = requests.get(f'https://api.vk.com/method/photos.getWallUploadServer', params=params)
    response.raise_for_status
    upload_url = response.json()['response']['upload_url']
    return upload_url


def upload_comic_to_server(filename, server_address):
    with open(filename, "rb") as file:
        files = {
            'photo': file,
        }
        response = requests.post(server_address, files=files)
    photo = response.json()['photo']
    picture_hash = response.json()['hash']
    server = response.json()['server']
    response.raise_for_status
    return server, photo, picture_hash


def saveing_comic_in_group_album(server, photo, picture_hash):
    files = {
    'access_token': (None, _ACCESS_TOKEN),
    'photo': (None, photo),
    'server': (None, server),
    'hash': (None, picture_hash),
    'v': (None, '5.131')
    }
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', files=files)
    owner_id = response.json()['response'][0]['owner_id']
    photo_id = response.json()['response'][0]['id']
    response.raise_for_status
    return owner_id, photo_id


def publishing_comic_on_wall(authors_comment, filename, photo, owner_id, photo_id, group_id):
    files = {
    'access_token': (None, _ACCESS_TOKEN),
    'attachments': (None, f'photo{owner_id}_{photo_id}'),
    'message': (None, authors_comment),
    'v': (None, '5.131'),
    'from_group': (None, '1'),
    'group_id': (None, group_id),
    'owner_id': (None, f'-{group_id}'),
    }
    response = requests.post('https://api.vk.com/method/wall.post', files=files)
    response.raise_for_status()

if __name__ == '__main__':
    try:
        load_dotenv()
        authors_comment, filename = download_comic()
        group_id = get_groups_id()
        client_id = os.environ['CLIENT_ID']
        server_address = get_servers_address()
        server, photo, picture_hash = upload_comic_to_server(filename, server_address)
        group_id = get_groups_id()
        owner_id, photo_id = saveing_comic_in_group_album(server, photo, picture_hash)
        publishing_comic_on_wall(authors_comment, filename, photo, owner_id, photo_id, group_id)
    finally:
        os.remove(filename)