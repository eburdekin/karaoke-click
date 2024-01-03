# from .__init__ import CONN, CURSOR
from .song import Song, CONN, CURSOR
from rich.console import Console
from rich.table import Table

console = Console()

error_style = "color(9)"
callout_style = "color(2)"
update_style = "color(6)"


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
        singer = cls(name)
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
            console.print(f"Removed {name} from the queue.", style=update_style)
            deleted_singer = cls(name, id=singer_id)
            return deleted_singer

        else:
            console.print(f"No singer found with the name: {name}", style=error_style)
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
