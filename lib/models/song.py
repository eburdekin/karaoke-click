from .__init__ import CONN, CURSOR

from data.song_library import song_library

from rich.console import Console
from rich.table import Table
from rich.live import Live

import time

console = Console()

error_style = "color(9)"
callout_style = "color(2)"
update_style = "color(6)"


class Song:
    all = {}
    current_song_id = None

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

        table = Table(title="All Songs")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Artist", style="green")
        table.add_column("Genre", style="yellow")

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[3])

        console.print(table)

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

        if not rows:
            console.print("No songs yet! Add yours!", style=callout_style)

        if rows:
            table = Table(title=f"Next Up")
            table.add_column("ID", justify="right", style="cyan")
            table.add_column("Title", style="magenta")
            table.add_column("Artist", style="green")
            table.add_column("Who's Singing?", style="yellow")

            for row in rows:
                table.add_row(str(row[0]), row[1], row[2], row[3])

            console.print(table)

    @classmethod
    def update_singer_id(cls, song_id, singer_id):
        """Update the singer_id for a song if it's currently NULL."""
        # Check if the current singer_id is NULL
        check_sql = "SELECT singer_id FROM songs WHERE id = ?"
        current_singer_id = CURSOR.execute(check_sql, (int(song_id),)).fetchone()

        if current_singer_id[0] is not None:
            console.print(
                "This song is already in the queue. Choose another!",
                style=error_style,
            )
            return

        # Update the singer_id if it's currently NULL
        update_sql = "UPDATE songs SET singer_id = ? WHERE id = ?"
        values = (singer_id, int(song_id))
        console.print(f"Song #{song_id} added to queue!", style=update_style)
        CURSOR.execute(update_sql, values)
        CONN.commit()

    @classmethod
    def load_next_song(cls):
        """Load the next song from the queue."""
        # Check if there are any songs in the queue
        sql = """
            SELECT songs.id, songs.title, songs.artist, songs.lyrics, singers.name
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
            song_id, title, artist, lyrics, singer_name = result
            cls.current_song_id = song_id

            chunks = lyrics.split("\n")

            with Live(transient=True) as live:
                live.update(
                    f"Loading next song: {title} by {artist}, Sung by: {singer_name}"
                )

                for chunk in chunks:
                    live.update(chunk)
                    lines = chunk.splitlines()
                    exit_live = False

                    while not exit_live:
                        for i in range(len(lines)):
                            highlighted_line = f"[bold yellow]{lines[i]}[/bold yellow]"
                            display_text = "\n".join(
                                lines[j] if j != i else highlighted_line
                                for j in range(len(lines))
                            )
                            live.update(display_text)

                            time.sleep(2)

                        exit_live = True
            # else:
            console.print("No songs yet! Add yours!", style=callout_style)

    @classmethod
    def exit_loop(cls):
        # Add any necessary cleanup code here
        pass

    @classmethod
    def get_by_title(cls, title):
        """Return a list containing a Song object per row in the table"""
        sql = """
            SELECT id, title, artist, genre
            FROM songs
            WHERE title = ?
        """

        rows = CURSOR.execute(sql, (title,)).fetchall()

        table = Table()
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Artist", style="green")
        table.add_column("Genre", style="yellow")

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[3])

        console.print(table)

    @classmethod
    def get_by_artist(cls, artist):
        """Return a list containing a Song object per row in the table"""
        sql = """
            SELECT id, title, artist, genre
            FROM songs
            WHERE artist = ?
        """

        rows = CURSOR.execute(sql, (artist,)).fetchall()

        table = Table()
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Artist", style="green")
        table.add_column("Genre", style="yellow")

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[3])

        console.print(table)

    @classmethod
    def get_by_genre(cls, genre):
        """Return a list containing a Song object per row in the table"""
        sql = """
            SELECT id, title, artist, genre
            FROM songs
            WHERE genre = ?
        """

        rows = CURSOR.execute(sql, (genre,)).fetchall()

        table = Table()
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Artist", style="green")
        table.add_column("Genre", style="yellow")

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[3])

        console.print(table)

    @classmethod
    def add_new_song_to_library(cls, title, artist, genre, lyrics):
        sql = """
            INSERT INTO songs (title, artist, genre, lyrics, singer_id)
            VALUES (?, ?, ?, ?, NULL)
        """

        values = (title, artist, genre, lyrics)
        CURSOR.execute(sql, values)

        CONN.commit()
        console.print(f"{title} by {artist} added to Song Library.")
