from dotenv import load_dotenv
from PIL import Image
import requests
import random
import os


def download_comic():
    comic_num = random.randint(1, Num_of_all_comics)
    filename = f'random_comic_num{comic_num}.png'
    url = f'https://xkcd.com/{comic_num}/info.0.json'
    response_json = response.json()
    response = requests.get(url)
    response.raise_for_status()
    image_url = response_json['img']
    image = requests.get(image_url)
    image.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(image.content)
    authors_comment = response_json['alt']
    return authors_comment, filename


def get_servers_address(access_token):
    params = {
        'access_token': access_token,
        'v': '5.131', 
    }
    response = requests.get(f'https://api.vk.com/method/photos.getWallUploadServer', params=params)
    response.raise_for_status()
    response_json = response.json()
    upload_url = response_json['response']['upload_url']
    return upload_url


def upload_comic_to_server(filename, server_address):
    with open(filename, "rb") as file:
        files = {
            'photo': file,
        }
        response = requests.post(server_address, files=files)
    response.raise_for_status()
    response_json = response.json()
    photo = response_json['photo']
    picture_hash = response_json['hash']
    server = response_json['server']
    return server, photo, picture_hash


def save_comic_in_group_album(server, photo, picture_hash, access_token):
    files = {
    'access_token': (access_token),
    'photo': (photo),
    'server': (server),
    'hash': (picture_hash),
    'v': ('5.131')
    }
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', files=files)
    response.raise_for_status()
    response_json = response.json()
    owner_id = response_json['response'][0]['owner_id']
    photo_id = response_json['response'][0]['id']
    return owner_id, photo_id


def publish_comic_on_wall(authors_comment, filename, photo, owner_id, photo_id, group_id, access_token):
    files = {
    'access_token': (access_token),
    'attachments': (f'photo{owner_id}_{photo_id}'),
    'message': (authors_comment),
    'v': ('5.131'),
    'from_group': ('1'),
    'group_id': (group_id),
    'owner_id': (f'-{group_id}'),
    }
    response = requests.post('https://api.vk.com/method/wall.post', files=files)
    response.raise_for_status()

if __name__ == '__main__':
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']
    group_id = os.environ['VK_GROUP_ID']
    Num_of_all_comics = 2842
    try:
        authors_comment, filename = download_comic()
        group_id = get_groups_id()
        client_id = os.environ['VK_CLIENT_ID']
        server_address = get_servers_address(access_token)
        server, photo, picture_hash = upload_comic_to_server(filename, server_address)
        owner_id, photo_id = save_comic_in_group_album(server, photo, picture_hash, access_token)
        publish_comic_on_wall(authors_comment, filename, photo, owner_id, photo_id, group_id, access_token)
    finally:
        os.remove(filename)