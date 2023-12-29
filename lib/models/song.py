# from __init__ import CONN, CURSOR


class Song:
    all = {}

    def __init__(self, title, artist, genre, year, lyrics, playlist, singer, id=None):
        self.id = id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.year = year
        self.lyrics = lyrics
        self.playlist = playlist
        self.singer = singer
        type(self).all.append(self)

    @property
    def singer(self):
        return self._singer

    @singer.setter
    def singer(self, singer):
        if hasattr(self, "singer"):
            raise Exception("Song already has Singer")
        elif not isinstance(singer, Singer):
            raise Exception("Singer must be of Singer class")
        else:
            self._singer = singer
