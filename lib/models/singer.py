from .__init__ import CONN, CURSOR
from .song import Song


class Singer:
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0 and name not in Singer.all:
            self._name = name
        else:
            raise Exception("unique name, string of at least 1 char")

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
        singer = cls(name)
        cls.insert_singer_into_db(singer, song_id)
        return singer

    @classmethod
    def insert_singer_into_db(cls, singer, song_id):
        """Insert singer data into the database."""
        sql = """
            INSERT INTO singers (name, song_id) VALUES (?, ?)
        """
        values = (singer.name, song_id)
        CURSOR.execute(sql, values)
        CONN.commit()

    @classmethod
    def remove_singer_by_name(cls, name):
        """Remove a singer by name."""
        singer_id = cls.get_singer_id(name)

        if singer_id is not None:
            # Remove the singer from the database
            sql = "DELETE FROM singers WHERE id = ?"
            CURSOR.execute(sql, (singer_id,))
            CONN.commit()

            deleted_singer = cls(name, id=singer_id)
            return deleted_singer
        else:
            print(f"No singer found with the name: {name}")
            return None

    @classmethod
    def view(cls):
        sql = """
        SELECT singers.id, singers.name, songs.title
        FROM singers
        INNER JOIN songs
        ON singers.song_id = songs.id
        """
        rows = CURSOR.execute(sql).fetchall()
        print("Currently in line:")
        for row in rows:
            print(f"#{row[0]} Name: {row[1]}, Song: {row[2]}")
        if not rows:
            print("Nobody, yet! Add your name!")

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
