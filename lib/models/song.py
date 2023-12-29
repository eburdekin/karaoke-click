# from __init__ import CONN, CURSOR


class Song:
    all = {}

    def __init__(self, title, artist, genre, lyrics, singer_id, id=None):
        self.id = id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.lyrics = lyrics
        self.singer_id = singer_id
        type(self).all.append(self)

    def __repr__(self):
        return f"<Song {song.id}: {song.title}, {song.singer}>"

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

    # CRUD methods for Song
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            artist TEXT,
            genre TEXT,
            lyrics TEXT,
            singer_id INTEGER
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS songs;
        """
        CURSOR.execute(sql)
        CONN.commit()
