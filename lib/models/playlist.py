# from __init__ import CONN, CURSOR
from models.song import Song

# from Singer import Singer


class Playlist:
    def __init__(self):
        self.songs = songs()

    def songs(self):
        return [song for song in Song.all if song.playlist is self]
