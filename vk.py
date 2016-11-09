import requests
import json
import time
import random

vk_api = 'https://api.vk.com/method/'

HELLO_MESSAGE = 'Hello! I am Sora, the Playlist Bot.\n' \
                'If you wanna create playlist = write "/create" (I`ll help you)\n' \
                'More features soon!'

PLAYLIST_NAMING = 'Send me your playlist NAME.'


def anti_flood(msg) -> str:
    return msg + '\u200B' * random.randint(1, 100)


class Client:
    def __init__(self, token, audio_token, group_id):
        self.token = token
        self.creator_token = audio_token
        self.group_id = group_id

    def __request__(self, method, payload):
        time.sleep(0.34)
        r = requests.get(vk_api + method, params=payload)

        if r.status_code != 200:
            print('Invalid request "' + method + '". code:', r.status_code, '\nval:', r.text)
            return None

        d = json.loads(r.text)

        if d.get('error', False):
            print(method, 'Invalid params:', d)
            return None

        return d

    def get_unread_messages(self) -> list:

        payload = {
            'access_token': self.token,
            'count': 200,
        }

        d = self.__request__('messages.get', payload)
        if d is None:
            return d

        return [el for el in d['response'][1:] if el['read_state'] != 1]

    def send_message(self, uid, message):
        p = {
            'access_token': self.token,
            'peer_id': uid,
            'message': anti_flood(message),
            'v': '5.38'
        }
        d = self.__request__('messages.send', p)
        if d is None:
            return False

        return True

    def create_playlist(self, name) -> int:
        p = {
            'access_token': self.creator_token,
            'title': name,
            'group_id': self.group_id
        }
        r = self.__request__('audio.addAlbum', p)
        if r is None:
            return r

        return r['response']['album_id']

    def add_track(self, album_id, track_id, owner_id):
        p = {
            'access_token': self.creator_token,
            'album_id': album_id,
            'audio_id': track_id,
            'owner_id': owner_id,
            'group_id': self.group_id
        }

        r = self.__request__('audio.add', p)
        if r is None:
            return False

        return True
