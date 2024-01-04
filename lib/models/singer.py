# Methods for SQL table singers

from .song import (
    Song,
    CONN,
    CURSOR,
    error_style,
    callout_style,
    update_style,
)
from rich.console import Console
from rich.table import Table

console = Console()


class Singer:
    all = {}

    def __init__(self, name, song_id, _id=None):
        self._id = _id
        self.name = name
        self.song_id = song_id

    def __repr__(self):
        return f"<Song {self._id}: {self.name}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0 and name not in Singer.all:
            self._name = name
        else:
            raise Exception("Name must be a unique string of at least 1 character.")

    @property
    def song_id(self):
        return self._song_id

    @song_id.setter
    def song_id(self, song_id):
        self._song_id = song_id
        # song_id = int(song_id)  # Convert song_id to integer for comparison
        # console.print(Song.ALL)
        # for song in Song.all:
        #     print(f"Type of song._id: {type(song._id)}, Value: {song._id}")
        #     print(f"Type of song_id: {type(song_id)}, Value: {song_id}")
        #     if song._id == song_id:
        #         self._song_id = song_id
        #         return
        # raise Exception(f"No song with ID #{song_id} in Song Library.")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS singers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            song_id INTEGER
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create_singer(cls, name, song_id):
        """Instantiate a new singer, assign an ID, and insert into the database."""
        # Check if the song_id is already associated with a singer
        select_sql = """
            SELECT id FROM singers WHERE song_id = ?
        """
        select_values = (song_id,)
        existing_singer_ids = CURSOR.execute(select_sql, select_values).fetchall()

        if existing_singer_ids:
            console.print(f"A singer is already associated with song #{song_id}")
            return None

        # If not exists, create a new singer, insert into the database, and return the singer object
        singer = cls(name.title(), song_id)
        cls.insert_singer_into_db(singer, song_id)
        return singer

    @classmethod
    def insert_singer_into_db(cls, singer, song_id):
        # Insert the singer data into the database
        insert_sql = """
            INSERT INTO singers (name, song_id) VALUES (?, ?)
        """
        insert_values = (singer.name, song_id)
        CURSOR.execute(insert_sql, insert_values)
        CONN.commit()

    @classmethod
    def remove_singer_by_name(cls, name):
        """Remove a singer by name."""
        singer_id = cls.get_singer_id(name)

        if singer_id is not None:
            sql = "DELETE FROM singers WHERE id = ?"
            CURSOR.execute(sql, (singer_id,))
            CONN.commit()
            console.print(f"Removed {name}.", style=update_style)

        else:
            return None

    @classmethod
    def get_singer_id(cls, name):
        """Get the singer_id based on the singer's name."""
        sql = "SELECT id FROM singers WHERE name = ?"
        result = CURSOR.execute(sql, (name,)).fetchone()
        return result[0] if result is not None else None

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS singers
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def song_id_exists_in_singers(song_id):
        CURSOR.execute("SELECT COUNT(*) FROM singers WHERE song_id = ?", (song_id,))
        count = CURSOR.fetchone()[0]
        return count > 0
