from .__init__ import CONN, CURSOR

from data.song_library import song_library


class Song:
    all = {}

    def __init__(self, title, artist, genre, lyrics, singer_id=None, id=None):
        self.id = id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.lyrics = lyrics
        self.singer_id = singer_id
        type(self).all.append(self)

    def __repr__(self):
        return f"<Song {self.id}: {self.title}, {self.singer}>"

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
    def add_song_library(cls):
        sql = """
            INSERT INTO songs (title, artist, genre, lyrics, singer_id)
            VALUES (?, ?, ?, ?, NULL)
        """

        for song in song_library:
            values = (
                song["title"],
                song["artist"],
                song["genre"],
                song["lyrics"],
            )
            CURSOR.execute(sql, values)

        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS songs;
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def get_all(cls):
        """Return a list containing a Song object per row in the table"""
        sql = """
            SELECT id, title, artist, genre
            FROM songs
        """

        rows = CURSOR.execute(sql).fetchall()

        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Artist: {row[2]}, Genre: {row[3]}")

    @classmethod
    def get_queued(cls):
        """Return a list containing a Song object per row in the table"""
        sql = """
            SELECT songs.id, songs.title, songs.artist, singers.name
            FROM songs
            INNER JOIN singers
            ON songs.singer_id = singers.id
            WHERE singer_id IS NOT NULL
        """

        rows = CURSOR.execute(sql).fetchall()
        print("Songs in queue:")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Artist: {row[2]}, Sung by: {row[3]}")

    @classmethod
    def update_singer_id(cls, song_id, singer_id):
        """Update the singer_id for a song."""
        sql = "UPDATE songs SET singer_id = ? WHERE id = ?"
        values = (singer_id, int(song_id))
        CURSOR.execute(sql, values)
        CONN.commit()

    @classmethod
    def get_by_artist(cls, artist):
        """Return a list containing a Song object per row in the table"""
        sql = """
            SELECT id, title, artist, genre
            FROM songs
            WHERE artist = ?
        """

        print(f"Results for artist: {artist}")
        rows = CURSOR.execute(sql, (artist,)).fetchall()

        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Artist: {row[2]}, Genre: {row[3]}")

    @classmethod
    def get_by_genre(cls, genre):
        """Return a list containing a Song object per row in the table"""
        sql = """
            SELECT id, title, artist, genre
            FROM songs
            WHERE genre = ?
        """

        print(f"Results for genre: {genre}")
        rows = CURSOR.execute(sql, (genre,)).fetchall()

        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Artist: {row[2]}, Genre: {row[3]}")
