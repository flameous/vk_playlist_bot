STATE_NEW = 'new user'
STATE_PLAYLIST_NAMING = 'choosing name of the playlist'
STATE_PLAYLIST_ADD = 'adding song to playlist'


class User:
    def __init__(self, uid=0, state=""):
        self.id = uid
        self.state = state
        self.tracks = []
        self.playlist_name = ''
        self.pid = 1

    def change_state(self, new):
        self.state = new

    def add_tracks(self, tracks):
        self.tracks.extend(tracks)

    def get_tracks(self):
        return self.tracks

    def get_tracks_count(self):
        return len(self.tracks)
