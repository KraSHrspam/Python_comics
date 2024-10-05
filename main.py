import random
import os

from dotenv import load_dotenv
from PIL import Image
import requests


def download_comic(comics_amount):
    comic_num = random.randint(1, comics_amount)
    filename = f'random_comic_num{comic_num}.png'
    url = f'https://xkcd.com/{comic_num}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()
    response_comics = response.json()

    image_url = response_comics['img']
    image = requests.get(image_url)
    image.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(image.content)
    authors_comment = response_comics['alt']
    return authors_comment, filename


def get_servers_address(access_token):
    params = {
        'access_token': access_token,
        'v': '5.131', 
    }
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=params)
    response.raise_for_status()
    response_server_addres = response.json()
    print(response_server_addres)
    upload_url = response_server_addres['response']['upload_url']
    return upload_url


def upload_comic_to_server(filename, server_address):
    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(server_address, files=files)
    response.raise_for_status()
    response_uploaded_comic = response.json()
    photo = response_uploaded_comic['photo']
    picture_hash = response_uploaded_comic['hash']
    server = response_uploaded_comic['server']
    return server, photo, picture_hash


def save_comic_in_group_album(server, photo, picture_hash, access_token):
    files = {
        'access_token': access_token,
        'photo': photo,
        'server': server,
        'hash': picture_hash,
        'v': '5.131'
    }
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', files=files)
    response.raise_for_status()
    response_saved_comic = response.json()
    owner_id = response_saved_comic['response'][0]['owner_id']
    photo_id = response_saved_comic['response'][0]['id']
    return owner_id, photo_id


def publish_comic_on_wall(authors_comment, filename, photo, owner_id, photo_id, group_id, access_token):
    files = {
        'access_token': access_token,
        'attachments': f'photo{owner_id}_{photo_id}',
        'message': authors_comment,
        'v': '5.131',
        'from_group': '1',
        'group_id': group_id,
        'owner_id': f'-{group_id}',
    }
    response = requests.post('https://api.vk.com/method/wall.post', files=files)
    response.raise_for_status()


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']
    group_id = os.environ['VK_GROUP_ID']
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_amount = response.json()['num']
    try:
        authors_comment, filename = download_comic(comics_amount)
        server_address = get_servers_address(access_token)
        server, photo, picture_hash = upload_comic_to_server(filename, server_address)
        owner_id, photo_id = save_comic_in_group_album(server, photo, picture_hash, access_token)
        publish_comic_on_wall(authors_comment, filename, photo, owner_id, photo_id, group_id, access_token)
    finally:
        os.remove(filename)


if __name__ == '__main__':
    main()