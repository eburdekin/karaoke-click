from .__init__ import CONN, CURSOR
from .song import Song
from .singer import Singer


class Queue:
    all = []

    def __init__(self):
        type(self).all.append(self)

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS queue (
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
    def add_song_to_queue(cls, song_id, singer):
        for song in Song.all:
            # if song_id == song.id:
            #     # song.singer_id = singer.id
            #     # cls.all.append(song)
            sql = """
                    INSERT INTO queue (title, artist, genre, lyrics, singer_id)
                    VALUES (?, ?, ?, ?, ?)
                    """
            values = (
                song.title,
                song.artist,
                song.genre,
                song.lyrics,
                singer.id,
            )
            CURSOR.execute(sql, values)
            CONN.commit()
            # break

    @classmethod
    def display(cls):
        print("Current Queue:")
        """Return a list containing a Song object per row in the table"""
        sql = """
            SELECT id, title, artist, singer_id
            FROM queue
        """

        rows = CURSOR.execute(sql).fetchall()

        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Artist: {row[2]}, Singer: {row[3]}")

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS queue
        """
        CURSOR.execute(sql)
        CONN.commit()
