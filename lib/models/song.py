# Methods for SQL table songs

from .__init__ import CONN, CURSOR
from data.song_library import song_library
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.align import Align
import webbrowser
import time

console = Console()

error_style = "color(9)"
callout_style = "color(2)"


def print_song_table():
    table = Table(show_lines=True)
    table.add_column("ID", justify="right", style="cyan", width=3)
    table.add_column("Title", style="magenta", width=26)
    table.add_column("Artist", style="green", width=18)
    table.add_column("Genre", style="yellow", width=12)
    return table


class Song:
    ALL = []
    current_song_id = None

    def __init__(self, title, artist, genre, lyrics, url, singer_id=None, _id=None):
        self._id = _id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.lyrics = lyrics
        self.url = url
        self.singer_id = singer_id
        type(self).ALL.append(self)

    def __repr__(self):
        return f"<Song {self._id}: {self.title} - {self.artist}>"

    # Property setters

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and len(title) > 0:
            self._title = title
        else:
            raise Exception("Title must be a string of at least 1 character.")

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, artist):
        if isinstance(artist, str) and len(artist) > 0:
            self._artist = artist
        else:
            raise Exception("Artist must be a string of at least 1 character.")

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, genre):
        if isinstance(genre, str) and len(genre) > 0:
            self._genre = genre
        else:
            raise Exception("Genre must be a string of at least 1 character.")

    @property
    def lyrics(self):
        return self._lyrics

    @lyrics.setter
    def lyrics(self, lyrics):
        if isinstance(lyrics, str) and len(lyrics) > 0:
            self._lyrics = lyrics
        else:
            raise Exception("Lyrics must be a string of at least 1 character.")

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if isinstance(url, str) and len(url) > 0:
            self._url = url
        else:
            raise Exception("URL must be a string of at least 1 character.")

    # CRUD methods for Song Library

    # @classmethod
    # def execute_sql(cls, sql, values=None):
    #     # Common method to execute SQL queries
    #     if values:
    #         return cls.cursor.execute(sql, values)
    #     else:
    #         return cls.cursor.execute(sql)

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            artist TEXT,
            genre TEXT,
            lyrics TEXT,
            url TEXT,
            singer_id INTEGER
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def add_song_library(cls):
        sql = """
            INSERT INTO songs (title, artist, genre, lyrics, url, singer_id)
            VALUES (?, ?, ?, ?, ?, NULL)
        """

        for song in song_library:
            values = (
                song["title"],
                song["artist"],
                song["genre"],
                song["lyrics"],
                song["url"],
            )
            CURSOR.execute(sql, values)

            # Retrieve the last inserted row ID
            last_row_id = CURSOR.lastrowid
            cls(
                song["title"],
                song["artist"],
                song["genre"],
                song["lyrics"],
                song["url"],
                _id=last_row_id,
            )

        CONN.commit()
        console.print(cls.ALL)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS songs;
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def get_all_library(cls):
        """Return a list containing a Song object per row in the table"""
        sql = """
            SELECT id, title, artist, genre
            FROM songs
        """

        rows = CURSOR.execute(sql).fetchall()

        table = print_song_table()

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[3])

        console.print(table)

    @classmethod
    def get_library_by_title(cls, title):
        sql = """
            SELECT id, title, artist, genre
            FROM songs
            WHERE title = ?
        """

        rows = CURSOR.execute(sql, (title,)).fetchall()

        if not rows:
            console.print(f"No songs found with title {title}.", style=error_style)
        else:
            table = print_song_table()

            for row in rows:
                table.add_row(str(row[0]), row[1], row[2], row[3])

            console.print(table)

    @classmethod
    def get_library_by_artist(cls, artist):
        sql = """
            SELECT id, title, artist, genre
            FROM songs
            WHERE artist = ?
        """

        rows = CURSOR.execute(sql, (artist,)).fetchall()

        if not rows:
            console.print(f"No songs found by artist {artist}.", style=error_style)
        else:
            table = print_song_table()

            for row in rows:
                table.add_row(str(row[0]), row[1], row[2], row[3])

            console.print(table)

    @classmethod
    def get_library_by_genre(cls, genre):
        sql = """
            SELECT id, title, artist, genre
            FROM songs
            WHERE genre = ?
        """

        rows = CURSOR.execute(sql, (genre,)).fetchall()

        if not rows:
            console.print(f"No songs found in the {genre} genre.", style=error_style)
        else:
            table = print_song_table()

            for row in rows:
                table.add_row(str(row[0]), row[1], row[2], row[3])

            console.print(table)

    @classmethod
    def get_library_by_id(cls, _id):
        sql = """
            SELECT id, title, artist, genre
            FROM songs
            WHERE id = ?
        """

        rows = CURSOR.execute(sql, (_id,)).fetchall()

        if not rows:
            console.print(f"No song found with id #{_id}", style=error_style)
        else:
            table = print_song_table()

            for row in rows:
                table.add_row(str(row[0]), row[1], row[2], row[3])

            console.print(table)

    @classmethod
    def add_to_library(cls, title, artist, genre, lyrics, url):
        sql = """
            INSERT INTO songs (title, artist, genre, lyrics, url, singer_id)
            VALUES (?, ?, ?, ?, ?, NULL)
        """
        # currently can't add multi-line lyrics
        values = (title, artist, genre, lyrics, url)
        CURSOR.execute(sql, values)

        CONN.commit()
        last_row_id = CURSOR.lastrowid
        cls(title, artist, genre, lyrics, url, _id=last_row_id)
        console.print(
            f"{title} by {artist} added to Song Library.", style=callout_style
        )

    @classmethod
    def remove_from_library(cls, song_id):
        """Remove a song from library by ID"""
        sql = "DELETE FROM songs WHERE id = ?"
        CURSOR.execute(sql, (song_id,))
        CONN.commit()

        # Remove the instance from the ALL list
        removed_song = next((s for s in cls.ALL if s._id == song_id), None)
        if removed_song:
            cls.ALL.remove(removed_song)

        console.print(
            f"Removed song #{song_id} from Song Library.", style=callout_style
        )

    # CRUD methods for Your Playlist

    @classmethod
    def get_all_playlist(cls):
        sql = """
            SELECT songs.id, songs.title, songs.artist, singers.name
            FROM songs
            INNER JOIN singers
            ON songs.singer_id = singers.id
            WHERE singer_id IS NOT NULL
        """

        rows = CURSOR.execute(sql).fetchall()

        if not rows:
            console.print(
                "No songs in your playlist yet! Add your pick!", style=callout_style
            )

        if rows:
            table = Table(show_lines=True)
            table.add_column("ID", justify="right", style="cyan", width=3)
            table.add_column("Title", style="magenta", width=26)
            table.add_column("Artist", style="green", width=18)
            table.add_column("Who's Singing?", style="bold yellow", width=18)

            for row in rows:
                table.add_row(str(row[0]), row[1], row[2], row[3])

            console.print("\n", table)

    @classmethod
    def remove_all_singer_ids(cls):
        for song_instance in cls.ALL:
            song_instance.singer_id = None

    @classmethod
    def clear_playlist(cls):
        # Define the SQL query to delete all songs from the playlist
        update_songs_sql = """
            UPDATE songs
            SET singer_id = NULL
            WHERE singer_id IS NOT NULL
        """

        # Execute the SQL query to update the songs table
        CURSOR.execute(update_songs_sql)

        # Define the SQL query to delete all records from the singers table
        delete_singers_sql = """
            DELETE FROM singers
        """

        # Execute the SQL query to delete records from the singers table
        CURSOR.execute(delete_singers_sql)
        CONN.commit()

        # Clear the ALL list
        cls.ALL = []

        # need to also remove singer_ids from Song
        cls.remove_all_singer_ids()

        console.print(
            "Playlist cleared - time to start a new one!", style=callout_style
        )

    @classmethod
    def update_singer_id(cls, song_id, singer_id):
        """Update the singer_id for a song if it's currently NULL."""
        # Check if the current singer_id is NULL
        check_sql = "SELECT singer_id FROM songs WHERE id = ?"
        current_singer_id = CURSOR.execute(check_sql, (int(song_id),)).fetchone()

        if current_singer_id[0] is not None:
            console.print(
                "This song is already in Your Playlist. Choose another!",
                style=error_style,
            )
            return

        # Update the singer_id if it's currently NULL
        update_sql = "UPDATE songs SET singer_id = ? WHERE id = ?"
        values = (singer_id, int(song_id))
        console.print(f"Song #{song_id} added to Your Playlist!", style=callout_style)
        CURSOR.execute(update_sql, values)
        CONN.commit()

    @classmethod
    def get_song_id_from_singer_id(cls, singer_id):
        """Get the song's ID based on the singer's ID"""
        sql = "SELECT id FROM songs WHERE singer_id = ?"
        result = CURSOR.execute(sql, (singer_id,)).fetchone()
        return result[0] if result is not None else None

    @classmethod
    def remove_singer_id(cls, song_id, singer_name):
        if song_id:
            """Set singer_id back to NULL for song based on song_id."""
            sql = "UPDATE songs SET singer_id = NULL WHERE id = ?"
            # needs to pass a tuple
            values = (int(song_id),)

            CURSOR.execute(sql, values)
            CONN.commit()
            console.print(
                f"Song #{song_id} removed from Your Playlist.", style=callout_style
            )
        else:
            console.print(f"{singer_name} hasn't signed up yet!", style=error_style)

    @classmethod
    def song_id_exists_in_songs(song_id):
        CURSOR.execute("SELECT COUNT(*) FROM songs WHERE id = ?", (song_id,))
        count = CURSOR.fetchone()[0]
        return count > 0

    @classmethod
    def load_next_song(cls):
        """Load the next song from the queue."""
        # Check if there are any songs in the queue
        sql = """
            SELECT songs.id, songs.title, songs.artist, songs.lyrics, songs.url, singers.name
            FROM songs
            INNER JOIN singers
            ON songs.singer_id = singers.id
            WHERE singer_id IS NOT NULL
            ORDER BY songs.singer_id
            LIMIT 1
        """
        result = CURSOR.execute(sql).fetchone()

        if not result:
            console.print(
                "No songs in your playlist yet! Add your pick!", style=callout_style
            )

        if result:
            song_id, title, artist, lyrics, url, singer_name = result
            cls.current_song_id = song_id

            webbrowser.open(url)

            verses = lyrics.split("*")

            with Live(transient=True, screen=True, console=console) as live:
                live.update(
                    f"Loading next song: {title} by {artist}, Sung by: {singer_name}"
                )

                exit_live = False
                i = 0

                for verse in verses:
                    live.update(verse)
                    lines = verse.splitlines()
                    exit_live = False

                    while not exit_live:
                        for i in range(len(lines)):
                            highlighted_line = f"[bold yellow]{lines[i]}[/bold yellow]"
                            display_text = Align.center(
                                "\n".join(
                                    lines[j] if j != i else highlighted_line
                                    for j in range(len(lines))
                                )
                            )
                            live.update(display_text)

                            time.sleep(2)

                        exit_live = True

            # Need to run remove_singer_id on this Song instance
            cls.remove_singer_id(song_id, singer_name)
